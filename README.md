# omegapoint
This library offers a convenient way to access the Omega Point API from Python. It consists of 3 parts: 
    schema.py. This has Python classes that give full access to the Omega Point GQL API. It is automatically generated from sgqlc. 
    omegapoint.py. This has convenience functions that let you perform common operations more fluently than you could by using schema.py directly.
        It also defines the class GqlError, which lets you capture Omega Point error messages on failed operations. 

There are 3 default values you can set with enviroment variables:
 
DEFAULT_MODEL_ID = os.getenv('OMEGA_POINT_DEFAULT_MODEL_ID')

API_KEY = os.getenv('OMEGA_POINT_API_KEY')

URL = os.getenv('OMEGA_POINT_URL')


Here are some examples of code using the library.

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
    
    print(op.get_portfolios())
    
    #Load a portfolio from CSV 
    import pandas as pd
    from omegapoint import omegapoint as op
    try:
        op.delete_portfolio('rwf_test')
    except: pass
    df = pd.read_csv(r'c:\users\ross\omegapoint\test\port_test.csv')
    op.upload_portfolio_positions('rwf_test', df)
    
    
