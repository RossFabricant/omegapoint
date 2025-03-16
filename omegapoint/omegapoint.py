"""
Omega Point API client module.

This module provides convenience functions for interacting with the Omega Point API.
It handles authentication, error handling, and provides a simplified interface
for common operations like portfolio management, performance analysis, and optimization.

Notes:
    - For optimization parameters like maxConcentration, 1.0 means 100%.
    - For maxTrade.percentADV 1.0 means 1%.
    - See examples: https://support.ompnt.com/en/articles/2068051-optimization-graphql-parameters

Environment variables:
    OMEGA_POINT_DEFAULT_MODEL_ID: Default model ID to use (e.g., "AXWW4-SH")
    OMEGA_POINT_API_KEY: API key for authentication
    OMEGA_POINT_URL: API endpoint URL (default: "https://api.ompnt.com/graphql")
"""
import os
import pandas as pd
import numpy as np
from sgqlc.operation import Operation
from omegapoint import schema, utils
from sgqlc.endpoint.http import HTTPEndpoint
import logging
from datetime import date, timedelta
from collections import defaultdict
from typing import List, Dict, Optional, Union, Tuple, Any, Iterator, Callable, Type, TypeVar, cast
from omegapoint.utils import split_dates

logging.basicConfig()

logger = HTTPEndpoint.logger
DEFAULT_MODEL_ID = os.getenv("OMEGA_POINT_DEFAULT_MODEL_ID")
API_KEY = os.getenv("OMEGA_POINT_API_KEY")
URL = os.getenv("OMEGA_POINT_URL")


class GqlError(Exception):
    """Exception raised for errors in GraphQL API responses.
    
    This exception captures the full context of a GraphQL error including the
    original operation that caused the error and the error response from the server.
    
    Attributes:
        errors: The error response from the GraphQL server
        operation: The GraphQL operation that resulted in the error
    """
    def __init__(self, message: str, errors: Dict[str, Any], operation: Operation) -> None:
        """Initialize the GqlError.
        
        Args:
            message: The error message
            errors: The error response from the GraphQL server
            operation: The GraphQL operation that resulted in the error
        """
        super().__init__(message)
        self.errors = errors
        self.operation = operation

    def error_list(self) -> List[str]:
        """Get a list of error messages from the error response.
        
        Returns:
            List of error message strings
        """
        return [e["message"] for e in self.errors["errors"]]

    def __str__(self) -> str:
        """Get a string representation of the error.
        
        Returns:
            Formatted error message with all individual error messages
            and the string representation of the object
        """
        return "\n".join(self.error_list()) + "\n" + self.__repr__()


class OpOperation(Operation):
    """Extended Operation class for Omega Point API operations.
    
    This class wraps sgqlc.operation.Operation to provide automatic
    authentication and error handling for Omega Point API requests.
    """
    def __init__(self, typ: Optional[Any] = None, name: Optional[str] = None, **args: Any) -> None:
        """Initialize an OpOperation.
        
        Args:
            typ: GraphQL operation type (Query or Mutation)
            name: Optional operation name
            **args: Additional arguments to pass to the operation
        """
        super().__init__(typ, name, **args)

    def __call__(self) -> Any:
        """Execute the operation and return the result.
        
        Returns:
            The result of the GraphQL operation
            
        Raises:
            GqlError: If the GraphQL server returns errors
        """
        url = URL
        headers = {"Authorization": API_KEY}
        endpoint = HTTPEndpoint(url, headers)
        data = endpoint(self)
        if "errors" in data:
            logger.error(f"Failed query:\n{self}")
            raise GqlError(str(data), data, self)
        return self + data

    def call(self, get_extensions: bool = False) -> Union[Any, Tuple[Any, List[Any]]]:
        """Execute the operation and optionally return extensions.
        
        Args:
            get_extensions: Whether to return extensions along with the result
            
        Returns:
            Either the operation result or a tuple of (result, extensions)
            
        Raises:
            GqlError: If the GraphQL server returns errors
        """
        if not get_extensions: 
            return self.__call__()
            
        url = URL
        headers = {"Authorization": API_KEY}
        endpoint = HTTPEndpoint(url, headers)
        data = endpoint(self)
        if "errors" in data:
            logger.error(f"Failed query:\n{self}")
            raise GqlError(str(data), data, self)
        extensions = []
        if "extensions" in data:
            extensions = data['extensions']
        return (self + data), extensions


def set_verbose(is_verbose: bool) -> None:
    """Set the verbosity level of the logger.
    
    Args:
        is_verbose: If True, set log level to DEBUG; otherwise, set to INFO
    """
    if is_verbose:
        logger.setLevel("DEBUG")
    else:
        logger.setLevel("INFO")


def create_portfolio(name: str, description: Optional[str] = None, 
                   default_model_id: Optional[str] = DEFAULT_MODEL_ID) -> schema.Portfolio:
    """Create a new portfolio.
    
    Args:
        name: Name of the portfolio to create
        description: Optional description for the portfolio
        default_model_id: Default model ID to use for this portfolio
        
    Returns:
        The created portfolio object
        
    Raises:
        RuntimeError: If a portfolio with the given name already exists
        GqlError: If the GraphQL operation fails
    """
    same_name = [p for p in get_portfolios() if p.name == name]
    if len(same_name) > 0:
        raise RuntimeError(f"There's already a portfolio with name {name}.")
    oper = OpOperation(schema.Mutation)
    port = schema.NewPortfolio(name=name, description=description, default_model_id=default_model_id)
    oper.create_portfolio(portfolio=port)
    oper.create_portfolio.__fields__("id")
    return oper().create_portfolio


def get_portfolios(fields: List[str] = ["name", "id"]) -> List[schema.PortfolioMetadata]:
    """Get a list of all portfolios.
    
    Args:
        fields: List of portfolio fields to return
        
    Returns:
        List of portfolio metadata objects
        
    Raises:
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Query)
    oper.portfolios().__fields__(*fields)
    return oper().portfolios


def get_portfolio_id(name: str) -> str:
    """Get the ID of a portfolio by name.
    
    Args:
        name: Name of the portfolio
        
    Returns:
        Portfolio ID
        
    Raises:
        RuntimeError: If no portfolio with the given name exists
                     or if multiple portfolios with the same name exist
    """
    ret = [p.id for p in get_portfolios() if p.name == name]
    if len(ret) == 0:
        raise RuntimeError(f"There are no portfolios with the name {name}")
    if len(ret) > 1:
        raise RuntimeError(f"There are multiple portfolios with the name {name}")
    return ret[0]


def delete_portfolio(name: str) -> schema.DeletePortfolio:
    """Delete a portfolio by name.
    
    Args:
        name: Name of the portfolio to delete
        
    Returns:
        Delete operation result
        
    Raises:
        RuntimeError: If the portfolio does not exist
        GqlError: If the GraphQL operation fails
    """
    return delete_portfolio_by_id(get_portfolio_id(name))


def delete_portfolio_by_id(port_id: str) -> schema.DeletePortfolio:
    """Delete a portfolio by ID.
    
    Args:
        port_id: ID of the portfolio to delete
        
    Returns:
        Delete operation result
        
    Raises:
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Mutation)
    oper.delete_portfolio(id=port_id).__fields__(ok=True)
    return oper().delete_portfolio


def get_models() -> List[schema.Model]:
    """Get a list of all available models.
    
    Returns:
        List of model objects
        
    Raises:
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Query)
    models = oper.models()
    models.__fields__()
    models.availability().__fields__(dates=None)
    return oper().models


def get_model_availability(model_id: Optional[str] = DEFAULT_MODEL_ID) -> date:
    """Get the current availability date for a model.
    
    Args:
        model_id: ID of the model
        
    Returns:
        Current date available for the model
        
    Raises:
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Query)
    oper.model(id=model_id).availability().current_date()
    return oper().model.availability.current_date


