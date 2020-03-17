import os
import pandas as pd

from sgqlc.operation import Operation
from omegapoint import schema
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.types import Type, Field, list_of
from sgqlc.types.relay import Connection, connection_args
import logging
logging.basicConfig()

#op.logger.setLevel('DEBUG') to see queries.
#op.logger.setLevel('INFO') to hide queries.
logger = HTTPEndpoint.logger
DEFAULT_MODEL_ID = os.getenv('OMEGA_POINT_DEFAULT_MODEL_ID')
API_KEY = os.getenv('OMEGA_POINT_API_KEY')
URL = os.getenv('OMEGA_POINT_URL')

class GqlError(Exception):
    def __init__(self, message, errors, operation):
        super().__init__(message)
        self.errors = errors
        self.operation = operation
        
    def error_list(self):
        return [e['message'] for e in self.errors['errors']]
    
    def __str__(self):
        return '\n'.join(self.error_list())


class OpOperation(Operation):
    def __init__(self, typ=None, name=None, **args):
        super().__init__(typ, name, **args)
        
    def __call__(self):
        url = URL
        headers = {
            'Authorization':  API_KEY
        }
        endpoint = HTTPEndpoint(url, headers)
        data = endpoint(self)
        if 'errors' in data: 
            logger.error(f'Failed query:\n{self}')
            raise GqlError(str(data), data, self)
        return self+data

def create_portfolio(name, default_model_id = DEFAULT_MODEL_ID):
    same_name = [p for p in get_portfolios() if p.name == name]
    if len(same_name) > 0: 
        raise RuntimeError(f"There's already a portfolio with name {name}.")
    oper = OpOperation(schema.Mutation)
    port = schema.NewPortfolio(name = name, default_model_id = default_model_id)
    oper.create_portfolio(portfolio=port)
    return oper().create_portfolio

def get_portfolios(fields=['name','id']):
    oper = OpOperation(schema.Query)
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
    oper = OpOperation(schema.Mutation)
    oper.delete_portfolio(id = port_id).__fields__(ok = True)
    return oper().delete_portfolio

def get_models():
    oper = OpOperation(schema.Query)   
    models = oper.models()
    models.__fields__()
    models.availability().__fields__(dates = None)
    return oper().models 

def delete_portfolio_positions(name):
    oper= OpOperation(schema.Mutation)
    oper.delete_position_set_dates(portfolio_id = get_portfolio_id(name), all_dates=True)
    return oper()
    
def update_portfolio(port_id, alias = None, name = None, default_model_id = None, rollover_position_set_to_current_date = None):
    oper = OpOperation(schema.Mutation)
    pu = schema.PortfolioUpdate()
    if alias is not None: pu.__setattr__('alias', alias)
    if name is not None: pu.__setattr__('name', name)
    if default_model_id is not None: pu.__setattr__('default_model_id', default_model_id)
    if rollover_position_set_to_current_date is not None: pu.__setattr__('rollover_position_set_to_current_date',rollover_position_set_to_current_date)
    oper.update_portfolio(id = port_id, portfolio = pu).__fields__(id = True)
    return oper().update_portfolio
    
def upload_portfolio_positions(name, df):
    port_id = get_portfolio_id(name)
    for date in list(df.date.unique()):
        oper = OpOperation(schema.Mutation)
        equities = [schema.PositionSetEquityInput(id = schema.PositionSetEquityIdInput(sedol=r[1].sedol),
                                          economic_exposure = r[1].economic_exposure) 
            for r in df.iterrows()
            if r[1].date == date]
        position_set = schema.PositionSetDateInput(date = date, equities = equities)
        oper = OpOperation(schema.Mutation)
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
    oper = OpOperation(schema.Query)   
    port = oper.model(id=model_id).portfolio(id=get_portfolio_id(port_name)) 
    exposure = port.exposure(from_=start_date, to=end_date)
    exposure.__fields__()
    exposure.factors().__fields__()
    return oper().model.portfolio.exposure

#benchmark = [schema.PositionSetInput(id = 'SP500', type='BENCHMARK', weight = 70),
#             schema.PositionSetInput(id = 'Russell3000', type='BENCHMARK', weight = 30)]
#df_summary, df_factors = get_portfolio_performance('Equal Weighted Portfolio', '2020-01-02', '2020-01-15', benchmark)
def get_portfolio_performance(name, start_date, end_date, 
                              base = None, interval = schema.PositionSetInterval.AUTO, model_id = DEFAULT_MODEL_ID):
    summary_fields = ['trading', 'factors', 'specific']
    factor_fields = ['id', 'name', 'category', 'value']
    if base is None: base = []
    oper = OpOperation(schema.Query)   
    model = oper.model(id = model_id)
    port = schema.PositionSetInput(id = get_portfolio_id(name), type='PORTFOLIO')
    model.simulation(position_set = port, from_ = start_date, to = end_date, 
                     base = base, interval = interval).performance.__fields__('date')
    attr = oper.model.simulation.performance.percent_return_cumulative.attribution
    attr.summary.__fields__(*summary_fields)
    attr.factors.__fields__(*factor_fields)
    res = oper()
    
    df_summary = pd.DataFrame(data = 
             [(p.date, *[p.percent_return_cumulative.attribution.summary[f] for f in summary_fields]) 
              for p in res.model.simulation.performance],
                              columns = ['date'] + summary_fields)

    factor_data = []
    for p in res.model.simulation.performance:
        for pf in p.percent_return_cumulative.attribution.factors:
            factor_data.append([p.date] + [pf[f] for f in factor_fields])
    df_factors = pd.DataFrame(data = factor_data,
                             columns = ['date'] + factor_fields)
    return df_summary, df_factors

"""Given a list of sedols and a date range, get total,factor,specific, and sector returns in a dataframe.
"""
def get_stock_returns(sedols, start_date, end_date, model_id = DEFAULT_MODEL_ID):
    returns = []

    for sedol in sedols:
        oper = OpOperation(schema.Query)   
        security = oper.model(id=model_id).security(sedol=sedol)
        perf = security.performance(from_ = start_date, to = end_date)
        perf.__fields__()
        perf.percent_price_change_cumulative.__fields__()
        attr = perf.percent_price_change_cumulative.attribution
        attr.summary.__fields__('factors', 'specific')
        attr.factors.__fields__('id', 'name', 'category', 'value')
        res = oper()

        sedol_prices = [(sedol, p.date, p.percent_price_change_cumulative.total, p.percent_price_change_cumulative.attribution.summary.factors,
                  p.percent_price_change_cumulative.attribution.summary.specific, 
                [res.value for res in p.percent_price_change_cumulative.attribution.factors if res.category == 'sector'][0])
                 for p in res.model.security.performance]
        returns = prices + sedol_prices
        
        columns = ['sedol',
'date',
'total_return',
'factor_return',
'specific_return',
'sector_return']

    df_returns = pd.DataFrame(data = [p for p in returns],
                              columns = columns)
    return df_returns


def test():
    print('6')

#res = create_portfolio(name='TestName7', default_model_id='AXUS4-MH')
#print(get_portfolios())
#delete_portfolio('TestName7')
#print(get_portfolios())
