"""
Comprehensive example demonstrating portfolio analysis using omegapoint.

This example shows how to:
1. Create a portfolio
2. Upload positions
3. Get performance attribution
4. Analyze factor exposure
5. Clean up by deleting the portfolio
"""
import os
import pandas as pd
from datetime import date, timedelta
from omegapoint import schema, utils, omegapoint as op
from omegapoint.validation import validate_portfolio_positions

def main():
    # Set up environment variables if not already set
    if not os.getenv('OMEGA_POINT_API_KEY'):
        print("Please set OMEGA_POINT_API_KEY environment variable")
        return
    
    if not os.getenv('OMEGA_POINT_DEFAULT_MODEL_ID'):
        print("Please set OMEGA_POINT_DEFAULT_MODEL_ID environment variable")
        return
    
    if not os.getenv('OMEGA_POINT_URL'):
        os.environ['OMEGA_POINT_URL'] = "https://api.ompnt.com/graphql"
    
    # Turn on verbose logging
    op.set_verbose(True)
    
    # Get available models
    print("Available models:")
    available_models = op.get_models()
    for model in available_models:
        print(f"  - {model.id}")
    
    # Use the first available model
    model_id = available_models[0].id
    
    # Portfolio name for this example
    portfolio_name = "ExamplePortfolio"
    
    # Try to create portfolio (will fail if it already exists)
    try:
        portfolio = op.create_portfolio(name=portfolio_name, default_model_id=model_id)
        print(f"Created portfolio: {portfolio.id}")
    except RuntimeError as e:
        print(f"Portfolio already exists: {e}")
        # Get the existing portfolio ID
        portfolio_id = op.get_portfolio_id(portfolio_name)
        print(f"Using existing portfolio: {portfolio_id}")
    
    # Sample portfolio data
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    # Create sample portfolio data
    portfolio_data = pd.DataFrame([
        {'date': yesterday, 'sedol': '2005973', 'economic_exposure': 1000000},
        {'date': yesterday, 'sedol': 'BYY88Y7', 'economic_exposure': 2000000},
        {'date': today, 'sedol': '2005973', 'economic_exposure': 1200000},
        {'date': today, 'sedol': 'BYY88Y7', 'economic_exposure': 1800000},
    ])
    
    # Validate the portfolio data
    validate_portfolio_positions(portfolio_data)
    
    # Upload positions
    print(f"Uploading positions for {portfolio_name}...")
    op.upload_portfolio_positions(portfolio_name, portfolio_data)
    
    # Get portfolio performance
    print(f"Getting performance for {portfolio_name}...")
    try:
        summary_df, factors_df = op.get_portfolio_performance(
            portfolio_name, 
            yesterday, 
            today, 
            model_id=model_id
        )
        
        print("\nPerformance Summary:")
        print(summary_df)
        
        print("\nFactor Performance:")
        print(factors_df)
    except Exception as e:
        print(f"Error getting performance: {e}")
    
    # Get exposure
    print(f"\nGetting exposure for {portfolio_name}...")
    try:
        exposures = op.get_portfolio_exposure(
            portfolio_name,
            yesterday,
            today,
            model_id=model_id
        )
        
        for exposure in exposures:
            print(f"Exposure on {exposure.date}:")
            for factor in exposure.factors:
                print(f"  - {factor.id}: {factor.z_score}")
    except Exception as e:
        print(f"Error getting exposure: {e}")
    
    # Get risk
    print(f"\nGetting risk summary for {portfolio_name}...")
    try:
        risk_df = op.get_portfolio_risk_summary(
            portfolio_name,
            yesterday,
            today,
            model_id=model_id
        )
        
        print("\nRisk Summary:")
        print(risk_df)
    except Exception as e:
        print(f"Error getting risk: {e}")
    
    # Clean up - uncomment to delete the portfolio
    # print(f"\nDeleting portfolio {portfolio_name}...")
    # op.delete_portfolio(portfolio_name)
    # print("Portfolio deleted")
    
    print("\nExample completed successfully")

if __name__ == "__main__":
    main()