def delete_portfolio_positions(name: str) -> Any:
    """Delete all positions for a portfolio.
    
    Args:
        name: Name of the portfolio
        
    Returns:
        Delete operation result
        
    Raises:
        RuntimeError: If the portfolio does not exist
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Mutation)
    oper.delete_position_set_dates(portfolio_id=get_portfolio_id(name), all_dates=True)
    return oper()


def update_portfolio(
    port_id: str,
    alias: Optional[str] = None,
    name: Optional[str] = None,
    default_model_id: Optional[str] = None,
    rollover_position_set_to_current_date: Optional[bool] = None,
) -> schema.UpdatePortfolio:
    """Update portfolio details.
    
    Args:
        port_id: ID of the portfolio to update
        alias: New alias for the portfolio
        name: New name for the portfolio
        default_model_id: New default model ID
        rollover_position_set_to_current_date: Whether to roll over positions
            to the current date
            
    Returns:
        Updated portfolio object
        
    Raises:
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Mutation)
    pu = schema.PortfolioUpdate()
    if alias is not None:
        pu.__setattr__("alias", alias)
    if name is not None:
        pu.__setattr__("name", name)
    if default_model_id is not None:
        pu.__setattr__("default_model_id", default_model_id)
    if rollover_position_set_to_current_date is not None:
        pu.__setattr__(
            "rollover_position_set_to_current_date",
            rollover_position_set_to_current_date,
        )
    oper.update_portfolio(id=port_id, portfolio=pu).__fields__(id=True)
    return oper().update_portfolio


def upload_portfolio_positions(name: str, df: pd.DataFrame, nav: Optional[float] = None) -> None:
    """Upload positions to a portfolio.
    
    Args:
        name: Name of the portfolio
        df: DataFrame containing position data with columns:
            - date: Date of the positions
            - sedol or model_provider_id: Security identifier
            - economic_exposure: Economic exposure value
        nav: Optional net asset value
        
    Raises:
        RuntimeError: If the portfolio doesn't exist and can't be created
        GqlError: If the GraphQL operation fails
        
    Note:
        If the portfolio doesn't exist, it will be created automatically.
    """
    if "model_provider_id" in df.columns:
        id_type = "model_provider_id"
    else:
        id_type = "sedol"
    if name not in [p.name for p in get_portfolios()]:
        create_portfolio(name)

    port_id = get_portfolio_id(name)
    for date in list(df.date.unique()):
        oper = OpOperation(schema.Mutation)
        equities = [
            schema.PositionSetEquityInput(
                id=schema.PositionSetEquityIdInput(**{id_type: r[1][id_type]}),
                economic_exposure=r[1].economic_exposure,
            )
            for r in df.iterrows()
            if r[1].date == date
        ]
        if nav is not None:
            position_set = schema.PositionSetDateInput(
                date=date, equities=equities, equity=nav
            )
        else:
            position_set = schema.PositionSetDateInput(date=date, equities=equities)
        oper = OpOperation(schema.Mutation)
        oper.upload_position_set_date(portfolio_id=port_id, data=position_set)
        oper()


def df_to_position_set(df: pd.DataFrame) -> schema.PositionSetInput:
    """Convert a DataFrame to a PositionSetInput object.
    
    Args:
        df: DataFrame containing position data with columns:
            - date: Date of the positions
            - sedol: Security identifier
            - economic_exposure: Economic exposure value
            
    Returns:
        PositionSetInput object for use with API operations
        
    Note:
        This function assumes the DataFrame contains sedol identifiers.
        For model_provider_id, you'll need to modify the code.
    """
    dates = []
    for dt in df.date.unique():
        equities = [
            schema.PositionSetEquityInput(
                id=schema.PositionSetEquityIdInput(sedol=row.sedol),
                economic_exposure=row.economic_exposure,
            )
            for _, row in df[df.date==dt].iterrows()
        ]
        dates += [schema.PositionSetDateInput(equities=equities, date=dt)]
    return schema.PositionSetInput(dates=dates)

