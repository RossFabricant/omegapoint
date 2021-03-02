#Note: For optimization parameters like maxConcentration, 1.0 means 100%.
#For maxTrade.percentADV 1.0 means 1%. 
#See here for examples: https://support.ompnt.com/en/articles/2068051-optimization-graphql-parameters 
import os
import pandas as pd
import numpy as np
from sgqlc.operation import Operation
from omegapoint import schema, utils
from sgqlc.endpoint.http import HTTPEndpoint
import logging
from datetime import timedelta
from collections import defaultdict
from omegapoint.utils import split_dates

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

    def call(self, get_extensions = False):
        if not get_extensions: return __call__()
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

def set_verbose(is_verbose):
    if is_verbose:
        logger.setLevel("DEBUG")
    else:
        logger.setLevel("INFO")


def create_portfolio(name, description = None,default_model_id=DEFAULT_MODEL_ID):
    same_name = [p for p in get_portfolios() if p.name == name]
    if len(same_name) > 0:
        raise RuntimeError(f"There's already a portfolio with name {name}.")
    oper = OpOperation(schema.Mutation)
    port = schema.NewPortfolio(name=name, description = description, default_model_id=default_model_id)
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

def get_model_availability(model_id=DEFAULT_MODEL_ID):
    oper = OpOperation(schema.Query)
    oper.model(id=model_id).availability().current_date()
    return oper().model.availability.current_date

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

'''df is a pd.DataFrame(sedol, economic_exposure)'''
def df_to_position_set(df : pd.DataFrame):
    dates = []
    for dt in df.date.unique():
        equities = [
        schema.PositionSetEquityInput(
            id=schema.PositionSetEquityIdInput(sedol=row.sedol),
            economic_exposure=row.economic_exposure,
        )
        for _, row in df[df.date==dt].iterrows()
    ]
        dates +=[schema.PositionSetDateInput(equities=equities, date=dt)]
    return schema.PositionSetInput(dates=dates)

"""
port_name = 'Test Name'
model_id = 'AXUS4-MH'
start_date = '2018-12-31'
end_date = '2020-01-09'

for exposure in op.get_portfolio_exposure(port_name, start_date, end_date, model_id):
    for f in exposure.factors:
        print(exposure.date, f)
"""


def get_portfolio_exposure(name, start_date, end_date, model_id=DEFAULT_MODEL_ID):
    oper = OpOperation(schema.Query)
    port = oper.model(id=model_id).portfolio(id=get_portfolio_id(name))
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


def get_stock_factor_exposure(start_date, end_date, sedol, factor_ids, model_id = DEFAULT_MODEL_ID):
    '''For a single stock, get factor exposure for a date range.'''
    oper = OpOperation(schema.Query)
    exposure = oper.model(id=model_id).security(sedol=sedol).exposure(from_ = start_date, to = end_date)
    exposure.date()
    exposure.factors(id=factor_ids).__fields__('id', 'z_score')
    res = oper().model.security.exposure
    return pd.DataFrame(data=[(r.date, f.id, f.z_score) for r in res for f in r.factors], 
                        columns = ['date', 'factor', 'z_score'])

"""Given a list of sedol or model provider IDs and a date range, get total,factor,specific, and sector returns in a dataframe."""


def get_stock_returns(id_type, ids, start_date, end_date, model_id=DEFAULT_MODEL_ID):
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


# factor_cols is a list of factor ids, this returns return attribution for those factors.
def get_stock_factor_returns(
    id_type, ids, start_date, end_date, factor_cols, model_id=DEFAULT_MODEL_ID
):
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


"""Get daily returns for a list of factor ids."""
def get_factor_returns(start_date, end_date, factor_ids, model_id = DEFAULT_MODEL_ID):
    oper = OpOperation(schema.Query)
    factors = oper.model(id = model_id).factors(id = factor_ids)
    factors.__fields__('id', 'name')
    factors.performance(from_ = start_date, to = end_date).__fields__(
        'date', 'percent_price_change1_day','percent_price_change_cumulative', 'normalized_return')
    res = oper()
    df_factor = pd.DataFrame(data = [(f.id, p.date, p.percent_price_change1_day) 
                                     for f in res.model.factors 
                                     for p in f.performance], 
                             columns = ['id', 'date', 'ret_1d'])
    return df_factor
    
"""Get daily and cumulative performance attribution for a list of factors."""
def get_factor_performance_attribution(portfolio_name, start_date, end_date, factor_ids, model_id = DEFAULT_MODEL_ID):
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
    performance.percent_return_cumulative.attribution.factors(id=factor_ids) .__fields__(
        "id", "value"
    )
    results = oper()
    results
    df = pd.DataFrame(data = [(p.date, f.id, f.value) 
                              for p in results.model.simulation.performance
                              for f in p.percent_return_cumulative.attribution.factors],
                      columns = ['date', 'id', 'value'])
    df.value = df.value + 1
    df['daily_value'] = df.groupby('id')['value'].pct_change(1)
    df.value = df.value - 1
    return df 

