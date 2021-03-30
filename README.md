# omegapoint
This library offers a convenient way to access the Omega Point API from Python. It has 3 components: 

    schema.py. This has Python classes that give full access to the Omega Point GQL API. 
    It is automatically generated from sgqlc. EG: 
    python -m sgqlc.introspection --exclude-deprecated --exclude-description -H "Authorization: SECRET" https://api.ompnt.com/graphql schema.json
    python "C:\Program Files\Python38\Scripts\sgqlc-codegen" schema.json schema.py
    (Anaconda may install your scripts in a directory like C:\Users\%username%\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\Scripts\)
     
    
    omegapoint.py. This has convenience functions that let you perform common operations more
    fluently than you could by using schema.py directly.
    It also defines the class GqlError, which lets you capture Omega Point error messages on failed operations. 
    
    utils.py. This has convenince functions for working with dates and splitting up large API requests.  

There are 3 default values you can set with enviroment variables:
 
#EG: AXWW4-SH
DEFAULT_MODEL_ID = os.getenv('OMEGA_POINT_DEFAULT_MODEL_ID')

#Get this from https://pi.ompnt.com/centerbook_partners/home/platform
API_KEY = os.getenv('OMEGA_POINT_API_KEY')

#https://api.ompnt.com/graphql
URL = os.getenv('OMEGA_POINT_URL')


Here is a quick sample of the code. There are more examples in the examples/ directory.  
```
from omegapoint import schema, utils, omegapoint as op
import pandas as pd
from datetime import date 

available_models = op.get_models()
model_id  = available_models[0].id
bad_model_id = 'fake'

try:
    res = op.create_portfolio(name='OpTest1', default_model_id=bad_model_id)
except op.GqlError as e:
    print(f"GQL error. Query Id is {e.errors['extensions']['queryId']}")
    print(f"Operation is:\n{e.operation}")
    print(f"Error is:\n{e.errors}")

'''
ERROR:sgqlc.endpoint.http:GraphQL query failed with 1 errors
ERROR:sgqlc.endpoint.http:Failed query:
mutation {
  createPortfolio(portfolio: {name: "OpTest1", defaultModelId: "fake"}) {
    id
  }
}

GQL error. Query Id is c5fb462d-653f-4632-a0cf-12557a17573b
Operation is:
mutation {
  createPortfolio(portfolio: {name: "OpTest1", defaultModelId: "fake"}) {
    id
  }
}
Error is:
{'errors': [{'message': 'Access to model fake forbidden', 'locations': [{'line': 2, 'column': 1}], 'path': ['createPortfolio']}], 'data': {'createPortfolio': None}, 'extensions': {'queryId': 'c5fb462d-653f-4632-a0cf-12557a17573b'}}
Portfolio(id=68d1d99a-e0ba-4c3f-9bf5-6a29c155042d)
'''

res = op.create_portfolio(name='OpTest1', default_model_id=model_id)
print(res)
#Portfolio(id=68d1d99a-e0ba-4c3f-9bf5-6a29c155042d)
print([p for p in op.get_portfolios() if p.name == 'OpTest1'])
#[PortfolioMetadata(name='OpTest1', id='68d1d99a-e0ba-4c3f-9bf5-6a29c155042d')]

#There's a file test\port_test.csv in this repo. 
df = pd.read_csv(r'c:\users\ross\omegapoint\test\port_test.csv')
op.upload_portfolio_positions('OpTest1', df)

for dt in utils.weekdays(start = date(2019,11,4), stop = date(2019,11,7)):
    perf = op.get_performance_contributors(portfolio_name = 'OpTest1', start_date = dt, end_date = dt,model_id = model_id)
    print(dt, perf)
'''
2019-11-04      sedol model_provider_id  average_percent_equity     total   factors  \
0  2005973         RM8T7MA55                0.316215  0.004993 -0.000084   
1  BYY88Y7         3U74B69J1                0.683785  0.009464  0.004385   

   specific  trading  
0  0.005077      0.0  
1  0.005079      0.0  

2019-11-05      sedol model_provider_id  average_percent_equity     total   factors  \
0  BYY88Y7         3U74B69J1                0.683369  0.000349 -0.002349   
1  2005973         RM8T7MA55                0.316631  0.000506 -0.001168   

   specific  trading  
0  0.002698      0.0  
1  0.001674      0.0  

2019-11-06      sedol model_provider_id  average_percent_equity     total   factors  \
0  2005973         RM8T7MA55                0.316866  0.002045  0.000241   
1  BYY88Y7         3U74B69J1                0.683134 -0.000122 -0.004280   

   specific  trading  
0  0.001804      0.0  
1  0.004158      0.0  
'''
    
op.delete_portfolio('OpTest1')
```
