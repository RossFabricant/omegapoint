"""
Basic example of omegapoint usage with input validation.

This example demonstrates:
1. Setting up the environment
2. Creating a portfolio
3. Handling errors using GqlError
4. Using the validation module
"""
import os
from datetime import date
import pandas as pd
from omegapoint import schema, utils, omegapoint as op
from omegapoint.validation import (
    validate_portfolio_name,
    validate_model_id,
    validate_portfolio_positions
)

# Set environment variables
# You would typically set these in your environment rather than in code
# os.environ['OMEGA_POINT_DEFAULT_MODEL_ID'] = 'YOUR_MODEL_ID'
# os.environ['OMEGA_POINT_API_KEY'] = 'YOUR_API_KEY'
# os.environ['OMEGA_POINT_URL'] = 'https://api.ompnt.com/graphql'

# Get available models
available_models = op.get_models()
print("Available models:")
for model in available_models:
    print(f"  - {model.id}")

# Use the first available model or a default
model_id = available_models[0].id if available_models else None
if not model_id:
    print("No models available")
    exit(1)

# Validate the model ID
try:
    validate_model_id(model_id)
except ValueError as e:
    print(f"Invalid model ID: {e}")
    exit(1)

# Try with an invalid model ID to demonstrate error handling
bad_model_id = 'fake'

# Validate portfolio name
portfolio_name = 'Test Portfolio'
try:
    validate_portfolio_name(portfolio_name)
except ValueError as e:
    print(f"Invalid portfolio name: {e}")
    exit(1)

# Use a try-except block to handle GQL errors
try:
    res = op.create_portfolio(name=portfolio_name, default_model_id=bad_model_id)
except op.GqlError as e:
    print(f"GQL error. Query Id is {e.errors['extensions']['queryId']}")
    print(f"Operation is:\n{e.operation}")
    print(f"Error is:\n{e.errors}")

# Now try with the valid model ID
res = op.create_portfolio(name=portfolio_name, default_model_id=model_id)
print(res)

# Check if the portfolio was created
print([p for p in op.get_portfolios() if p.name == portfolio_name])

# Create and validate portfolio data
df = pd.DataFrame([
    {'date': date(2023, 1, 3), 'sedol': '2005973', 'economic_exposure': 1000000},
    {'date': date(2023, 1, 3), 'sedol': 'BYY88Y7', 'economic_exposure': 2000000},
])

try:
    validate_portfolio_positions(df)
    print("Portfolio positions validated successfully")
except ValueError as e:
    print(f"Invalid portfolio positions: {e}")
    exit(1)

# Upload the positions
op.upload_portfolio_positions(portfolio_name, df)
print("Positions uploaded successfully")

# Clean up
op.delete_portfolio(portfolio_name)
print("Portfolio deleted")