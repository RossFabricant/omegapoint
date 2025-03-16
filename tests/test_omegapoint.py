"""Tests for the omegapoint module."""
import pytest
from unittest.mock import patch, MagicMock
from datetime import date
import pandas as pd
from omegapoint import omegapoint as op
from omegapoint import schema

class TestOmegapoint:
    """Test the omegapoint module."""

    @patch('omegapoint.omegapoint.OpOperation.__call__')
    def test_get_models(self, mock_call):
        """Test the get_models function."""
        # Mock the response
        mock_model = MagicMock()
        mock_model.id = 'TEST_MODEL_ID'
        mock_model.name = 'Test Model'
        
        mock_call.return_value = MagicMock()
        mock_call.return_value.models = [mock_model]
        
        # Call the function
        models = op.get_models()
        
        # Check the result
        assert len(models) == 1
        assert models[0].id == 'TEST_MODEL_ID'
        assert models[0].name == 'Test Model'
    
    @patch('omegapoint.omegapoint.OpOperation.__call__')
    @patch('omegapoint.omegapoint.get_portfolios')
    def test_create_portfolio(self, mock_get_portfolios, mock_call):
        """Test the create_portfolio function."""
        # Mock the get_portfolios response
        mock_get_portfolios.return_value = []
        
        # Mock the create_portfolio response
        mock_call.return_value = MagicMock()
        mock_call.return_value.create_portfolio.id = 'TEST_PORTFOLIO_ID'
        
        # Call the function
        portfolio = op.create_portfolio(name='Test Portfolio', default_model_id='TEST_MODEL_ID')
        
        # Check the result
        assert portfolio.id == 'TEST_PORTFOLIO_ID'
    
    @patch('omegapoint.omegapoint.OpOperation.__call__')
    def test_get_portfolios(self, mock_call):
        """Test the get_portfolios function."""
        # Mock the response
        mock_portfolio = MagicMock()
        mock_portfolio.id = 'TEST_PORTFOLIO_ID'
        mock_portfolio.name = 'Test Portfolio'
        
        mock_call.return_value = MagicMock()
        mock_call.return_value.portfolios = [mock_portfolio]
        
        # Call the function
        portfolios = op.get_portfolios()
        
        # Check the result
        assert len(portfolios) == 1
        assert portfolios[0].id == 'TEST_PORTFOLIO_ID'
        assert portfolios[0].name == 'Test Portfolio'
    
    @patch('omegapoint.omegapoint.get_portfolios')
    def test_get_portfolio_id(self, mock_get_portfolios):
        """Test the get_portfolio_id function."""
        # Mock the response
        mock_portfolio = MagicMock()
        mock_portfolio.id = 'TEST_PORTFOLIO_ID'
        mock_portfolio.name = 'Test Portfolio'
        
        mock_get_portfolios.return_value = [mock_portfolio]
        
        # Call the function
        portfolio_id = op.get_portfolio_id('Test Portfolio')
        
        # Check the result
        assert portfolio_id == 'TEST_PORTFOLIO_ID'
    
    @patch('omegapoint.omegapoint.get_portfolios')
    def test_get_portfolio_id_not_found(self, mock_get_portfolios):
        """Test the get_portfolio_id function with a non-existent portfolio."""
        # Mock the response
        mock_get_portfolios.return_value = []
        
        # Call the function and check the exception
        with pytest.raises(RuntimeError, match="There are no portfolios with the name"):
            op.get_portfolio_id('Non-existent Portfolio')