"""Get the factor exposure for a DataFrame of (date, sedol, economicExposure)"""
def get_factor_exposure(df, start_date, end_date, factor_ids, model_id = DEFAULT_MODEL_ID):
    oper = OpOperation(schema.Query)
    sim = oper.model(id=model_id).simulation(
        position_set=df_to_position_set(df),
        from_=start_date,
        to=end_date,
    )
    exposure = sim.exposure
    exposure.date()
    exposure.factors(id=factor_ids) .__fields__(
        "id", "net", "long", "short"
    )
    results = oper()
    results
    df = pd.DataFrame(data = [(e.date, f.id, f.net, f.long, f.short) 
                                for e in results.model.simulation.exposure
                                for f in e.factors],
                      columns = ['date', 'id', 'net', 'long', 'short'])
    return df



"""Omega Point provides cumulative returns. To convert to daily returns requires different formulas for total return and other returns (factor, sector and specific.)
This is explained here: https://support.ompnt.com/en/articles/3804566-simple-performance-attribution-explanation
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


def get_daily_total_return(df, col_name="total_return", days_forward=0, id_col="sedol"):
    df[col_name] = df[col_name] + 1
    if days_forward == 0:
        s = df.groupby(id_col)[col_name].pct_change(1)
    else:
        s = df.groupby(id_col)[col_name].pct_change(days_forward).shift(
            -days_forward
        ) * np.sign(days_forward)
    df[col_name] = df[col_name] - 1
    return s


"""See note for get_daily_total_return"""


def get_daily_factor_return(
    df,
    total_col="total_return",
    factor_col="factor_return",
    days_forward=0,
    id_col="sedol",
):
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
    portfolio_name, start_date, end_date, model_id=DEFAULT_MODEL_ID
):
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
    portfolio_name, start_date, end_date, model_id=DEFAULT_MODEL_ID
):
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


"""
df of (date,sedol,expected_return)
df = pd.DataFrame(data = [[date(2019,12,31), '2005973', .05]], columns = ['date', 'sedol', 'expected_return'])
objective = schema.OptimizationObjective(target_total_risk = 0.07)
constraints = schema.OptimizationConstraints()
try:
    op.delete_portfolio('rwf_test')
except: pass

