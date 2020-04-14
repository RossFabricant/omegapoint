# TODO: It's easy to send a single input rather than a list, and you
# get a confusing error. It would be nice to catch this and show a friendly error.
import os
import pandas as pd
from sgqlc.operation import Operation
from omegapoint import schema
from sgqlc.endpoint.http import HTTPEndpoint
import logging

logging.basicConfig()

logger = HTTPEndpoint.logger
DEFAULT_MODEL_ID = os.getenv("OMEGA_POINT_DEFAULT_MODEL_ID")
API_KEY = os.getenv("OMEGA_POINT_API_KEY")
URL = os.getenv("OMEGA_POINT_URL")


class GqlError(Exception):
    def __init__(self, message, errors, operation):
        super().__init__(message)
        self.errors = errors
        self.operation = operation

    def error_list(self):
        return [e["message"] for e in self.errors["errors"]]

    def __str__(self):
        return "\n".join(self.error_list()) + "\n" + self.__repr__()


class OpOperation(Operation):
    def __init__(self, typ=None, name=None, **args):
        super().__init__(typ, name, **args)

    def __call__(self):
        url = URL
        headers = {"Authorization": API_KEY}
        endpoint = HTTPEndpoint(url, headers)
        data = endpoint(self)
        if "errors" in data:
            logger.error(f"Failed query:\n{self}")
            raise GqlError(str(data), data, self)
        return self + data


def set_verbose(is_verbose):
    if is_verbose:
        logger.setLevel("DEBUG")
    else:
        logger.setLevel("INFO")


def create_portfolio(name, default_model_id=DEFAULT_MODEL_ID):
    same_name = [p for p in get_portfolios() if p.name == name]
    if len(same_name) > 0:
        raise RuntimeError(f"There's already a portfolio with name {name}.")
    oper = OpOperation(schema.Mutation)
    port = schema.NewPortfolio(name=name, default_model_id=default_model_id)
    oper.create_portfolio(portfolio=port)
    oper.create_portfolio.__fields__("id")
    return oper().create_portfolio


def get_portfolios(fields=["name", "id"]):
    oper = OpOperation(schema.Query)
    oper.portfolios().__fields__(*fields)
    return oper().portfolios


def get_portfolio_id(name):
    ret = [p.id for p in get_portfolios() if p.name == name]
    if len(ret) == 0:
        raise RuntimeError(f"There are no portfolios with the name %s" % name)
    if len(ret) > 1:
        raise RuntimeError(f"There are multiple portfolios with the name %s" % name)
    return ret[0]


def delete_portfolio(name):
    return delete_portfolio_by_id(get_portfolio_id(name))


def delete_portfolio_by_id(port_id):
    oper = OpOperation(schema.Mutation)
    oper.delete_portfolio(id=port_id).__fields__(ok=True)
    return oper().delete_portfolio


def get_models():
    oper = OpOperation(schema.Query)
    models = oper.models()
    models.__fields__()
    models.availability().__fields__(dates=None)
    return oper().models


def delete_portfolio_positions(name):
    oper = OpOperation(schema.Mutation)
    oper.delete_position_set_dates(portfolio_id=get_portfolio_id(name), all_dates=True)
    return oper()


def update_portfolio(
    port_id,
    alias=None,
    name=None,
    default_model_id=None,
    rollover_position_set_to_current_date=None,
):
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


