'''This is an example of how to use the security search API'''

from omegapoint import omegapoint as op 
from omegapoint import utils
from omegapoint import schema
import pandas as pd
from datetime import date
import os
from datetime import date, datetime

missing_sedols_go_here = r'x:\bulk_data\sedols.txt'

sedols = list(pd.read_csv(missing_sedols_go_here).sedol.values)

portfolio = 'rwf_test3'
#Arbitary dates, to catch changes.
dates = utils.weekdays(date(2010,1,1), date(2020,4,4))
for dt in dates:
    print(dt)
    df_pos = pd.DataFrame(data = [[dt, sedol, 1e6] for sedol in sedols], columns = ['date', 'sedol', 'economic_exposure'])

    try:
        op.upload_portfolio_positions(portfolio, df_pos)
    except URLError as err:
        print(err)
        continue
        
    count = 0
    total_count = 0
    first_for_date = True
    first_row = True

    while (first_for_date or count  > 0):
        oper = op.OpOperation(schema.Query)   
        filter = schema.SecuritySearchFilter()
        universe = schema.SecuritySearchFilterUniverse(type = schema.Universe.PORTFOLIO, 
                                                       in_= op.get_portfolio_id(portfolio))
        filter.__setattr__('universe', [universe])

        security_search = oper.model(id='AXWW4-MH').security_search(on = dt, filter = [filter], take=200, 
                                                                    skip = total_count)
        security_search.count()

        security_search.securities().__fields__('id', 'sedol', 'model_provider_id', ) 
        print(dt,count, total_count)
        try:
            results = oper()
            data = [(dt, res.id, res.sedol, res.model_provider_id) 
                for res in results.model.security_search.securities]
            columns = ['date', 'op_id', 'sedol', 'axioma_id']
            if len(data) > 0:
                df_out = pd.DataFrame(data = data, columns = columns)
                df_out.to_sql('load_missing_sedols', utils.get_db_connection(), if_exists = 'append', index = False)
            count = results.model.security_search.count
            total_count += min(200, count)
        except op.GqlError as gql_err:
            print(gql_err)
            count = 0
        first_for_date = False

