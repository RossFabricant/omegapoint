"""
#This works
print(get_models())    
#This fails
res = create_portfolio(name='TestName6', default_model_id='fake')

#This fails too.
try:
    res = create_portfolio(name='TestName6', default_model_id='fake')
except GqlError as e:
    print(f"GQL error. Query Id is {e.errors['extensions']['queryId']}")
    print(f"Operation is:\n{e.operation}")
    print(f"Error is:\n{e.errors}")
#This works
res = create_portfolio(name='TestName7', default_model_id='AXUS4-MH')
print(res)
#This works
bad = [p for p in get_portfolios() if p.name !='Equal Weighted Portfolio']
for p in bad:
    delete_portfolio_by_id(p.id)

#Create and delete a portfolio
res = op.create_portfolio(name='TestName7', default_model_id='AXUS4-MH')
print(op.get_portfolios())
op.delete_portfolio('TestName7')
print(op.get_portfolios())

#Load a portfolio from CSV 
# df = pd.read_csv('c:\\users\\ross\\op\\port_test.csv')
#load_portfolio_position('Test Name', df)
"""

import sys
sys.path.append(r'C:\Program Files\Python38\lib\site-packages')
sys.path.append(r'C:\Users\Ross')

import os
import pandas as pd

from sgqlc.operation import Operation
from omega_point import schema
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.types import Type, Field, list_of
from sgqlc.types.relay import Connection, connection_args

class GqlError(Exception):
    def __init__(self, message, errors, operation):
        super().__init__(message)
        self.errors = errors
        self.operation = operation
        
    def error_list(self):
        return [e['message'] for e in self.errors['errors']]
    
    def __str__(self):
        return '\n'.join(self.error_list())

def call_operation(self):
    url = os.getenv('OMEGA_POINT_URL')
    headers = {
        'Authorization':  os.getenv('OMEGA_POINT_API_KEY')
    }
    endpoint = HTTPEndpoint(url, headers)
    data = endpoint(self)
    if 'errors' in data: 
        raise GqlError(str(data), data, self)
    return self+data

Operation.__call__ = call_operation

#fields is what gets returned by output
#kwargs is what gets sent as input.
def create_portfolio(fields=['name','id'], **kwargs):
    if 'name' not in kwargs:
        raise RuntimeError('Portfolio name is required.')
    same_name = [p for p in get_portfolios() if p.name == kwargs['name']]
    if len(same_name) > 0: 
        raise RuntimeError(f"There's already a portfolio with name {kwargs['name']}.")
    oper = Operation(schema.Mutation)
    port = schema.NewPortfolio(**kwargs)
    oper.create_portfolio(portfolio=port).__fields__(*fields)
    return oper().create_portfolio

def get_portfolios(fields=['name','id']):
    oper = Operation(schema.Query)
    oper.portfolios().__fields__(*fields)
    return oper().portfolios 

def get_portfolio_id(name):
    ret = [p.id for p in get_portfolios() if p.name == name]
    if len(ret) == 0: raise RuntimeError(f'There are no portfolios with the name %s' % name)
    if len(ret) > 1: raise RuntimeError(f'There are multiple portfolios with the name %s' % name)
    return ret[0]

def delete_portfolio(name):    
    return delete_portfolio_by_id(get_portfolio_id(name))

def delete_portfolio_by_id(port_id):    
    oper = Operation(schema.Mutation)
    oper.delete_portfolio(id = port_id).__fields__(ok = True)
    return oper().delete_portfolio

def get_models(*args, **kwargs):
    oper = Operation(schema.Query)   
    models = oper.models(**kwargs)
    models.availability().__fields__(dates = None)
    return oper().models 

def delete_portfolio_positions(name):
    oper= Operation(schema.Mutation)
    oper.delete_position_set_dates(portfolio_id = get_portfolio_id(name), all_dates=True)
    return oper()
    
def load_portfolio_position(name, df):
    port_id = get_portfolio_id(name)
    for date in list(df.date.unique()):
        oper = Operation(schema.Mutation)
        equities = [schema.PositionSetEquityInput(id = schema.PositionSetEquityIdInput(sedol=r[1].sedol),
                                          economic_exposure = r[1].economic_exposure) 
            for r in df.iterrows()
            if r[1].date == date]
        position_set = schema.PositionSetDateInput(date = date, equities = equities)
        oper = Operation(schema.Mutation)
        oper.upload_position_set_date(portfolio_id=port_id, data=position_set)
        oper()

"""
port_name = 'Test Name'
model_id = 'AXUS4-MH'
start_date = '2018-12-31'
end_date = '2020-01-09'

for exposure in op.get_portfolio_exposure(port_name, model_id, start_date, end_date):
    for f in exposure.factors:
        print(exposure.date, f)
"""
def get_portfolio_exposure(port_name, model_id, start_date, end_date):
    oper = Operation(schema.Query)   
    port = oper.model(id=model_id).portfolio(id=get_portfolio_id(port_name)) 
    exposure = port.exposure(from_=start_date, to=end_date)
    exposure.__fields__()
    exposure.factors().__fields__()
    return oper().model.portfolio.exposure

def test():
    print('4')

#res = create_portfolio(name='TestName7', default_model_id='AXUS4-MH')
#print(get_portfolios())
#delete_portfolio('TestName7')
#print(get_portfolios())