def upload_portfolio_positions(name, df, nav=None):
    if 'model_provider_id' in df.columns:
        id_type = 'model_provider_id' 
    else:
        id_type = 'sedol'
    if name not in [p.name for p in get_portfolios()]:
        create_portfolio(name)

    port_id = get_portfolio_id(name)
    for date in list(df.date.unique()):
        oper = OpOperation(schema.Mutation)
        equities = [schema.PositionSetEquityInput(
                    id=schema.PositionSetEquityIdInput(**{id_type : r[1][id_type]}),
                    economic_exposure=r[1].economic_exposure
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


# benchmark = [schema.PositionSetInput(id = 'SP500', type='BENCHMARK', weight = 70),
#             schema.PositionSetInput(id = 'Russell3000', type='BENCHMARK', weight = 30)]
# df_summary, df_factors = get_portfolio_performance('Equal Weighted Portfolio', '2020-01-02', '2020-01-15', benchmark)
def get_portfolio_performance(
    name,
    start_date,
    end_date,
    base=None,
    interval=schema.PositionSetInterval.AUTO,
    model_id=DEFAULT_MODEL_ID,
):
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

    factor_data = []
    for p in res.model.simulation.performance:
        for pf in p.percent_return_cumulative.attribution.factors:
            factor_data.append([p.date] + [pf[f] for f in factor_fields])
    df_factors = pd.DataFrame(data=factor_data, columns=["date"] + factor_fields)
    return df_summary, df_factors


"""Given a list of sedol or model provider IDs and a date range, get total,factor,specific, and sector returns in a dataframe."""


def get_stock_returns(id_type, ids, start_date, end_date, model_id=DEFAULT_MODEL_ID):
    returns = []

    for id in ids:
        oper = OpOperation(schema.Query)
        security = oper.model(id=model_id).security(**{id_type : id})
        perf = security.performance(from_=start_date, to=end_date)
        perf.__fields__()
        perf.percent_price_change_cumulative.__fields__()
        attr = perf.percent_price_change_cumulative.attribution
        attr.summary.__fields__("factors", "specific")
        attr.factors.__fields__("id", "name", "category", "value")
        res = oper()

        sedol_returns = [
            (
                sedol,
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
        ]
        columns = [
            "sedol",
            "date",
            "total_return",
            "factor_return",
            "specific_return",
            "sector_return",
        ]

    df_returns = pd.DataFrame(data=sedol_returns, columns=columns)
    return df_returns


"""Omega Point provides cumulative returns. To convert to daily returns requires different formulas for total return and other returns (factor, sector and specific.)
This is explained here: https://support.ompnt.com/en/articles/3804566-simple-performance-attribution-explanation
T1 = Cumulative total return, period 1
T2 = Cumulative total return, period 2
F1 = Cumulative total return, period 1
F2 = Cumulative total return, period 2
t1 = Daily total returns, period 1
t2 = Daily total returns, period 2
f1 = Daily factor returns, period 1
f2 = Daily factor returns, period 2
t1 = T1
t2 = (T2/T1) - 1
f1 = F1
f2 = (F2-F1)/ (1+T1) = f2

"""


def get_daily_total_return(df, col_name="total_return", days_forward=0):
    if days_forward == 0:
        s = (1 + df[col_name]).pct_change(1)
        s[0] = df.at[0, col_name]
    else:
        s = (1 + df[col_name]).pct_change(days_forward).shift(-days_forward)
    return s


"""See note for get_daily_total_return"""


def get_daily_factor_return(df, total_col="total_return", factor_col="factor_return", days_forward=0):
    if days_forward == 0:
        s = ((df.shift(-1)[factor_col] - df[factor_col]) / (1 + df[total_col])).shift(1)
        s[0] = df.at[0, factor_col]
    else:
        s = (df.shift(-days_forward)[factor_col] - df[factor_col]) / (+df[total_col])
    return s


def get_exposure_contributors(portfolio_name, start_date, end_date, model_id=DEFAULT_MODEL_ID):
    oper = OpOperation(schema.Query)
    ec = oper.model(id=model_id).simulation(
        position_set=schema.PositionSetInput(
            id=get_portfolio_id(portfolio_name), type="PORTFOLIO"
        ),
        from_=start_date,
        to=end_date,
    )
    ec.exposure_contributors(equity_id_format='MODEL_PROVIDER_ID').__fields__("date")
    ec.exposure_contributors.contributors.__fields__("sedol", "id", "percent_equity")
    results = oper()
    values = [
        [ec_date.date, ec.sedol, ec.id, ec.percent_equity]
        for ec_date in results.model.simulation.exposure_contributors
        for ec in ec_date.contributors
    ]
    return pd.DataFrame(data=values, columns=["date", "sedol", "model_provider_id", "percent_equity"])


'''
df of (date,sedol,expected_return)
df = pd.DataFrame(data = [[date(2019,12,31), '2005973', .05]], columns = ['date', 'sedol', 'expected_return'])
objective = schema.OptimizationObjective(target_total_risk = 0.07)
constraints = schema.OptimizationConstraints()
try:
    op.delete_portfolio('rwf_test')
except: pass

load_optimized_portfolio(df,'rwf_test', 100e6, 21, objective)
'''
def load_optimized_portfolio(df, portfolio_name, nav, forecast_horizon, objective, 
                             model_id = DEFAULT_MODEL_ID):
    if portfolio_name not in [p.name for p in op.get_portfolios()]:
        op.create_portfolio(portfolio_name)

    errors = []
    for dt in df.date.unique():
        rows = list(row for index, row in df[df.date == dt].iterrows())
        oper = op.OpOperation(schema.Query)   
        long_len = len([r for r in rows if r.expected_return > 0])
        if long_len > 0: long_base = nav / long_len
        short_len = len([r for r in rows if r.expected_return <= 0])
        if short_len > 0: short_base = -nav / short_len
        equities = [schema.PositionSetEquityInput(
        id = schema.PositionSetEquityIdInput(sedol = row.sedol),
        economic_exposure = long_base if row.expected_return > 0 else short_base)
            for row in rows]

        position_set_dates = [schema.PositionSetDateInput(equities=equities, date = dt)] 
        position_set = schema.PositionSetInput(dates = position_set_dates)

        forecast_equities = [schema.ForecastEquityInput
                                 (id = schema.PositionSetEquityIdInput(sedol = row.sedol), 
                                  expected_percent_return = row.expected_return)
                                 for row in rows]
        forecast = schema.ForecastInput(horizon = forecast_horizon, equities = forecast_equities)

        constants = schema.OptimizationConstantsInput(equity = nav)
        optimization = oper.model(id=model_id).optimization(
                position_set = position_set, objective = [objective], constants = constants,
                constraints = constraints, forecast = forecast
        )
        opt_dates = optimization.positions().dates
        opt_dates.date()
        opt_dates.equities().id().sedol()
        opt_dates.equities().__fields__('id', 'economic_exposure')
        results = None
        try:
            results = oper()
        except op.GqlError as gql_err:
            errors.append((dt, gql_err))
        values = [[pos_date.date, equity.id.sedol, equity.economic_exposure]
                  for pos_date in results.model.optimization.positions.dates
                  for equity in pos_date.equities]
        columns = ['date', 'sedol', 'economic_exposure']
        df_pos = pd.DataFrame(data = values, columns = columns)
        upload_portfolio_positions(portfolio_name, df_pos, nav=nav)
    return errors
