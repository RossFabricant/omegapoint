"""
Input validation utilities for the omegapoint library.

This module provides helper functions for validating input parameters
before making API calls to the Omega Point API.
"""
from datetime import date
import pandas as pd
from typing import List, Dict, Any, Optional, Union, Tuple

def validate_date_range(start_date: date, end_date: date) -> None:
    """
    Validate that the start date is before or equal to the end date.
    
    Args:
        start_date: The start date to validate
        end_date: The end date to validate
        
    Raises:
        ValueError: If start_date is after end_date
    """
    if start_date > end_date:
        raise ValueError(f"Start date ({start_date}) must be before or equal to end date ({end_date})")

def validate_portfolio_name(name: str) -> None:
    """
    Validate a portfolio name.
    
    Args:
        name: The portfolio name to validate
        
    Raises:
        ValueError: If name is empty or contains invalid characters
    """
    if not name:
        raise ValueError("Portfolio name cannot be empty")
    
    if len(name) > 100:
        raise ValueError("Portfolio name cannot exceed 100 characters")

def validate_portfolio_positions(df: pd.DataFrame) -> None:
    """
    Validate the format of portfolio positions dataframe.
    
    Args:
        df: DataFrame containing portfolio positions
        
    Raises:
        ValueError: If the dataframe is missing required columns or contains invalid data
    """
    required_columns = ['date']
    id_columns = ['sedol', 'model_provider_id']
    
    # Verify we have date and at least one ID column
    if 'date' not in df.columns:
        raise ValueError("DataFrame must contain a 'date' column")
    
    if not any(col in df.columns for col in id_columns):
        raise ValueError("DataFrame must contain either 'sedol' or 'model_provider_id' column")
    
    if 'economic_exposure' not in df.columns:
        raise ValueError("DataFrame must contain an 'economic_exposure' column")
    
    # Check for NaN values in required columns
    if df['date'].isna().any():
        raise ValueError("DataFrame contains NaN values in 'date' column")
    
    id_col = 'sedol' if 'sedol' in df.columns else 'model_provider_id'
    if df[id_col].isna().any():
        raise ValueError(f"DataFrame contains NaN values in '{id_col}' column")
    
    if df['economic_exposure'].isna().any():
        raise ValueError("DataFrame contains NaN values in 'economic_exposure' column")

def validate_model_id(model_id: str) -> None:
    """
    Validate a model ID.
    
    Args:
        model_id: The model ID to validate
        
    Raises:
        ValueError: If model_id is empty
    """
    if not model_id:
        raise ValueError("Model ID cannot be empty")

def validate_api_key(api_key: str) -> None:
    """
    Validate an API key.
    
    Args:
        api_key: The API key to validate
        
    Raises:
        ValueError: If api_key is empty or malformed
    """
    if not api_key:
        raise ValueError("API key cannot be empty")
    
    # Add additional validation if the API key has a specific format