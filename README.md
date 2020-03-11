# omegapoint
This library offers a convenient way to access the Omega Point API from Python. It consists of 2 parts: 
    schema from sgqlc 
    omegapoint with specialization


3 default values you can set: 
DEFAULT_MODEL_ID = os.getenv('OMEGA_POINT_DEFAULT_MODEL_ID')
API_KEY = os.getenv('OMEGA_POINT_API_KEY')
URL = os.getenv('OMEGA_POINT_URL')


#This works
print(get_models())    
#This fails
res = create_portfolio(name='RwfTest1', default_model_id='fake')

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

