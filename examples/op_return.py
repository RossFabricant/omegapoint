'''This example shows how to work with OP returns: 
    1) Pull raw returns with load_op_raw_return
    2) Convert them to daily returns at forward horizons with load_op_return
    3) Use TSQL to winsorize the returns. 
'''

from omegapoint import omegapoint as op
import os
from datetime import date 
import pandas as pd
import numpy as np
import logging 
from models import utils

def load_op_raw_return(axioma_ids, start_date, end_date):
    errors = []
    for id in axioma_ids:
        try:
            df_ret = op.get_stock_returns('model_provider_id', [id], start_date, end_date)
            df_ret = df_ret.rename(columns = {'model_provider_id':'axioma_id', 'specific_return':'idio_return'})
            df_ret.to_sql('op_raw_return', utils.get_db_connection(), if_exists = 'append', index = False)
        except Exception as e:
            errors.append((e,id))
    return errors

def load_op_return(axioma_ids, table_name):
    day_counts = [1,5,10,15,21,42,63,126]
    columns = ['date', 'axioma_id']
    for n in day_counts:
        for ret_type in ['total', 'idio', 'sector']:
            columns.append(f'{ret_type}_{n}d_fwd')
    errors = []
    for id in axioma_ids:
        try:
            print(id)
            df = pd.read_sql(f'''
            select axioma_id,date,total_return,factor_return,idio_return,sector_return
            from op_raw_return 
            where axioma_id = '{id}'
        ''', utils.get_db_connection())
            for n in day_counts:
                for ret_type in ['total']:
                    col_name = f'{ret_type}_{n}d_fwd'
                    df[col_name] = (1+df[[f'{ret_type}_return']]).pct_change(n).shift(-n)
                for ret_type in ['idio', 'sector']:
                    col_name = f'{ret_type}_{n}d_fwd'
                    total_col_name = f'total_return'
                    df[col_name] = (df.shift(-n)[f'{ret_type}_return'] - 
                            df[f'{ret_type}_return']) / \
                            (1+df[total_col_name])
            df = df.rename(columns = {'total_return' : 'total_return_index',
                                      'factor_return' : 'factor_return_index',
                                      'idio_return' : 'idio_return_index',
                                      'sector_return': 'sector_return_index'})
            df = df.replace([np.inf, -np.inf], np.nan)
            
            df.to_sql(table_name, utils.get_db_connection(), if_exists = 'append', index = False)
        except Exception as e:
            errors.append((e,id))
    return errors

#Set some values that are easiest to set from SQL. 
def update_op_return(table_name):
    command = f'''
drop table if exists #map 
drop table if exists #op_return
--Take the max sedol arbitrarily. 
select  map.axioma_id, max(map.sedol) sedol 
into #map
from sedol_map map 
group by map.axioma_id 

create clustered index map_idx on #map (sedol)

update {table_name}
set idio_and_sector_return_index = (idio_return_index + sector_return_index),
idio_and_sector_0d_fwd = (sector_0d_fwd + idio_0d_fwd),
idio_and_sector_1d_fwd = (sector_1d_fwd + idio_1d_fwd),
idio_and_sector_5d_fwd = (sector_5d_fwd + idio_5d_fwd),
idio_and_sector_10d_fwd = (sector_10d_fwd + idio_10d_fwd),
idio_and_sector_15d_fwd = (sector_15d_fwd + idio_15d_fwd),
idio_and_sector_21d_fwd = (sector_21d_fwd + idio_21d_fwd),
idio_and_sector_42d_fwd = (sector_42d_fwd + idio_42d_fwd),
idio_and_sector_63d_fwd = (sector_63d_fwd + idio_63d_fwd),
idio_and_sector_126d_fwd = (sector_126d_fwd + idio_126d_fwd)
from {table_name} 

select ret.date,
ret.axioma_id,
map.sedol,
LAG(total_1d_fwd) OVER(partition by ret.axioma_id order by ret.date) total_0d_fwd,
LAG(idio_1d_fwd) OVER(partition by ret.axioma_id order by ret.date) idio_0d_fwd,
 LAG(sector_1d_fwd) OVER(partition by ret.axioma_id order by ret.date) sector_0d_fwd, 
LAG(idio_and_sector_1d_fwd) OVER(partition by ret.axioma_id order by ret.date) idio_and_sector_0d_fwd
into #op_return
from {table_name} ret
join #map map on map.axioma_id = ret.axioma_id

update ret
set ret.sedol = temp.sedol, 
ret.total_0d_fwd = temp.total_0d_fwd,
ret.idio_0d_fwd = temp.idio_0d_fwd,
ret.sector_0d_fwd = temp.sector_0d_fwd,
ret.idio_and_sector_0d_fwd = temp.idio_and_sector_0d_fwd
from {table_name} ret 
join #op_return temp on temp.axioma_id = ret.axioma_id and temp.date = ret.date

 
'''
    connection = utils.get_db_connection()
    connection.execute(command)

    