load_optimized_portfolio(df,'rwf_test', 100e6, 21, objective)
"""
# TODO support model_provider_id
def load_optimized_portfolio(
    df, portfolio_name, nav, forecast_horizon, objective, model_id=DEFAULT_MODEL_ID
):
    if portfolio_name not in [p.name for p in op.get_portfolios()]:
        op.create_portfolio(portfolio_name)

    errors = []
    for dt in df.date.unique():
        rows = list(row for index, row in df[df.date == dt].iterrows())
        oper = op.OpOperation(schema.Query)
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
            constraints=constraints,
            forecast=forecast,
        )
        opt_dates = optimization.positions().dates
        opt_dates.date()
        opt_dates.equities().id().sedol()
        opt_dates.equities().__fields__("id", "economic_exposure")
        results = None
        try:
            results = oper()
        except op.GqlError as gql_err:
            errors.append((dt, gql_err))
        values = [
            [pos_date.date, equity.id.sedol, equity.economic_exposure]
            for pos_date in results.model.optimization.positions.dates
            for equity in pos_date.equities
        ]
        columns = ["date", "sedol", "economic_exposure"]
        df_pos = pd.DataFrame(data=values, columns=columns)
        upload_portfolio_positions(portfolio_name, df_pos, nav=nav)
    return errors

'''df is a DataFrame(date,sedol, economic_exposure)
EG 
df = pd.DataFrame(data = [[date(2014,1,3), '2005973', 1e6], [date(2014,1,3), '2588173', 2e6],
                         [date(2014,1,6), '2005973', 2e6], [date(2014,1,6), '2588173', 4e6]],
                         columns = ['date', 'sedol', 'economic_exposure'])
objective=schema.OptimizationObjective(minimize_factor_risk = True)
constraints = schema.OptimizationConstraints(
    max_trade = schema.OptimizationMaxTradeConstraint(percent_adv=1.0))
constants = schema.OptimizationConstantsInput(equity=nav)

op.get_optimized_weights(df = df, objective = objective, constraints = constraints, constants = constants)


'''
def get_optimized_weights(
    df, objective, constraints, constants = schema.OptimizationConstantsInput(), forecast = None, model_id=DEFAULT_MODEL_ID
):
    pos_data = []
    #The OP API can only optimize 1 date per API call. 
    for dt in sorted(df.date.unique()):
        print(dt)
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
                forecast = forecast
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

def get_descriptors(dates, id_type, ids, descriptors, model_id=DEFAULT_MODEL_ID):
    ret = []

    for id in ids:
        print(id)
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
    start_date, end_date, sedols, security_columns, factors, model_id=DEFAULT_MODEL_ID
):
    if "sedol" not in security_columns:
        security_columns.append("sedol")
    dfs = []
    dates = utils.weekdays(start_date, end_date)
    for dt in dates:
        print(dt)
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

'''Use the security search API to get values for ETF members for a date range. op_id is in the form ticker.exchange code, EG SPY.ARCX or IWB.ARCX'''
def etf_security_search(
    start_date, end_date, op_id, security_columns, factors, model_id=DEFAULT_MODEL_ID
):
    if "sedol" not in security_columns:
        security_columns.append("sedol")
    dfs = []
    dates = utils.weekdays(start_date, end_date)
    for dt in [d for d in dates if not (d.month == 1 and d.day == 1)]:
        print(dt)
        count_left = -1
        total_count_taken = 0
        while count_left != 0:
            oper = OpOperation(schema.Query)
            filter = schema.SecuritySearchFilter()
            universe = [schema.SecuritySearchFilterUniverse(
                type = 'ETF',
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



def get_composition(portfolio_name, start_date, end_date, model_id=DEFAULT_MODEL_ID):
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
    mi_date, deltas, nav, denominator=None, model_id=DEFAULT_MODEL_ID
):
    if denominator == None:
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


def get_position_deltas(curr_pos, prev_pos):
    """Get the position deltas between 2 position sets on 2 different dates. Include positions that are closed out and initiated.
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
    portfolio_name,
    start_date,
    end_date,
    denominator="reference_equity",
    model_id=DEFAULT_MODEL_ID,
):
    """Get market impact for each daily change of a portfolio in terms of dollars and percent of a denominator, either reference_equity or gmv.
    Note that this ignores changes in position due to price changes, and assumes all changes are from trading and calculates market impact on that basis. 
    A more correct approach would be to calculate a synthetic position for each day assuming no trading from the prior day, and then calculate market impact
    on the delta from synthetic to actual position. 
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
    portfolio_name, start_date, end_date, model_id=DEFAULT_MODEL_ID
):
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
    portfolio_name, start_date, end_date, factors, model_id=DEFAULT_MODEL_ID
):
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


def get_total_risk(id, id_type, start_date, end_date, model_id=DEFAULT_MODEL_ID):
    oper = OpOperation(schema.Query)
    oper.model(id=model_id).security(**{id_type: id}).risk(
        from_=start_date, to=end_date
    ).__fields__("date", "total")
    res = oper()
    return pd.DataFrame(
        data=[(r.date, r.total) for r in res.model.security.risk],
        columns=["date", "total"],
    )


def create_watchlist(name):
    oper = OpOperation(schema.Mutation)
    oper.create_watchlist(name=name)
    res = oper()
    return res


def get_watchlist_id(name):
    oper = OpOperation(schema.Query)
    oper.watchlists().__fields__("name", "id")
    res = oper()
    return [w.id for w in res.watchlists if w.name == name][0]


def add_watchlist_securities(name, id_type, ids):
    oper = OpOperation(schema.Mutation)
    equities = [schema.PositionSetEquityIdInput(**{id_type: id}) for id in ids]
    securities = schema.WatchlistSecuritiesInput(equities=equities)
    oper.add_watchlist_securities(
        watchlist_id=get_watchlist_id(name), securities=securities
    )
    oper()


def clear_watchlist_securities(name):
    oper = OpOperation(schema.Mutation)
    oper.clear_watchlist_securities(watchlist_id=get_watchlist_id(name))
    return oper()

#CRUD for Forecasts
def create_forecast(name):
    oper = OpOperation(schema.Mutation)
    oper.create_forecast(forecast = schema.ForecastCreate(name = name)).id()
    return oper().create_forecast.id

def get_forecast_id(forecast_name):
    oper = OpOperation(schema.Query)
    oper.forecasts().__fields__('id', 'name')
    ret = [f.id for f in oper().forecasts if f.name == forecast_name]
    if len(ret) == 0:
        raise RuntimeError(f"There are no forecasts with the name %s" % forecast_name)
    if len(ret) > 1:
        raise RuntimeError(f"There are multiple forecasts with the name %s" % forecast_name)
    return ret[0]

def delete_forecast(name):
    oper = OpOperation(schema.Mutation)
    oper.delete_forecast(id = get_forecast_id(name))
    return oper()

def upload_forecast_securities(forecast_name, df_forecast):
    '''expects dataframe of (sedol, date, expected_return, horizon)'''
    oper = OpOperation(schema.Mutation)
    forecast_values = [schema.ForecastSecurityInput(
        id = schema.UniversalIdInput(sedol= row.sedol),
        as_of = row.date, 
        expected_return = schema.ForecastExpectedReturnInput(return_ = row.expected_return, horizon = row.horizon))
                  for _, row in df_forecast.iterrows()
                  ]
    oper.upload_forecast_securities(id = get_forecast_id(forecast_name), values = forecast_values)
    return oper()
