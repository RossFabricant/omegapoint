"""Pytest configuration for omegapoint tests."""
import os
import pytest
import pandas as pd
from pathlib import Path

@pytest.fixture(scope='session')
def test_data_dir():
    """Return the path to the test data directory."""
    return Path(__file__).parent.parent / 'omegapoint' / 'test'

@pytest.fixture(scope='session')
def sample_portfolio_data(test_data_dir):
    """Return sample portfolio data for testing."""
    return pd.read_csv(test_data_dir / 'port_test.csv')

@pytest.fixture
def mock_environment(monkeypatch):
    """Mock the environment variables for testing."""
    monkeypatch.setenv('OMEGA_POINT_DEFAULT_MODEL_ID', 'TEST_MODEL_ID')
    monkeypatch.setenv('OMEGA_POINT_API_KEY', 'TEST_API_KEY')
    monkeypatch.setenv('OMEGA_POINT_URL', 'https://test-api.example.com/graphql')