def get_winsorize_sql(col_name, table_name):
    return f'''
update wr 
set wr.{col_name}_ceiling = t.ceiling,
wr.{col_name}_floor = t.floor 
from winsorize_return wr 
join (
select
    distinct ret.date,
    percentile_disc(0.995) within group (order by {col_name} ) over (partition by date) as ceiling,
    percentile_disc(0.005) within group (order by {col_name}) over (partition by date) as floor
from {table_name} ret  
) t on t.date = wr.date 
'''    

def get_ceiling(col_name, table_name):
    return f'''
    update ret 
    set ret.{col_name} = wr.{col_name}_ceiling
    from {table_name} ret 
    join winsorize_return wr on wr.date = ret.date and wr.{col_name}_ceiling is not NULL
    where ret.{col_name} > wr.{col_name}_ceiling;
    '''

def get_floor(col_name, table_name):
    return f'''
    update ret 
    set ret.{col_name}  = wr.{col_name}_floor
    from {table_name} ret 
    join winsorize_return wr on wr.date = ret.date and wr.{col_name}_floor is not NULL
    where ret.{col_name} < wr.{col_name}_floor;
    '''

def winsorize_op_return(table_name):
    columns = [    
'total_0d_fwd',
'idio_0d_fwd',
'sector_0d_fwd',
'idio_and_sector_0d_fwd',
'total_1d_fwd',
'idio_1d_fwd',
'sector_1d_fwd',
'idio_and_sector_1d_fwd',
'total_5d_fwd',
'idio_5d_fwd',
'sector_5d_fwd',
'idio_and_sector_5d_fwd',
'total_10d_fwd',
'idio_10d_fwd',
'sector_10d_fwd',
'idio_and_sector_10d_fwd',
'total_15d_fwd',
'idio_15d_fwd',
'sector_15d_fwd',
'idio_and_sector_15d_fwd',
'total_21d_fwd',
'idio_21d_fwd',
'sector_21d_fwd',
'idio_and_sector_21d_fwd',
'total_42d_fwd',
'idio_42d_fwd',
'sector_42d_fwd',
'idio_and_sector_42d_fwd',
'total_63d_fwd',
'idio_63d_fwd',
'sector_63d_fwd',
'idio_and_sector_63d_fwd',
'total_126d_fwd',
'idio_126d_fwd',
'sector_126d_fwd',
'idio_and_sector_126d_fwd'
    ]
    connection = utils.get_db_connection()
    connection.execute('truncate table winsorize_return')
    connection.execute(f'insert into winsorize_return (date) select distinct date from {table_name}')
    for col_name in columns: 
        print('building winsorize_return ', col_name)
        query = get_winsorize_sql(col_name, table_name)
        connection.execute(query)
        
    for col_name in columns: 
        print('winsorizing ', col_name)
        connection.execute(get_ceiling(col_name, table_name))
        connection.execute(get_floor(col_name, table_name))

if __name__ == 'main':
    #Note to get winsorization to work properly, first run: 
    #truncate table op_return 
    #Change this to op_return_test to test.
    table_name = 'op_return'
    missing_ids = pd.read_sql('''
    select distinct axioma_id from sedol_map map
    where not exists (select * from op_raw_return ret 
        where ret.axioma_id = map.axioma_id)
    ''', utils.get_db_connection()).axioma_id.values
    errors_raw = load_op_raw_return(missing_ids, date(2012,1,1), date(2019,12,31))
    #errors_raw = load_op_raw_return(['11D7GQAK9'], date(2012,1,1), date(2019,12,31))
    print(errors_raw)
    
    missing_op_return_ids = pd.read_sql('''
    select distinct axioma_id from op_raw_return raw
    where not exists (select * from op_return ret 
        where ret.axioma_id = raw.axioma_id)
    ''', utils.get_db_connection()).axioma_id.values
    errors_op_return = load_op_return(missing_op_return_ids, table_name)
    print(errors_op_return)
    update_op_return(table_name)
    winsorize_op_return(table_name)
    print('Done.')
        