def get_portfolio_exposure(
    name: str, 
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> List[schema.Exposure]:
    """Get portfolio factor exposures for a date range.
    
    Args:
        name: Portfolio name
        start_date: Start date for the analysis
        end_date: End date for the analysis
        model_id: Model ID to use for the analysis
        
    Returns:
        List of exposure objects for each date in the range
        
    Raises:
        RuntimeError: If the portfolio doesn't exist
        GqlError: If the GraphQL operation fails
        
    Example:
        ```python
        port_name = 'Test Portfolio'
        model_id = 'AXUS4-MH'
        start_date = '2023-01-01'
        end_date = '2023-01-31'
        
        for exposure in op.get_portfolio_exposure(port_name, start_date, end_date, model_id):
            for f in exposure.factors:
                print(exposure.date, f.id, f.z_score)
        ```
    """
    oper = OpOperation(schema.Query)
    port = oper.model(id=model_id).portfolio(id=get_portfolio_id(name))
    exposure = port.exposure(from_=start_date, to=end_date)
    exposure.__fields__()
    exposure.factors().__fields__()
    return oper().model.portfolio.exposure


def get_portfolio_performance(
    name: str,
    start_date: Union[str, date],
    end_date: Union[str, date],
    base: Optional[List[schema.PositionSetInput]] = None,
    interval: schema.PositionSetInterval = schema.PositionSetInterval.POSITION_SET_DATES,
    model_id: Optional[str] = DEFAULT_MODEL_ID,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Get portfolio performance metrics for a date range.
    
    Args:
        name: Portfolio name
        start_date: Start date for the analysis
        end_date: End date for the analysis
        base: Optional list of benchmark position sets (e.g., for comparing against indices)
        interval: The time interval for the analysis
        model_id: Model ID to use for the analysis
        
    Returns:
        Tuple containing:
            - DataFrame with summary performance data (trading, factors, specific, total)
            - DataFrame with detailed factor performance data
            
    Raises:
        RuntimeError: If the portfolio doesn't exist
        GqlError: If the GraphQL operation fails
        
    Example:
        ```python
        # Create benchmark comparison
        benchmark = [
            schema.PositionSetInput(id='SP500', type='BENCHMARK', weight=70),
            schema.PositionSetInput(id='Russell3000', type='BENCHMARK', weight=30)
        ]
        
        # Get performance with benchmark
        df_summary, df_factors = get_portfolio_performance(
            'My Portfolio', 
            '2023-01-01', 
            '2023-01-31', 
            benchmark
        )
        ```
    """
    summary_fields = ["trading", "factors", "specific"]
    factor_fields = ["id", "name", "category", "value"]
    if base is None:
        base = []
    oper = OpOperation(schema.Query)
    model = oper.model(id=model_id)
    port = schema.PositionSetInput(id=get_portfolio_id(name), type="PORTFOLIO")
    model.simulation(
        position_set=port, from_=start_date, to=end_date, base=base, interval=interval
    ).performance.__fields__("date")
    attr = oper.model.simulation.performance.percent_return_cumulative.attribution
    attr.summary.__fields__(*summary_fields)
    attr.factors.__fields__(*factor_fields)
    res = oper()

    df_summary = pd.DataFrame(
        data=[
            (
                p.date,
                *[
                    p.percent_return_cumulative.attribution.summary[f]
                    for f in summary_fields
                ],
            )
            for p in res.model.simulation.performance
        ],
        columns=["date"] + summary_fields,
    )
    # We're given cumulative values but may want daily values.
    df_summary["trading_daily"] = (1 + df_summary.trading).pct_change()
    df_summary.trading_daily.iat[0] = df_summary.trading[0]
    df_summary["factors_daily"] = (1 + df_summary.factors).pct_change()
    df_summary.factors_daily.iat[0] = df_summary.factors[0]
    df_summary["specific_daily"] = (1 + df_summary.specific).pct_change()
    df_summary.specific_daily.iat[0] = df_summary.specific[0]
    df_summary["total"] = df_summary.trading + df_summary.factors + df_summary.specific
    df_summary["total_daily"] = (1 + df_summary.total).pct_change()
    df_summary.total_daily.iat[0] = df_summary.total[0]

    factor_data = []
    for p in res.model.simulation.performance:
        for pf in p.percent_return_cumulative.attribution.factors:
            factor_data.append([p.date] + [pf[f] for f in factor_fields])
    df_factors = pd.DataFrame(data=factor_data, columns=["date"] + factor_fields)
    return df_summary, df_factors


def get_stock_factor_exposure(
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    sedol: str, 
    factor_ids: List[str], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get factor exposures for a single stock over a date range.
    
    Args:
        start_date: Start date for the analysis
        end_date: End date for the analysis
        sedol: Security identifier (SEDOL)
        factor_ids: List of factor IDs to retrieve exposures for
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - date: Date of the exposure
            - factor: Factor ID
            - z_score: Z-score of the factor exposure
            
    Raises:
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Query)
    exposure = oper.model(id=model_id).security(sedol=sedol).exposure(from_=start_date, to=end_date)
    exposure.date()
    exposure.factors(id=factor_ids).__fields__('id', 'z_score')
    res = oper().model.security.exposure
    return pd.DataFrame(data=[(r.date, f.id, f.z_score) for r in res for f in r.factors], 
                        columns=['date', 'factor', 'z_score'])


def get_stock_returns(
    id_type: str, 
    ids: List[str], 
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get performance returns for a list of securities over a date range.
    
    Args:
        id_type: Type of security ID ('sedol' or 'model_provider_id')
        ids: List of security identifiers
        start_date: Start date for the analysis
        end_date: End date for the analysis
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - id_type: Security identifier
            - date: Date of the return
            - total_return: Total return
            - factor_return: Return attributed to factors
            - specific_return: Return attributed to specific risk
            - sector_return: Return attributed to sector exposure
            
    Raises:
        GqlError: If the GraphQL operation fails
    """
    returns = []

    for id in ids:
        oper = OpOperation(schema.Query)
        security = oper.model(id=model_id).security(**{id_type: id})
        perf = security.performance(from_=start_date, to=end_date)
        perf.__fields__()
        perf.percent_price_change_cumulative.__fields__()
        attr = perf.percent_price_change_cumulative.attribution
        attr.summary.__fields__("factors", "specific")
        attr.factors.__fields__("id", "name", "category", "value")
        res = oper()

        id_returns = [
            (
                id,
                p.date,
                p.percent_price_change_cumulative.total,
                p.percent_price_change_cumulative.attribution.summary.factors,
                p.percent_price_change_cumulative.attribution.summary.specific,
                [
                    res.value
                    for res in p.percent_price_change_cumulative.attribution.factors
                    if res.category == "sector"
                ][0],
            )
            for p in res.model.security.performance
            if len(p.percent_price_change_cumulative.attribution.factors) != 0
        ]
        columns = [
            id_type,
            "date",
            "total_return",
            "factor_return",
            "specific_return",
            "sector_return",
        ]
        returns.append(pd.DataFrame(data=id_returns, columns=columns))
    return pd.concat(returns)


def get_stock_factor_returns(
    id_type: str, 
    ids: List[str], 
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    factor_cols: List[str], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get factor return attribution for specific factors across multiple securities.
    
    Args:
        id_type: Type of security ID ('sedol' or 'model_provider_id')
        ids: List of security identifiers
        start_date: Start date for the analysis
        end_date: End date for the analysis
        factor_cols: List of factor IDs to retrieve returns for
        model_id: Model ID to use for the analysis
        
    Returns:
        Pivoted DataFrame with:
            - Rows indexed by date and security ID
            - Columns for each factor ID
            - Values representing factor return attribution
            
    Raises:
        GqlError: If the GraphQL operation fails
        
    Note:
        This function differs from get_stock_returns by providing specific 
        factor-level attribution rather than summary attribution.
    """
    returns = []

    for id in ids:
        oper = OpOperation(schema.Query)
        security = oper.model(id=model_id).security(**{id_type: id})
        perf = security.performance(from_=start_date, to=end_date)
        perf.__fields__()
        perf.percent_price_change_cumulative.__fields__()
        attr = perf.percent_price_change_cumulative.attribution
        attr.factors(id=factor_cols).__fields__("id", "name", "category", "value")
        res = oper()

        id_returns = [
            (id, p.date, f.id, f.value)
            for p in res.model.security.performance
            for f in p.percent_price_change_cumulative.attribution.factors
        ]
        columns = [id_type, "date", "id", "value"]
        returns.append(pd.DataFrame(data=id_returns, columns=columns))
    df = pd.concat(returns)
    return pd.pivot_table(
        df, values="value", index=["date", "sedol"], columns=["id"]
    ).reset_index()


def get_factor_returns(
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    factor_ids: List[str], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get daily returns for a list of factor IDs.
    
    Args:
        start_date: Start date for the analysis
        end_date: End date for the analysis
        factor_ids: List of factor IDs to retrieve returns for
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - id: Factor ID
            - date: Date of the return
            - ret_1d: One-day return percentage
            
    Raises:
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Query)
    factors = oper.model(id=model_id).factors(id=factor_ids)
    factors.__fields__('id', 'name')
    factors.performance(from_=start_date, to=end_date).__fields__(
        'date', 'percent_price_change1_day', 'percent_price_change_cumulative', 'normalized_return')
    res = oper()
    df_factor = pd.DataFrame(data=[(f.id, p.date, p.percent_price_change1_day) 
                                   for f in res.model.factors 
                                   for p in f.performance], 
                             columns=['id', 'date', 'ret_1d'])
    return df_factor
    

def get_factor_performance_attribution(
    portfolio_name: str, 
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    factor_ids: List[str], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get daily and cumulative performance attribution for a list of factors.
    
    Args:
        portfolio_name: Name of the portfolio to analyze
        start_date: Start date for the analysis
        end_date: End date for the analysis
        factor_ids: List of factor IDs to retrieve attribution for
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - date: Date of the attribution
            - id: Factor ID
            - value: Cumulative factor attribution (as a decimal, not percentage)
            - daily_value: Daily factor attribution
            
    Raises:
        RuntimeError: If the portfolio doesn't exist
        GqlError: If the GraphQL operation fails
        
    Note:
        This function adds 1 to the raw attribution values to calculate
        daily returns, then subtracts 1 before returning the final data.
    """
    oper = OpOperation(schema.Query)
    sim = oper.model(id=model_id).simulation(
        position_set=schema.PositionSetInput(
            id=get_portfolio_id(portfolio_name), type="PORTFOLIO"
        ),
        from_=start_date,
        to=end_date,
    )
    performance = sim.performance
    performance.date()
    performance.percent_return_cumulative.attribution.factors(id=factor_ids).__fields__(
        "id", "value"
    )
    results = oper()
    
    df = pd.DataFrame(data=[(p.date, f.id, f.value) 
                            for p in results.model.simulation.performance
                            for f in p.percent_return_cumulative.attribution.factors],
                     columns=['date', 'id', 'value'])
    # Add 1 to convert to return multiplier for calculating daily returns
    df.value = df.value + 1
    df['daily_value'] = df.groupby('id')['value'].pct_change(1)
    # Convert back to percentage 
    df.value = df.value - 1
    return df

def get_factor_exposure(
    df: pd.DataFrame, 
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    factor_ids: List[str], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get factor exposures for a custom portfolio defined by a DataFrame.
    
    Args:
        df: DataFrame containing position data with columns:
            - date: Date of the positions
            - sedol: Security identifier
            - economic_exposure: Economic exposure value
        start_date: Start date for the analysis
        end_date: End date for the analysis
        factor_ids: List of factor IDs to retrieve exposures for
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - date: Date of the exposure
            - id: Factor ID
            - net: Net exposure to the factor
            - long: Long exposure to the factor
            - short: Short exposure to the factor
            
    Raises:
        GqlError: If the GraphQL operation fails
        
    Note:
        This function creates a temporary position set from the provided DataFrame
        and runs a simulation to calculate factor exposures. The position set is not
        stored permanently in the Omega Point system.
    """
    oper = OpOperation(schema.Query)
    sim = oper.model(id=model_id).simulation(
        position_set=df_to_position_set(df),
        from_=start_date,
        to=end_date,
    )
    exposure = sim.exposure
    exposure.date()
    exposure.factors(id=factor_ids).__fields__(
        "id", "net", "long", "short"
    )
    results = oper()
    
    df_result = pd.DataFrame(data=[(e.date, f.id, f.net, f.long, f.short) 
                             for e in results.model.simulation.exposure
                             for f in e.factors],
                      columns=['date', 'id', 'net', 'long', 'short'])
    return df_result



"""
Omega Point provides cumulative returns. To convert to daily returns requires different formulas for total return and other returns (factor, sector and specific).

This is explained here: https://support.ompnt.com/en/articles/3804566-simple-performance-attribution-explanation

Formulas:
    T1 = Cumulative total return, period 1
    T2 = Cumulative total return, period 2
    F1 = Cumulative factor return, period 1
    F2 = Cumulative factor return, period 2
    t1 = Daily total returns, period 1
    t2 = Daily total returns, period 2
    f1 = Daily factor returns, period 1
    f2 = Daily factor returns, period 2
    
    t1 = T1
    t2 = (T2/T1) - 1
    f1 = F1
    f2 = (F2-F1)/ (1+T1)
"""


def get_daily_total_return(
    df: pd.DataFrame, 
    col_name: str = "total_return", 
    days_forward: int = 0, 
    id_col: str = "sedol"
) -> pd.Series:
    """Calculate daily returns from cumulative returns.
    
    Args:
        df: DataFrame containing cumulative returns
        col_name: Column name containing cumulative returns
        days_forward: Number of days to look forward when calculating
            return. Use 0 for standard 1-day returns.
        id_col: Column name to group by (e.g., "sedol")
        
    Returns:
        Series containing daily returns
        
    Note:
        This function temporarily adds 1 to returns to calculate percent changes,
        then restores the original values in the DataFrame.
    """
    df[col_name] = df[col_name] + 1
    if days_forward == 0:
        s = df.groupby(id_col)[col_name].pct_change(1)
    else:
        s = df.groupby(id_col)[col_name].pct_change(days_forward).shift(
            -days_forward
        ) * np.sign(days_forward)
    df[col_name] = df[col_name] - 1
    return s


def get_daily_factor_return(
    df: pd.DataFrame,
    total_col: str = "total_return",
    factor_col: str = "factor_return",
    days_forward: int = 0,
    id_col: str = "sedol",
) -> pd.Series:
    """Calculate daily factor returns from cumulative returns.
    
    Args:
        df: DataFrame containing cumulative returns
        total_col: Column name containing total cumulative returns
        factor_col: Column name containing factor cumulative returns
        days_forward: Number of days to look forward when calculating
            return. Use 0 for standard 1-day returns.
        id_col: Column name to group by (e.g., "sedol")
        
    Returns:
        Series containing daily factor returns
        
    Note:
        Unlike total returns, factor returns require a different formula:
        daily_factor_return = (factor_return_tomorrow - factor_return_today) / (1 + total_return_today)
        This function handles this calculation and replaces any infinite values with NaN.
    """
    if days_forward == 0:
        s = (
            (df.groupby(id_col).shift(-1)[factor_col] - df[factor_col])
            / (1 + df[total_col])
        ).shift(1)
        s[0] = df.at[0, factor_col]
    else:
        df[total_col] = df[total_col] + 1
        s = (
            (df.groupby(id_col).shift(-days_forward)[factor_col] - df[factor_col])
            / (df[total_col])
            * np.sign(days_forward)
        )
        df[total_col] = df[total_col] - 1
    return s.replace([np.inf, -np.inf], np.nan)


def get_exposure_contributors(
    portfolio_name: str, 
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get the exposure contributors for a portfolio.
    
    This function returns the breakdown of portfolio exposure by security,
    showing how much each security contributes to the portfolio's overall
    exposure for each date in the date range.
    
    Args:
        portfolio_name: Name of the portfolio
        start_date: Start date for the analysis
        end_date: End date for the analysis
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - date: Date of the exposure
            - sedol: Security identifier (SEDOL)
            - model_provider_id: Model provider ID for the security
            - percent_equity: Percentage of portfolio equity allocated to this security
            
    Raises:
        RuntimeError: If the portfolio doesn't exist
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Query)
    ec = oper.model(id=model_id).simulation(
        position_set=schema.PositionSetInput(
            id=get_portfolio_id(portfolio_name), type="PORTFOLIO"
        ),
        from_=start_date,
        to=end_date,
    )
    ec.exposure_contributors(equity_id_format="MODEL_PROVIDER_ID").__fields__("date")
    ec.exposure_contributors.contributors.__fields__("sedol", "id", "percent_equity")
    results = oper()
    values = [
        [ec_date.date, ec.sedol, ec.id, ec.percent_equity]
        for ec_date in results.model.simulation.exposure_contributors
        for ec in ec_date.contributors
    ]
    return pd.DataFrame(
        data=values, columns=["date", "sedol", "model_provider_id", "percent_equity"]
    )


def get_performance_contributors(
    portfolio_name: str, 
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get the performance contributors for a portfolio.
    
    This function returns the breakdown of portfolio performance by security,
    showing how much each security contributes to the portfolio's overall
    performance and the attribution of each security's performance to
    factors, specific risk, and trading.
    
    Args:
        portfolio_name: Name of the portfolio
        start_date: Start date for the analysis
        end_date: End date for the analysis
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - sedol: Security identifier (SEDOL)
            - model_provider_id: Model provider ID for the security
            - average_percent_equity: Average percentage of portfolio equity allocated to this security
            - total: Total performance contribution
            - factors: Contribution from factor exposures
            - specific: Contribution from specific risk
            - trading: Contribution from trading
            
    Raises:
        RuntimeError: If the portfolio doesn't exist
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Query)
    sim = oper.model(id=model_id).simulation(
        position_set=schema.PositionSetInput(
            id=get_portfolio_id(portfolio_name), type="PORTFOLIO"
        ),
        from_=start_date,
        to=end_date,
    )
    sim.performance_contributors(equity_id_format="MODEL_PROVIDER_ID").__fields__(
        "id", "sedol", "average_percent_equity", "total"
    )
    sim.performance_contributors.attribution.summary.__fields__(
        "factors", "specific", "trading"
    )
    results = oper()
    values = [
        [
            pc.sedol,
            pc.id,
            pc.average_percent_equity,
            pc.total,
            pc_at.factors,
            pc_at.specific,
            pc_at.trading,
        ]
        for pc in results.model.simulation.performance_contributors
        for pc_at in [pc.attribution.summary]
    ]
    return pd.DataFrame(
        data=values,
        columns=[
            "sedol",
            "model_provider_id",
            "average_percent_equity",
            "total",
            "factors",
            "specific",
            "trading",
        ],
    )


def load_optimized_portfolio(
    df: pd.DataFrame, 
    portfolio_name: str, 
    nav: float, 
    forecast_horizon: int, 
    objective: schema.OptimizationObjective, 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> List[Tuple[date, GqlError]]:
    """Create an optimized portfolio based on expected returns.
    
    This function takes a DataFrame with expected returns for securities,
    creates a basic portfolio with those securities, runs an optimization based
    on the specified objective and constraints, and uploads the optimized
    positions to a portfolio.
    
    Args:
        df: DataFrame with columns:
            - date: Date for the position
            - sedol: Security identifier (SEDOL)
            - expected_return: Expected return for the security
        portfolio_name: Name of the portfolio to create or update
        nav: Net asset value for the portfolio
        forecast_horizon: Forecast horizon in days
        objective: Optimization objective (e.g., target risk, maximize return)
        model_id: Model ID to use for the analysis
        
    Returns:
        List of tuples (date, error) for any optimization errors
        
    Raises:
        GqlError: If any of the GraphQL operations fail
        
    Example:
        ```python
        df = pd.DataFrame(data=[
            [date(2023, 1, 31), '2005973', 0.05],
            [date(2023, 1, 31), 'BYY88Y7', 0.03]
        ], columns=['date', 'sedol', 'expected_return'])
        
        objective = schema.OptimizationObjective(target_total_risk=0.07)
        constraints = schema.OptimizationConstraints()
        
        errors = load_optimized_portfolio(
            df, 'my_optimized_portfolio', 100e6, 21, objective
        )
        ```
    
    Note:
        This function currently only supports sedol identifiers.
        TODO: Add support for model_provider_id.
    """
    if portfolio_name not in [p.name for p in get_portfolios()]:
        create_portfolio(portfolio_name)

    errors = []
    for dt in df.date.unique():
        rows = list(row for index, row in df[df.date == dt].iterrows())
        oper = OpOperation(schema.Query)
        long_len = len([r for r in rows if r.expected_return > 0])
        if long_len > 0:
            long_base = nav / long_len
        short_len = len([r for r in rows if r.expected_return <= 0])
        if short_len > 0:
            short_base = -nav / short_len
        equities = [
            schema.PositionSetEquityInput(
                id=schema.PositionSetEquityIdInput(sedol=row.sedol),
                economic_exposure=long_base if row.expected_return > 0 else short_base,
            )
            for row in rows
        ]

        position_set_dates = [schema.PositionSetDateInput(equities=equities, date=dt)]
        position_set = schema.PositionSetInput(dates=position_set_dates)

        forecast_equities = [
            schema.ForecastEquityInput(
                id=schema.PositionSetEquityIdInput(sedol=row.sedol),
                expected_percent_return=row.expected_return,
            )
            for row in rows
        ]
        forecast = schema.ForecastInput(
            horizon=forecast_horizon, equities=forecast_equities
        )

        constants = schema.OptimizationConstantsInput(equity=nav)
        optimization = oper.model(id=model_id).optimization(
            position_set=position_set,
            objective=[objective],
            constants=constants,
            constraints=schema.OptimizationConstraints(),
            forecast=forecast,
        )
        opt_dates = optimization.positions().dates
        opt_dates.date()
        opt_dates.equities().id().sedol()
        opt_dates.equities().__fields__("id", "economic_exposure")
        results = None
        try:
            results = oper()
        except GqlError as gql_err:
            errors.append((dt, gql_err))
            continue
            
        values = [
            [pos_date.date, equity.id.sedol, equity.economic_exposure]
            for pos_date in results.model.optimization.positions.dates
            for equity in pos_date.equities
        ]
        columns = ["date", "sedol", "economic_exposure"]
        df_pos = pd.DataFrame(data=values, columns=columns)
        upload_portfolio_positions(portfolio_name, df_pos, nav=nav)
    return errors

def get_optimized_weights(
    df: pd.DataFrame, 
    objective: schema.OptimizationObjective, 
    constraints: schema.OptimizationConstraints, 
    constants: schema.OptimizationConstantsInput = schema.OptimizationConstantsInput(), 
    forecast: Optional[schema.ForecastInput] = None, 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get optimized portfolio weights based on position data.
    
    This function takes a DataFrame with position data, runs an optimization
    based on the specified objective, constraints, and forecast, and returns
    a DataFrame with the optimized weights.
    
    Args:
        df: DataFrame with columns:
            - date: Date for the position
            - sedol: Security identifier (SEDOL)
            - economic_exposure: Economic exposure value
        objective: Optimization objective (e.g., minimize_factor_risk=True)
        constraints: Optimization constraints (e.g., max_trade limits)
        constants: Optimization constants (e.g., equity value)
        forecast: Optional forecast information
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with optimized weights with columns:
            - date: Date for the optimized position
            - sedol: Security identifier (SEDOL)
            - economic_exposure: Optimized economic exposure value
        
    Raises:
        GqlError: If any of the GraphQL operations fail
        
    Example:
        ```python
        df = pd.DataFrame(data=[
            [date(2023, 1, 31), '2005973', 1e6], 
            [date(2023, 1, 31), '2588173', 2e6]
        ], columns=['date', 'sedol', 'economic_exposure'])
        
        objective = schema.OptimizationObjective(minimize_factor_risk=True)
        constraints = schema.OptimizationConstraints(
            max_trade=schema.OptimizationMaxTradeConstraint(percent_adv=1.0)
        )
        constants = schema.OptimizationConstantsInput(equity=10e6)
        
        optimized_df = get_optimized_weights(
            df=df, 
            objective=objective, 
            constraints=constraints, 
            constants=constants
        )
        ```
        
    Note:
        The Omega Point API can only optimize 1 date per API call,
        so this function processes each date separately.
    """
    pos_data = []
    # The OP API can only optimize 1 date per API call. 
    for dt in sorted(df.date.unique()):
        position_set = df_to_position_set(df[df.date == dt])
        oper = OpOperation(schema.Query)
        if forecast is None: 
            optimization = oper.model(id=model_id).optimization(
                position_set=position_set,
                objective=[objective],
                constants=constants,
                constraints=constraints
            )
        else: 
            optimization = oper.model(id=model_id).optimization(
                position_set=position_set,
                objective=[objective],
                constants=constants,
                constraints=constraints,
                forecast=forecast
            )            
        opt_dates = optimization.positions().dates
        opt_dates.date()
        opt_dates.equities().id().sedol()
        opt_dates.equities().__fields__("id", "economic_exposure")
        results = oper()
        pos_data += [
            [pos_date.date, equity.id.sedol, equity.economic_exposure]
            for pos_date in results.model.optimization.positions.dates
            for equity in pos_date.equities
        ]
    columns = ["date", "sedol", "economic_exposure"]
    df_pos = pd.DataFrame(data=pos_data, columns=columns)
    return df_pos


def optimize_portfolio(
    portfolio_name: str, 
    dt: Union[str, date], 
    objective: schema.OptimizationObjective, 
    constraints: schema.OptimizationConstraints, 
    constants: schema.OptimizationConstantsInput = schema.OptimizationConstantsInput(), 
    forecast: Optional[schema.ForecastInput] = None, 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Optimize an existing portfolio for a specific date.
    
    This function optimizes an existing portfolio for a specific date based on
    the specified objective, constraints, and optional forecast, and returns
    a DataFrame with the optimized weights.
    
    Args:
        portfolio_name: Name of the portfolio to optimize
        dt: Date for optimization
        objective: Optimization objective (e.g., minimize_factor_risk=True)
        constraints: Optimization constraints (e.g., max_trade limits)
        constants: Optimization constants (e.g., equity value)
        forecast: Optional forecast information
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with optimized weights with columns:
            - date: Date for the optimized position
            - model_provider_id: Model provider ID for the security
            - economic_exposure: Optimized economic exposure value
        
    Raises:
        RuntimeError: If the portfolio doesn't exist
        GqlError: If any of the GraphQL operations fail
        
    Example:
        ```python
        objective = schema.OptimizationObjective(minimize_factor_risk=True)
        constraints = schema.OptimizationConstraints(
            max_trade=schema.OptimizationMaxTradeConstraint(percent_adv=1.0)
        )
        constants = schema.OptimizationConstantsInput(equity=10e6)
        
        optimized_df = optimize_portfolio(
            'my_portfolio',
            date(2023, 1, 31),
            objective,
            constraints,
            constants
        )
        ```
    """
    pos_data = []
    position_set = schema.PositionSetInput(id=get_portfolio_id(portfolio_name), type="PORTFOLIO")
    oper = OpOperation(schema.Query)
    if forecast is None: 
        optimization = oper.model(id=model_id).optimization(
            position_set=position_set,
            objective=[objective],
            constants=constants,
            constraints=constraints,
            on=[dt]
        )
    else: 
        optimization = oper.model(id=model_id).optimization(
            position_set=position_set,
            objective=[objective],
            constants=constants,
            constraints=constraints,
            on=[dt],
            forecast=forecast
        )            
    opt_dates = optimization.positions().dates
    opt_dates.date()
    opt_dates.equities().id().model_provider_id()
    opt_dates.equities().__fields__("id", "economic_exposure")
    results = oper()
    pos_data += [
        [pos_date.date, equity.id.model_provider_id, equity.economic_exposure]
        for pos_date in results.model.optimization.positions.dates
        for equity in pos_date.equities
    ]
    columns = ["date", "model_provider_id", "economic_exposure"]
    df_pos = pd.DataFrame(data=pos_data, columns=columns)
    return df_pos

def get_descriptors(
    dates: List[Union[str, date]], 
    id_type: str, 
    ids: List[str], 
    descriptors: List[str], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get descriptors for securities on specific dates.
    
    Args:
        dates: List of dates to get descriptors for
        id_type: Type of security ID ('sedol' or 'model_provider_id')
        ids: List of security identifiers
        descriptors: List of descriptor names to retrieve
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - id_type: Security identifier
            - date: Date of the descriptors
            - descriptor columns: One column for each requested descriptor
            
    Raises:
        GqlError: If any of the GraphQL operations fail
        
    Example:
        ```python
        descriptors = ['market_cap', 'price', 'volume']
        dates = [date(2023, 1, 31), date(2023, 2, 28)]
        ids = ['2005973', 'BYY88Y7']
        
        df = get_descriptors(dates, 'sedol', ids, descriptors)
        ```
    """
    ret = []

    for id in ids:
        for dt in dates:
            oper = OpOperation(schema.Query)
            oper.model(id=model_id).security(**{id_type: id}).descriptors(
                on=dt
            ).__fields__(*descriptors)
            res = oper()
            ret.append(
                [id, dt] + [res.model.security.descriptors[d] for d in descriptors]
            )
    return pd.DataFrame(data=ret, columns=[id_type, "date"] + descriptors)


def get_security_search(
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    sedols: List[str], 
    security_columns: List[str], 
    factors: Optional[List[str]] = None, 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Search for securities by SEDOL and get their attributes and factor exposures.
    
    Args:
        start_date: Start date for the search
        end_date: End date for the search
        sedols: List of SEDOL identifiers to search for
        security_columns: List of security attributes to retrieve
        factors: Optional list of factor IDs to retrieve exposures for
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - date: Date of the search results
            - security_columns: Requested security attributes
            - factor columns: If factors were requested, one column for each factor
            
    Raises:
        GqlError: If any of the GraphQL operations fail
        
    Note:
        This function automatically adds 'sedol' to security_columns if not present.
        The API returns at most 200 securities per request, so pagination is handled
        automatically.
    """
    if "sedol" not in security_columns:
        security_columns.append("sedol")
    dfs = []
    dates = utils.weekdays(start_date, end_date)
    for dt in dates:
        count_left = -1
        total_count_taken = 0
        while count_left != 0:
            oper = OpOperation(schema.Query)
            filter = schema.SecuritySearchFilter()
            securities = schema.SecuritySearchFilterSecurities(
                in_=[schema.UniversalIdInput(sedol=s) for s in sedols]
            )
            filter.__setattr__("securities", securities)
            security_search = oper.model(id=model_id).security_search(
                on=dt, filter=[filter], take=200, skip=total_count_taken
            )
            security_search.count()
            security_search.securities().__fields__(*security_columns)
            if factors is not None and len(factors) > 0:
                security_search.securities.factor_exposure(id=factors).__fields__(
                    "id", "z_score"
                )
            results = oper()
            if results.model.security_search.securities is None:
                current_count_taken = 0
            else:
                current_count_taken = len(results.model.security_search.securities)
            total_count_taken += current_count_taken
            count_left = total_count_taken - results.model.security_search.count
            if current_count_taken == 0:
                count_left = 0
                break
            if factors is not None and len(factors) > 0:
                data = [
                    [dt]
                    + [getattr(res, s) for s in security_columns]
                    + [fe.z_score for fe in res.factor_exposure]
                    for res in results.model.security_search.securities
                ]
                data_columns = (
                    ["date"]
                    + security_columns
                    + [
                        fe.id
                        for fe in results.model.security_search.securities[
                            0
                        ].factor_exposure
                    ]
                )
            else:
                data = [
                    [dt] + [getattr(res, s) for s in security_columns]
                    for res in results.model.security_search.securities
                ]
                data_columns = ["date"] + security_columns
            dfs.append(pd.DataFrame(data=data, columns=data_columns))
    return pd.concat(dfs)

def etf_security_search(
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    op_id: str, 
    security_columns: List[str], 
    factors: Optional[List[str]] = None, 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Search for ETF constituent securities and get their attributes and factor exposures.
    
    Args:
        start_date: Start date for the search
        end_date: End date for the search
        op_id: ETF identifier in the form of 'ticker.exchange_code' (e.g., 'SPY.ARCX')
        security_columns: List of security attributes to retrieve
        factors: Optional list of factor IDs to retrieve exposures for
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - date: Date of the search results
            - security_columns: Requested security attributes
            - factor columns: If factors were requested, one column for each factor
            
    Raises:
        GqlError: If any of the GraphQL operations fail
        
    Note:
        This function automatically adds 'sedol' to security_columns if not present.
        The API returns at most 200 securities per request, so pagination is handled
        automatically.
        January 1st dates are excluded to avoid common market holidays.
    """
    if "sedol" not in security_columns:
        security_columns.append("sedol")
    dfs = []
    dates = utils.weekdays(start_date, end_date)
    # Skip January 1st dates to avoid common market holidays
    for dt in [d for d in dates if not (d.month == 1 and d.day == 1)]:
        count_left = -1
        total_count_taken = 0
        while count_left != 0:
            oper = OpOperation(schema.Query)
            filter = schema.SecuritySearchFilter()
            universe = [schema.SecuritySearchFilterUniverse(
                type='ETF',
                in_=op_id
            )]
            filter.__setattr__("universe", universe)
            security_search = oper.model(id=model_id).security_search(
                on=dt, filter=[filter], take=200, skip=total_count_taken
            )
            security_search.count()
            security_search.securities().__fields__(*security_columns)
            if factors is not None and len(factors) > 0:
                security_search.securities.factor_exposure(id=factors).__fields__(
                    "id", "z_score"
                )
            results = oper()
            if results.model.security_search.securities is None:
                current_count_taken = 0
            else:
                current_count_taken = len(results.model.security_search.securities)
            total_count_taken += current_count_taken
            count_left = total_count_taken - results.model.security_search.count
            if current_count_taken == 0:
                count_left = 0
                break
            if factors is not None and len(factors) > 0:
                data = [
                    [dt]
                    + [getattr(res, s) for s in security_columns]
                    + [fe.z_score for fe in res.factor_exposure]
                    for res in results.model.security_search.securities
                ]
                data_columns = (
                    ["date"]
                    + security_columns
                    + [
                        fe.id
                        for fe in results.model.security_search.securities[
                            0
                        ].factor_exposure
                    ]
                )
            else:
                data = [
                    [dt] + [getattr(res, s) for s in security_columns]
                    for res in results.model.security_search.securities
                ]
                data_columns = ["date"] + security_columns
            dfs.append(pd.DataFrame(data=data, columns=data_columns))
    return pd.concat(dfs)

def get_composition(
    portfolio_name: str, 
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get portfolio composition data for a date range.
    
    Args:
        portfolio_name: Name of the portfolio
        start_date: Start date for the analysis
        end_date: End date for the analysis
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - date: Date of the composition data
            - gmv: Gross market value
            - reference_equity: Reference equity value
            
    Raises:
        RuntimeError: If the portfolio doesn't exist
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Query)
    oper.model(id=model_id).portfolio(id=get_portfolio_id(portfolio_name)).composition(
        from_=start_date, to=end_date
    ).__fields__("date", "gmv", "reference_equity")
    res = oper()
    return pd.DataFrame(
        data=[
            (r.date, r.gmv, r.reference_equity) for r in res.model.portfolio.composition
        ],
        columns=["date", "gmv", "reference_equity"],
    )


def get_market_impact_date(
    mi_date: Union[str, date], 
    deltas: Dict[str, float], 
    nav: float, 
    denominator: Optional[float] = None, 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Calculate market impact for position changes on a specific date.
    
    Args:
        mi_date: Date for the market impact calculation
        deltas: Dictionary mapping model_provider_id to percentage equity change
        nav: Net asset value for the portfolio
        denominator: Optional value to use as denominator for percentage calculations
            (defaults to nav if not provided)
        model_id: Model ID to use for the analysis
        
    Returns:
        Tuple of DataFrames:
            - Summary DataFrame with total cost and cost percentage
            - Contributor DataFrame with cost breakdown by security
            
    Raises:
        GqlError: If the GraphQL operation fails
        
    Note:
        The deltas should be provided as percentage of equity, not absolute values.
        The function multiplies these percentages by nav to get the actual
        economic exposure changes.
    """
    if denominator is None:
        denominator = nav
    equities = [
        schema.PositionSetEquityInput(
            id=schema.PositionSetEquityIdInput(model_provider_id=id),
            economic_exposure=pct_equity * nav,
        )
        for id, pct_equity in deltas.items()
    ]
    ps_delta = schema.PositionSetDateInput(date=mi_date, equities=equities)
    oper = OpOperation(schema.Query)
    market_impact = (
        oper.model(id=model_id)
        .simulation(position_set=schema.PositionSetInput())
        .market_impact(
            position_set_delta=ps_delta,
            equity_id_format="MODEL_PROVIDER_ID",
            scale_format="DEFAULT",
        )
    )
    market_impact.cost()
    market_impact.contributors().__fields__("id", "cost")
    res = oper()
    total_cost = res.model.simulation.market_impact.cost
    total_cost_pct = total_cost / denominator
    df_total = pd.DataFrame(
        data=[[mi_date, total_cost, total_cost_pct]],
        columns=["date", "total_cost", "total_cost_pct"],
    )

    contributors = [
        (mi_date, c.id, c.cost, c.cost / denominator)
        for c in res.model.simulation.market_impact.contributors
    ]
    df_contrib = pd.DataFrame(
        data=contributors, columns=["date", "model_provider_id", "cost", "cost_pct"]
    )
    return df_total, df_contrib


def get_position_deltas(
    curr_pos: pd.DataFrame, 
    prev_pos: pd.DataFrame
) -> Dict[str, float]:
    """Get the position deltas between two position sets on different dates.
    
    This function calculates the changes in position between two dates,
    including positions that are closed out and new positions that are initiated.
    
    Args:
        curr_pos: DataFrame with current positions, must have columns
            'model_provider_id' and 'percent_equity'
        prev_pos: DataFrame with previous positions, must have columns
            'model_provider_id' and 'percent_equity'
            
    Returns:
        Dictionary mapping model_provider_id to percentage equity change
    """
    dd = defaultdict(lambda: 0)
    deltas = {}
    curr_dict = (
        curr_pos[["model_provider_id", "percent_equity"]]
        .set_index("model_provider_id")
        .to_dict(into=dd)["percent_equity"]
    )
    prev_dict = (
        prev_pos[["model_provider_id", "percent_equity"]]
        .set_index("model_provider_id")
        .to_dict(into=dd)["percent_equity"]
    )
    for id, percent_equity in curr_dict.items():
        deltas[id] = prev_dict[id] - percent_equity
    for id, percent_equity in prev_dict.items():
        if id not in deltas:
            deltas[id] = percent_equity
    return deltas


@split_dates
def get_market_impact(
    portfolio_name: str,
    start_date: Union[str, date],
    end_date: Union[str, date],
    denominator: str = "reference_equity",
    model_id: Optional[str] = DEFAULT_MODEL_ID,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Get market impact for each daily change of a portfolio.
    
    This function calculates the market impact of position changes for each day
    in the date range, in terms of dollars and percent of a denominator
    (either reference_equity or gmv).
    
    Args:
        portfolio_name: Name of the portfolio
        start_date: Start date for the analysis
        end_date: End date for the analysis
        denominator: Column to use as denominator for percentage calculations
            ('reference_equity' or 'gmv')
        model_id: Model ID to use for the analysis
        
    Returns:
        Tuple of DataFrames:
            - Summary DataFrame with total cost and cost percentage for each date
            - Contributor DataFrame with cost breakdown by security for each date
            
    Raises:
        RuntimeError: If the portfolio doesn't exist
        GqlError: If any of the GraphQL operations fail
        
    Note:
        This function ignores changes in position due to price changes and assumes
        all changes are from trading. A more correct approach would be to calculate
        a synthetic position for each day assuming no trading from the prior day,
        and then calculate market impact on the delta from synthetic to actual position.
    """
    prev_date = start_date + timedelta(days=-4)
    df_pos = get_exposure_contributors(portfolio_name, prev_date, end_date)
    df_composition = get_composition(portfolio_name, start_date, end_date)
    nav = df_composition.set_index("date").to_dict()["reference_equity"]
    denominators = df_composition.set_index("date").to_dict()[denominator]

    prev_pos = None
    df_total, df_contrib = None, None
    for dt in [dt for dt in sorted(df_pos.date.unique()) if dt >= start_date]:
        curr_pos = df_pos[df_pos.date == dt]
        if prev_pos is None:
            prev_pos = curr_pos
            continue
        deltas = get_position_deltas(curr_pos, prev_pos)
        total_date, contrib_date = get_market_impact_date(
            dt, deltas, nav[dt], denominators[dt]
        )
        if df_total is None:
            df_total, df_contrib = total_date, contrib_date
        else:
            df_total, df_contrib = (
                pd.concat([df_total, total_date]),
                pd.concat([df_contrib, contrib_date]),
            )
        prev_pos = curr_pos
    return df_total, df_contrib


def get_portfolio_risk_summary(
    portfolio_name: str, 
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get risk summary for a portfolio over a date range.
    
    Args:
        portfolio_name: Name of the portfolio
        start_date: Start date for the analysis
        end_date: End date for the analysis
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - date: Date of the risk data
            - total: Total risk
            - factors: Risk attributed to factor exposures
            - specific: Risk attributed to specific exposures
            
    Raises:
        RuntimeError: If the portfolio doesn't exist
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Query)
    risk = (
        oper.model(id=model_id)
        .portfolio(id=get_portfolio_id(portfolio_name))
        .risk(from_=start_date, to=end_date)
    )
    risk.__fields__("date", "total")
    risk.attribution.summary().__fields__("factors", "specific")
    res = oper()
    return pd.DataFrame(
        data=[
            (
                r.date,
                r.total,
                r.attribution.summary.factors,
                r.attribution.summary.specific,
            )
            for r in res.model.portfolio.risk
        ],
        columns=["date", "total", "factors", "specific"],
    )


def get_portfolio_factor_risk(
    portfolio_name: str, 
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    factors: List[str], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get factor risk breakdown for a portfolio over a date range.
    
    Args:
        portfolio_name: Name of the portfolio
        start_date: Start date for the analysis
        end_date: End date for the analysis
        factors: List of factor IDs to retrieve risk for
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - date: Date of the risk data
            - id: Factor ID
            - name: Factor name
            - category: Factor category
            - value: Risk value attributed to the factor
            
    Raises:
        RuntimeError: If the portfolio doesn't exist
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Query)
    risk = (
        oper.model(id=model_id)
        .portfolio(id=get_portfolio_id(portfolio_name))
        .risk(from_=start_date, to=end_date)
    )
    risk.__fields__("date", "total")
    risk.attribution.factors(id=factors).__fields__("id", "name", "category", "value")
    res = oper()
    return pd.DataFrame(
        data=[
            (r.date, rf.id, rf.name, rf.category, rf.value)
            for r in res.model.portfolio.risk
            for rf in r.attribution.factors
        ],
        columns=["date", "id", "name", "category", "value"],
    )


def get_total_risk(
    id: str, 
    id_type: str, 
    start_date: Union[str, date], 
    end_date: Union[str, date], 
    model_id: Optional[str] = DEFAULT_MODEL_ID
) -> pd.DataFrame:
    """Get total risk for a security over a date range.
    
    Args:
        id: Security identifier
        id_type: Type of identifier ('sedol' or 'model_provider_id')
        start_date: Start date for the analysis
        end_date: End date for the analysis
        model_id: Model ID to use for the analysis
        
    Returns:
        DataFrame with columns:
            - date: Date of the risk data
            - total: Total risk value
            
    Raises:
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Query)
    oper.model(id=model_id).security(**{id_type: id}).risk(
        from_=start_date, to=end_date
    ).__fields__("date", "total")
    res = oper()
    return pd.DataFrame(
        data=[(r.date, r.total) for r in res.model.security.risk],
        columns=["date", "total"],
    )


def create_watchlist(name: str) -> Any:
    """Create a new watchlist.
    
    Args:
        name: Name for the new watchlist
        
    Returns:
        Result of the create watchlist operation
        
    Raises:
        GqlError: If the GraphQL operation fails (e.g., if a watchlist with the same name already exists)
    """
    oper = OpOperation(schema.Mutation)
    oper.create_watchlist(name=name)
    res = oper()
    return res


def get_watchlist_id(name: str) -> str:
    """Get the ID of a watchlist by name.
    
    Args:
        name: Name of the watchlist
        
    Returns:
        Watchlist ID
        
    Raises:
        IndexError: If no watchlist with the given name exists
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Query)
    oper.watchlists().__fields__("name", "id")
    res = oper()
    return [w.id for w in res.watchlists if w.name == name][0]


def add_watchlist_securities(name: str, id_type: str, ids: List[str]) -> None:
    """Add securities to a watchlist.
    
    Args:
        name: Name of the watchlist
        id_type: Type of identifier ('sedol' or 'model_provider_id')
        ids: List of security identifiers to add
        
    Raises:
        IndexError: If no watchlist with the given name exists
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Mutation)
    equities = [schema.PositionSetEquityIdInput(**{id_type: id}) for id in ids]
    securities = schema.WatchlistSecuritiesInput(equities=equities)
    oper.add_watchlist_securities(
        watchlist_id=get_watchlist_id(name), securities=securities
    )
    oper()


def clear_watchlist_securities(name: str) -> Any:
    """Remove all securities from a watchlist.
    
    Args:
        name: Name of the watchlist
        
    Returns:
        Result of the clear watchlist securities operation
        
    Raises:
        IndexError: If no watchlist with the given name exists
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Mutation)
    oper.clear_watchlist_securities(watchlist_id=get_watchlist_id(name))
    return oper()

# CRUD operations for Forecasts
def create_forecast(name: str) -> str:
    """Create a new forecast.
    
    Args:
        name: Name for the new forecast
        
    Returns:
        ID of the created forecast
        
    Raises:
        GqlError: If the GraphQL operation fails (e.g., if a forecast with the same name already exists)
    """
    oper = OpOperation(schema.Mutation)
    oper.create_forecast(forecast=schema.ForecastCreate(name=name)).id()
    return oper().create_forecast.id


def get_forecast_id(forecast_name: str) -> str:
    """Get the ID of a forecast by name.
    
    Args:
        forecast_name: Name of the forecast
        
    Returns:
        Forecast ID
        
    Raises:
        RuntimeError: If no forecast with the given name exists or if multiple forecasts with the same name exist
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Query)
    oper.forecasts().__fields__('id', 'name')
    ret = [f.id for f in oper().forecasts if f.name == forecast_name]
    if len(ret) == 0:
        raise RuntimeError(f"There are no forecasts with the name {forecast_name}")
    if len(ret) > 1:
        raise RuntimeError(f"There are multiple forecasts with the name {forecast_name}")
    return ret[0]


def delete_forecast(name: str) -> Any:
    """Delete a forecast by name.
    
    Args:
        name: Name of the forecast to delete
        
    Returns:
        Result of the delete forecast operation
        
    Raises:
        RuntimeError: If no forecast with the given name exists
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Mutation)
    oper.delete_forecast(id=get_forecast_id(name))
    return oper()


def upload_forecast_securities(forecast_name: str, df_forecast: pd.DataFrame) -> Any:
    """Upload security forecasts to a named forecast.
    
    Args:
        forecast_name: Name of the forecast to upload to
        df_forecast: DataFrame with columns:
            - sedol: Security identifier (SEDOL)
            - date: Date of the forecast
            - expected_return: Expected return value
            - horizon: Forecast horizon in days
            
    Returns:
        Result of the upload forecast securities operation
        
    Raises:
        RuntimeError: If no forecast with the given name exists
        GqlError: If the GraphQL operation fails
    """
    oper = OpOperation(schema.Mutation)
    forecast_values = [
        schema.ForecastSecurityInput(
            id=schema.UniversalIdInput(sedol=row.sedol),
            as_of=row.date, 
            expected_return=schema.ForecastExpectedReturnInput(
                return_=row.expected_return, 
                horizon=row.horizon
            )
        )
        for _, row in df_forecast.iterrows()
    ]
    oper.upload_forecast_securities(id=get_forecast_id(forecast_name), values=forecast_values)
    return oper()
