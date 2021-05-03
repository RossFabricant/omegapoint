import sgqlc.types
import sgqlc.types.datetime


schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
class ActiveContributorType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('WEIGHT', 'EXPOSURE')


class Aggregation(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('LAST',)


class BetaType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('PREDICTED', 'HISTORICAL')


Boolean = sgqlc.types.Boolean

class CompositionConstraintType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('CLASSIFICATION', 'SECTOR', 'INDUSTRY_GROUP', 'INDUSTRY', 'CURRENCY', 'COUNTRY')


class ContributorGroupType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('SECTOR', 'INDUSTRY_GROUP', 'INDUSTRY', 'CLASSIFICATION', 'CURRENCY', 'COUNTRY', 'LONG_SHORT')


class Cusip(sgqlc.types.Scalar):
    __schema__ = schema


Date = sgqlc.types.datetime.Date

DateTime = sgqlc.types.datetime.DateTime

class Descriptor(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('ASSET_CLASS', 'COUNTRY', 'CURRENCY', 'AVERAGE_DAILY_VOLUME', 'SECTOR', 'MARKET_CAPITALIZATION')


class EquityIdFormat(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('SEDOL', 'MODEL_PROVIDER_ID', 'ISIN', 'CUSIP')


class ExperimentType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('SIMULATION', 'PORTFOLIO', 'OPTIMIZATION', 'SMART_TRADE')


Float = sgqlc.types.Float

class ImpliedReturnsType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('MARKET',)


class IndustryClassificationType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('SECTOR', 'INDUSTRY_GROUP', 'INDUSTRY')


Int = sgqlc.types.Int

class Interval(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('END_DATE', 'WEEKLY_START_DATES', 'MONTHLY_START_DATES', 'AUTO')


class Isin(sgqlc.types.Scalar):
    __schema__ = schema


class PositionSetInterval(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('END_DATE', 'POSITION_SET_DATES', 'WEEKLY_START_DATES', 'MONTHLY_START_DATES', 'AUTO')


class PositionSetType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('PORTFOLIO', 'BENCHMARK', 'SWAP', 'RESEARCH_TOPIC')


class ReferenceInstrumentType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('SECURITY',)


class ResourceType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('PORTFOLIO', 'RESEARCH_TOPIC')


class RiskType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('TOTAL', 'VAR_DECOMP_SPECIFIC', 'VAR_DECOMP_FACTORS')


class ScaleFormat(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('DEFAULT', 'PERCENT_GMV', 'PERCENT_MODELED_GMV', 'PERCENT_EQUITY_GMV', 'PERCENT_EQUITY_MODELED_GMV')


class SecurityListType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('WATCHLIST',)


class Sedol(sgqlc.types.Scalar):
    __schema__ = schema


class SegmentBookFilter(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('LONG', 'SHORT')


class SegmentNormalization(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('STANDALONE', 'CONTRIBUTION')


class ShortId(sgqlc.types.Scalar):
    __schema__ = schema


class SortDirection(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('ASC', 'DESC')


String = sgqlc.types.String

class Universe(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('PORTFOLIO', 'WATCHLIST', 'ETF', 'SWAP')



########################################################################
# Input Objects
########################################################################
class BetaConstraintInput(sgqlc.types.Input):
    __schema__ = schema
    historical = sgqlc.types.Field('MinMaxInput', graphql_name='historical')
    predicted = sgqlc.types.Field('MinMaxInput', graphql_name='predicted')


class ClassificationSecurityInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null('UniversalIdInput'), graphql_name='id')
    as_of = sgqlc.types.Field(Date, graphql_name='asOf')
    classification = sgqlc.types.Field(sgqlc.types.non_null('ClassificationSecurityValueInput'), graphql_name='classification')


class ClassificationSecurityValueInput(sgqlc.types.Input):
    __schema__ = schema
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class ClassificationSort(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    tier = sgqlc.types.Field(String, graphql_name='tier')


class ContentSetDateInput(sgqlc.types.Input):
    __schema__ = schema
    date = sgqlc.types.Field(sgqlc.types.non_null(Date), graphql_name='date')
    securities = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ContentSetDateSecurityInput'))), graphql_name='securities')


class ContentSetDateSecurityInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null('UniversalIdInput'), graphql_name='id')
    factors = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ContentSetFactorValueInput'))), graphql_name='factors')


class ContentSetFactorValueInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    value = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='value')


class CustomExposureObjectiveTerm(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    weight = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='weight')
    content_set_id = sgqlc.types.Field(String, graphql_name='contentSetId')


class CustomObjectiveTermWeight(sgqlc.types.Input):
    __schema__ = schema
    weight = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='weight')


class CustomOptimizationObjective(sgqlc.types.Input):
    __schema__ = schema
    minimize_risk = sgqlc.types.Field('CustomRiskObjectiveTerm', graphql_name='minimizeRisk')
    maximize_forecast_return = sgqlc.types.Field(CustomObjectiveTermWeight, graphql_name='maximizeForecastReturn')
    minimize_market_impact = sgqlc.types.Field(CustomObjectiveTermWeight, graphql_name='minimizeMarketImpact')
    maximize_exposures = sgqlc.types.Field(sgqlc.types.list_of(CustomExposureObjectiveTerm), graphql_name='maximizeExposures')
    minimize_exposures = sgqlc.types.Field(sgqlc.types.list_of(CustomExposureObjectiveTerm), graphql_name='minimizeExposures')


class CustomRiskObjectiveTerm(sgqlc.types.Input):
    __schema__ = schema
    factor_risk = sgqlc.types.Field(CustomObjectiveTermWeight, graphql_name='factorRisk')
    specific_risk = sgqlc.types.Field(CustomObjectiveTermWeight, graphql_name='specificRisk')
    base = sgqlc.types.Field(sgqlc.types.list_of('PositionSetInput'), graphql_name='base')


class DeleteClassificationSecurityInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null('UniversalIdInput'), graphql_name='id')
    all = sgqlc.types.Field(Boolean, graphql_name='all')
    from_ = sgqlc.types.Field(Date, graphql_name='from')
    to = sgqlc.types.Field(Date, graphql_name='to')


class DeleteForecastSecurityInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null('UniversalIdInput'), graphql_name='id')
    all = sgqlc.types.Field(Boolean, graphql_name='all')
    from_ = sgqlc.types.Field(Date, graphql_name='from')
    to = sgqlc.types.Field(Date, graphql_name='to')


class ExposureConstraint(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    content_set_id = sgqlc.types.Field(String, graphql_name='contentSetId')
    max = sgqlc.types.Field(Float, graphql_name='max')
    min = sgqlc.types.Field(Float, graphql_name='min')
    base = sgqlc.types.Field('PositionSetInput', graphql_name='base')
    min_relative = sgqlc.types.Field(Float, graphql_name='minRelative')
    max_relative = sgqlc.types.Field(Float, graphql_name='maxRelative')


class FactorExposureTarget(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    target = sgqlc.types.Field(Float, graphql_name='target')


class ForecastCreate(sgqlc.types.Input):
    __schema__ = schema
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')


class ForecastEquityInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field('PositionSetEquityIdInput', graphql_name='id')
    annualized_return = sgqlc.types.Field(Float, graphql_name='annualizedReturn')
    expected_percent_return = sgqlc.types.Field(Float, graphql_name='expectedPercentReturn')


class ForecastExpectedReturnInput(sgqlc.types.Input):
    __schema__ = schema
    return_ = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='return')
    horizon = sgqlc.types.Field(Int, graphql_name='horizon')


class ForecastInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(ShortId, graphql_name='id')
    implied_returns = sgqlc.types.Field(ImpliedReturnsType, graphql_name='impliedReturns')
    horizon = sgqlc.types.Field(Int, graphql_name='horizon')
    equities = sgqlc.types.Field(sgqlc.types.list_of(ForecastEquityInput), graphql_name='equities')
    swaps = sgqlc.types.Field(sgqlc.types.list_of('ForecastSwapInput'), graphql_name='swaps')


class ForecastSecurityInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null('UniversalIdInput'), graphql_name='id')
    label = sgqlc.types.Field(String, graphql_name='label')
    as_of = sgqlc.types.Field(Date, graphql_name='asOf')
    expected_return = sgqlc.types.Field(sgqlc.types.non_null(ForecastExpectedReturnInput), graphql_name='expectedReturn')


class ForecastSwapInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    expected_percent_return = sgqlc.types.Field(Float, graphql_name='expectedPercentReturn')


class ForecastUpdate(sgqlc.types.Input):
    __schema__ = schema
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')


class MinMax(sgqlc.types.Input):
    __schema__ = schema
    min = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='min')
    max = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='max')


class MinMaxConstraintInput(sgqlc.types.Input):
    __schema__ = schema
    max = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='max')


class MinMaxInput(sgqlc.types.Input):
    __schema__ = schema
    min = sgqlc.types.Field(Float, graphql_name='min')
    max = sgqlc.types.Field(Float, graphql_name='max')


class NewExperiment(sgqlc.types.Input):
    __schema__ = schema
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    type = sgqlc.types.Field(sgqlc.types.non_null(ExperimentType), graphql_name='type')
    description = sgqlc.types.Field(String, graphql_name='description')


class NewPortfolio(sgqlc.types.Input):
    __schema__ = schema
    alias = sgqlc.types.Field(String, graphql_name='alias')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    default_model_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='defaultModelId')
    rollover_position_set_to_current_date = sgqlc.types.Field(Boolean, graphql_name='rolloverPositionSetToCurrentDate')


class NewResearchTopic(sgqlc.types.Input):
    __schema__ = schema
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    reference_instrument = sgqlc.types.Field(sgqlc.types.non_null('ReferenceInstrumentInput'), graphql_name='referenceInstrument')


class NewSwap(sgqlc.types.Input):
    __schema__ = schema
    ticker = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='ticker')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    termination_date = sgqlc.types.Field(Date, graphql_name='terminationDate')


class OptimizationCompositionConstraint(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    type = sgqlc.types.Field(sgqlc.types.non_null(CompositionConstraintType), graphql_name='type')
    classification_id = sgqlc.types.Field(String, graphql_name='classificationId')
    classification_tier = sgqlc.types.Field(String, graphql_name='classificationTier')
    max_economic_exposure = sgqlc.types.Field(Float, graphql_name='maxEconomicExposure')
    min_economic_exposure = sgqlc.types.Field(Float, graphql_name='minEconomicExposure')
    max_percent_equity = sgqlc.types.Field(Float, graphql_name='maxPercentEquity')
    min_percent_equity = sgqlc.types.Field(Float, graphql_name='minPercentEquity')
    max_relative_percent_equity = sgqlc.types.Field(Float, graphql_name='maxRelativePercentEquity')
    min_relative_percent_equity = sgqlc.types.Field(Float, graphql_name='minRelativePercentEquity')
    base = sgqlc.types.Field('PositionSetInput', graphql_name='base')


class OptimizationConstantsInput(sgqlc.types.Input):
    __schema__ = schema
    equity = sgqlc.types.Field(Float, graphql_name='equity')


class OptimizationConstraints(sgqlc.types.Input):
    __schema__ = schema
    max_turnover = sgqlc.types.Field(Float, graphql_name='maxTurnover')
    risk = sgqlc.types.Field('RiskConstraintInput', graphql_name='risk')
    max_liquidation_days = sgqlc.types.Field(Float, graphql_name='maxLiquidationDays')
    max_concentration = sgqlc.types.Field(Float, graphql_name='maxConcentration')
    min_concentration = sgqlc.types.Field(Float, graphql_name='minConcentration')
    exposure = sgqlc.types.Field(sgqlc.types.list_of(ExposureConstraint), graphql_name='exposure')
    securities = sgqlc.types.Field('SecurityConstraintInput', graphql_name='securities')
    composition = sgqlc.types.Field(sgqlc.types.list_of(OptimizationCompositionConstraint), graphql_name='composition')
    min_trade = sgqlc.types.Field(Float, graphql_name='minTrade')
    max_trade = sgqlc.types.Field('OptimizationMaxTradeConstraint', graphql_name='maxTrade')
    long_market_value = sgqlc.types.Field(Float, graphql_name='longMarketValue')
    short_market_value = sgqlc.types.Field(Float, graphql_name='shortMarketValue')
    min_short_market_value = sgqlc.types.Field(Float, graphql_name='minShortMarketValue')
    max_short_market_value = sgqlc.types.Field(Float, graphql_name='maxShortMarketValue')
    min_long_market_value = sgqlc.types.Field(Float, graphql_name='minLongMarketValue')
    max_long_market_value = sgqlc.types.Field(Float, graphql_name='maxLongMarketValue')
    gmv = sgqlc.types.Field(Float, graphql_name='GMV')
    min_gmv = sgqlc.types.Field(Float, graphql_name='minGMV')
    max_gmv = sgqlc.types.Field(Float, graphql_name='maxGMV')
    net_exposure = sgqlc.types.Field(Float, graphql_name='netExposure')
    min_net_exposure = sgqlc.types.Field(Float, graphql_name='minNetExposure')
    max_net_exposure = sgqlc.types.Field(Float, graphql_name='maxNetExposure')
    max_positions = sgqlc.types.Field(Int, graphql_name='maxPositions')
    security_min_trade = sgqlc.types.Field('SecurityMinTradeInput', graphql_name='securityMinTrade')
    fix_position_set_securities = sgqlc.types.Field(Boolean, graphql_name='fixPositionSetSecurities')
    trade_swaps = sgqlc.types.Field(Boolean, graphql_name='tradeSwaps')
    max_market_impact_cost = sgqlc.types.Field(Float, graphql_name='maxMarketImpactCost')
    beta = sgqlc.types.Field(BetaConstraintInput, graphql_name='beta')


class OptimizationConstraintsOptionsInput(sgqlc.types.Input):
    __schema__ = schema
    ignore_adv = sgqlc.types.Field(Boolean, graphql_name='ignoreADV')


class OptimizationMaxTradeConstraint(sgqlc.types.Input):
    __schema__ = schema
    percent_equity = sgqlc.types.Field(Float, graphql_name='percentEquity')
    percent_adv = sgqlc.types.Field(Float, graphql_name='percentADV')
    percent_original_economic_exposure = sgqlc.types.Field(Float, graphql_name='percentOriginalEconomicExposure')


class OptimizationObjective(sgqlc.types.Input):
    __schema__ = schema
    minimize_factor_risk = sgqlc.types.Field(Boolean, graphql_name='minimizeFactorRisk')
    minimize_total_risk = sgqlc.types.Field(Boolean, graphql_name='minimizeTotalRisk')
    target_exposures = sgqlc.types.Field(sgqlc.types.list_of('TargetExposure'), graphql_name='targetExposures')
    target_total_risk = sgqlc.types.Field(Float, graphql_name='targetTotalRisk')
    target_factor_risk = sgqlc.types.Field(Float, graphql_name='targetFactorRisk')
    target_positions = sgqlc.types.Field(Float, graphql_name='targetPositions')
    custom = sgqlc.types.Field(CustomOptimizationObjective, graphql_name='custom')
    factor_exposure = sgqlc.types.Field(FactorExposureTarget, graphql_name='factorExposure')
    weight = sgqlc.types.Field(Float, graphql_name='weight')


class OptimizationObjectiveOptionsInput(sgqlc.types.Input):
    __schema__ = schema
    include_market_impact = sgqlc.types.Field(Boolean, graphql_name='includeMarketImpact')


class OptimizationOptionsInput(sgqlc.types.Input):
    __schema__ = schema
    objectives = sgqlc.types.Field(OptimizationObjectiveOptionsInput, graphql_name='objectives')
    constraints = sgqlc.types.Field(OptimizationConstraintsOptionsInput, graphql_name='constraints')
    equity = sgqlc.types.Field(Float, graphql_name='equity')
    max_time = sgqlc.types.Field(Float, graphql_name='maxTime')


class OptimizationSecuritiesInput(sgqlc.types.Input):
    __schema__ = schema
    long = sgqlc.types.Field('SecuritiesInput', graphql_name='long')
    short = sgqlc.types.Field('SecuritiesInput', graphql_name='short')
    long_or_short = sgqlc.types.Field('SecuritiesInput', graphql_name='longOrShort')


class OptimizationSecuritySearchInput(sgqlc.types.Input):
    __schema__ = schema
    filter = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SecuritySearchFilter'))), graphql_name='filter')
    sort = sgqlc.types.Field(sgqlc.types.list_of('SecuritySearchSort'), graphql_name='sort')
    take = sgqlc.types.Field(Int, graphql_name='take')


class PnlDateInput(sgqlc.types.Input):
    __schema__ = schema
    date = sgqlc.types.Field(sgqlc.types.non_null(Date), graphql_name='date')
    equities = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PnlEquityInput')), graphql_name='equities')
    currencies = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PnlOtherAssetInput')), graphql_name='currencies')
    swaps = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PnlOtherAssetInput')), graphql_name='swaps')
    fixed_income = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PnlFixedIncomeInput')), graphql_name='fixedIncome')
    commodities = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PnlOtherAssetInput')), graphql_name='commodities')
    indices = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PnlOtherAssetInput')), graphql_name='indices')
    other_assets = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PnlOtherAssetInput')), graphql_name='otherAssets')


class PnlEquityInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null('PositionSetEquityIdInput'), graphql_name='id')
    amount = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='amount')


class PnlFixedIncomeInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null('PositionSetFixedIncomeIdInput'), graphql_name='id')
    amount = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='amount')


class PnlOtherAssetInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    amount = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='amount')


class PortfolioUpdate(sgqlc.types.Input):
    __schema__ = schema
    alias = sgqlc.types.Field(String, graphql_name='alias')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    default_model_id = sgqlc.types.Field(String, graphql_name='defaultModelId')
    rollover_position_set_to_current_date = sgqlc.types.Field(Boolean, graphql_name='rolloverPositionSetToCurrentDate')


class PositionSetDateInput(sgqlc.types.Input):
    __schema__ = schema
    date = sgqlc.types.Field(sgqlc.types.non_null(Date), graphql_name='date')
    equity = sgqlc.types.Field(Float, graphql_name='equity')
    equities = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PositionSetEquityInput')), graphql_name='equities')
    currencies = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PositionSetOtherAssetInput')), graphql_name='currencies')
    swaps = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PositionSetOtherAssetInput')), graphql_name='swaps')
    fixed_income = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PositionSetFixedIncomeInput')), graphql_name='fixedIncome')
    commodities = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PositionSetOtherAssetInput')), graphql_name='commodities')
    indices = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PositionSetOtherAssetInput')), graphql_name='indices')
    other_assets = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PositionSetOtherAssetInput')), graphql_name='otherAssets')


class PositionSetEquityIdInput(sgqlc.types.Input):
    __schema__ = schema
    ticker = sgqlc.types.Field(String, graphql_name='ticker')
    mic = sgqlc.types.Field(String, graphql_name='mic')
    sedol = sgqlc.types.Field(Sedol, graphql_name='sedol')
    isin = sgqlc.types.Field(Isin, graphql_name='isin')
    cusip = sgqlc.types.Field(Cusip, graphql_name='cusip')
    model_provider_id = sgqlc.types.Field(String, graphql_name='modelProviderId')


class PositionSetEquityInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(PositionSetEquityIdInput), graphql_name='id')
    economic_exposure = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='economicExposure')


class PositionSetFixedIncomeIdInput(sgqlc.types.Input):
    __schema__ = schema
    isin = sgqlc.types.Field(Isin, graphql_name='isin')


class PositionSetFixedIncomeInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(PositionSetFixedIncomeIdInput), graphql_name='id')
    economic_exposure = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='economicExposure')


class PositionSetInput(sgqlc.types.Input):
    __schema__ = schema
    type = sgqlc.types.Field(PositionSetType, graphql_name='type')
    id = sgqlc.types.Field(String, graphql_name='id')
    experiment_id = sgqlc.types.Field(String, graphql_name='experimentId')
    weight = sgqlc.types.Field(Float, graphql_name='weight')
    dates = sgqlc.types.Field(sgqlc.types.list_of(PositionSetDateInput), graphql_name='dates')
    segment = sgqlc.types.Field('Segment', graphql_name='segment')


class PositionSetOtherAssetInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    economic_exposure = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='economicExposure')


class ReferenceInstrumentInput(sgqlc.types.Input):
    __schema__ = schema
    type = sgqlc.types.Field(sgqlc.types.non_null(ReferenceInstrumentType), graphql_name='type')
    security_id = sgqlc.types.Field(sgqlc.types.non_null('UniversalIdInput'), graphql_name='securityId')


class RiskConstraintInput(sgqlc.types.Input):
    __schema__ = schema
    total = sgqlc.types.Field(MinMaxConstraintInput, graphql_name='total')
    factor = sgqlc.types.Field(MinMaxConstraintInput, graphql_name='factor')


class SecuritiesEquityInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(PositionSetEquityIdInput, graphql_name='id')


class SecuritiesInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    type = sgqlc.types.Field(SecurityListType, graphql_name='type')
    security_search = sgqlc.types.Field(OptimizationSecuritySearchInput, graphql_name='securitySearch')
    equities = sgqlc.types.Field(sgqlc.types.list_of(SecuritiesEquityInput), graphql_name='equities')
    swaps = sgqlc.types.Field(sgqlc.types.list_of('SecuritiesSwapInput'), graphql_name='swaps')


class SecuritiesSwapInput(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')


class SecurityConstraintInput(sgqlc.types.Input):
    __schema__ = schema
    equities = sgqlc.types.Field(sgqlc.types.list_of('SecurityConstraintInputEquity'), graphql_name='equities')
    swaps = sgqlc.types.Field(sgqlc.types.list_of('SecurityConstraintInputSwap'), graphql_name='swaps')


class SecurityConstraintInputEquity(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(PositionSetEquityIdInput, graphql_name='id')
    min_economic_exposure = sgqlc.types.Field(Float, graphql_name='minEconomicExposure')
    max_economic_exposure = sgqlc.types.Field(Float, graphql_name='maxEconomicExposure')
    min_percent_equity = sgqlc.types.Field(Float, graphql_name='minPercentEquity')
    max_percent_equity = sgqlc.types.Field(Float, graphql_name='maxPercentEquity')


class SecurityConstraintInputSwap(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    min_economic_exposure = sgqlc.types.Field(Float, graphql_name='minEconomicExposure')
    max_economic_exposure = sgqlc.types.Field(Float, graphql_name='maxEconomicExposure')
    min_percent_equity = sgqlc.types.Field(Float, graphql_name='minPercentEquity')
    max_percent_equity = sgqlc.types.Field(Float, graphql_name='maxPercentEquity')


class SecurityMinTradeInput(sgqlc.types.Input):
    __schema__ = schema
    equities = sgqlc.types.Field(sgqlc.types.list_of('SecurityMinTradeInputEquity'), graphql_name='equities')


class SecurityMinTradeInputEquity(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(PositionSetEquityIdInput, graphql_name='id')
    min_trade = sgqlc.types.Field(Float, graphql_name='minTrade')


class SecuritySearchFilter(sgqlc.types.Input):
    __schema__ = schema
    factor_exposure = sgqlc.types.Field(sgqlc.types.list_of('SecuritySearchFilterFactorExposure'), graphql_name='factorExposure')
    country = sgqlc.types.Field('SecuritySearchFilterString', graphql_name='country')
    sector = sgqlc.types.Field('SecuritySearchFilterString', graphql_name='sector')
    classification = sgqlc.types.Field(sgqlc.types.list_of('SecuritySearchFilterClassification'), graphql_name='classification')
    currency = sgqlc.types.Field('SecuritySearchFilterString', graphql_name='currency')
    asset_class = sgqlc.types.Field('SecuritySearchFilterString', graphql_name='assetClass')
    asset_subclass = sgqlc.types.Field('SecuritySearchFilterString', graphql_name='assetSubclass')
    average_daily_volume = sgqlc.types.Field('SecuritySearchFilterFloat', graphql_name='averageDailyVolume')
    market_capitalization = sgqlc.types.Field('SecuritySearchFilterFloat', graphql_name='marketCapitalization')
    beta = sgqlc.types.Field('SecuritySearchFilterBeta', graphql_name='beta')
    universe = sgqlc.types.Field(sgqlc.types.list_of('SecuritySearchFilterUniverse'), graphql_name='universe')
    securities = sgqlc.types.Field('SecuritySearchFilterSecurities', graphql_name='securities')
    risk = sgqlc.types.Field(sgqlc.types.list_of('SecuritySearchFilterRisk'), graphql_name='risk')


class SecuritySearchFilterBeta(sgqlc.types.Input):
    __schema__ = schema
    predicted = sgqlc.types.Field('SecuritySearchFilterFloat', graphql_name='predicted')
    historical = sgqlc.types.Field('SecuritySearchFilterFloat', graphql_name='historical')


class SecuritySearchFilterClassification(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    in_ = sgqlc.types.Field(sgqlc.types.list_of('SecuritySearchFilterClassificationTier'), graphql_name='in')
    not_in = sgqlc.types.Field(sgqlc.types.list_of('SecuritySearchFilterClassificationTier'), graphql_name='notIn')
    eq = sgqlc.types.Field('SecuritySearchFilterClassificationTier', graphql_name='eq')
    neq = sgqlc.types.Field('SecuritySearchFilterClassificationTier', graphql_name='neq')


class SecuritySearchFilterClassificationTier(sgqlc.types.Input):
    __schema__ = schema
    tier = sgqlc.types.Field(String, graphql_name='tier')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class SecuritySearchFilterFactorExposure(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    content_set_id = sgqlc.types.Field(String, graphql_name='contentSetId')
    gt = sgqlc.types.Field(Float, graphql_name='gt')
    lt = sgqlc.types.Field(Float, graphql_name='lt')
    gte = sgqlc.types.Field(Float, graphql_name='gte')
    lte = sgqlc.types.Field(Float, graphql_name='lte')
    eq = sgqlc.types.Field(Float, graphql_name='eq')
    neq = sgqlc.types.Field(Float, graphql_name='neq')
    between = sgqlc.types.Field(MinMax, graphql_name='between')
    not_between = sgqlc.types.Field(MinMax, graphql_name='notBetween')


class SecuritySearchFilterFloat(sgqlc.types.Input):
    __schema__ = schema
    gt = sgqlc.types.Field(Float, graphql_name='gt')
    lt = sgqlc.types.Field(Float, graphql_name='lt')
    gte = sgqlc.types.Field(Float, graphql_name='gte')
    lte = sgqlc.types.Field(Float, graphql_name='lte')
    eq = sgqlc.types.Field(Float, graphql_name='eq')
    neq = sgqlc.types.Field(Float, graphql_name='neq')
    between = sgqlc.types.Field(MinMax, graphql_name='between')
    not_between = sgqlc.types.Field(MinMax, graphql_name='notBetween')


class SecuritySearchFilterRisk(sgqlc.types.Input):
    __schema__ = schema
    type = sgqlc.types.Field(sgqlc.types.non_null(RiskType), graphql_name='type')
    gt = sgqlc.types.Field(Float, graphql_name='gt')
    lt = sgqlc.types.Field(Float, graphql_name='lt')
    gte = sgqlc.types.Field(Float, graphql_name='gte')
    lte = sgqlc.types.Field(Float, graphql_name='lte')
    eq = sgqlc.types.Field(Float, graphql_name='eq')
    neq = sgqlc.types.Field(Float, graphql_name='neq')
    between = sgqlc.types.Field(MinMax, graphql_name='between')
    not_between = sgqlc.types.Field(MinMax, graphql_name='notBetween')


class SecuritySearchFilterSecurities(sgqlc.types.Input):
    __schema__ = schema
    in_ = sgqlc.types.Field(sgqlc.types.list_of('UniversalIdInput'), graphql_name='in')
    not_in = sgqlc.types.Field(sgqlc.types.list_of('UniversalIdInput'), graphql_name='notIn')


class SecuritySearchFilterString(sgqlc.types.Input):
    __schema__ = schema
    in_ = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='in')
    not_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='notIn')
    eq = sgqlc.types.Field(String, graphql_name='eq')
    neq = sgqlc.types.Field(String, graphql_name='neq')


class SecuritySearchFilterUniverse(sgqlc.types.Input):
    __schema__ = schema
    type = sgqlc.types.Field(sgqlc.types.non_null(Universe), graphql_name='type')
    in_ = sgqlc.types.Field(String, graphql_name='in')
    not_in = sgqlc.types.Field(String, graphql_name='notIn')


class SecuritySearchSort(sgqlc.types.Input):
    __schema__ = schema
    content_set_id = sgqlc.types.Field(String, graphql_name='contentSetId')
    factor_exposure_id = sgqlc.types.Field(String, graphql_name='factorExposureId')
    risk = sgqlc.types.Field(RiskType, graphql_name='risk')
    beta = sgqlc.types.Field(BetaType, graphql_name='beta')
    descriptor = sgqlc.types.Field(Descriptor, graphql_name='descriptor')
    classification = sgqlc.types.Field(ClassificationSort, graphql_name='classification')
    direction = sgqlc.types.Field(sgqlc.types.non_null(SortDirection), graphql_name='direction')


class Segment(sgqlc.types.Input):
    __schema__ = schema
    filters = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SegmentFilter'))), graphql_name='filters')
    normalization = sgqlc.types.Field(sgqlc.types.non_null(SegmentNormalization), graphql_name='normalization')


class SegmentFilter(sgqlc.types.Input):
    __schema__ = schema
    long_short = sgqlc.types.Field(SegmentBookFilter, graphql_name='longShort')
    sector = sgqlc.types.Field(SecuritySearchFilterString, graphql_name='sector')
    classification = sgqlc.types.Field(sgqlc.types.list_of(SecuritySearchFilterClassification), graphql_name='classification')
    country = sgqlc.types.Field(SecuritySearchFilterString, graphql_name='country')
    currency = sgqlc.types.Field(SecuritySearchFilterString, graphql_name='currency')
    asset_class = sgqlc.types.Field(SecuritySearchFilterString, graphql_name='assetClass')
    asset_subclass = sgqlc.types.Field(SecuritySearchFilterString, graphql_name='assetSubclass')
    average_daily_volume = sgqlc.types.Field(SecuritySearchFilterFloat, graphql_name='averageDailyVolume')
    market_capitalization = sgqlc.types.Field(SecuritySearchFilterFloat, graphql_name='marketCapitalization')


class SwapUpdate(sgqlc.types.Input):
    __schema__ = schema
    description = sgqlc.types.Field(String, graphql_name='description')
    termination_date = sgqlc.types.Field(Date, graphql_name='terminationDate')


class TargetExposure(sgqlc.types.Input):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    target = sgqlc.types.Field(Float, graphql_name='target')


class UniversalIdInput(sgqlc.types.Input):
    __schema__ = schema
    sedol = sgqlc.types.Field(String, graphql_name='sedol')
    isin = sgqlc.types.Field(String, graphql_name='isin')
    ticker = sgqlc.types.Field(String, graphql_name='ticker')
    mic = sgqlc.types.Field(String, graphql_name='mic')
    country = sgqlc.types.Field(String, graphql_name='country')


class UpdateExperiment(sgqlc.types.Input):
    __schema__ = schema
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')


class UpdateResearchTopic(sgqlc.types.Input):
    __schema__ = schema
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')


class WatchlistSecuritiesInput(sgqlc.types.Input):
    __schema__ = schema
    equities = sgqlc.types.Field(sgqlc.types.list_of(PositionSetEquityIdInput), graphql_name='equities')
    currencies = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='currencies')
    swaps = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='swaps')
    fixed_income = sgqlc.types.Field(sgqlc.types.list_of(PositionSetFixedIncomeIdInput), graphql_name='fixedIncome')
    commodities = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='commodities')
    indices = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='indices')


class WatchlistUpdate(sgqlc.types.Input):
    __schema__ = schema
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    alias = sgqlc.types.Field(String, graphql_name='alias')



########################################################################
# Output Objects and Interfaces
########################################################################
class BenchmarkMetadata(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    available_from = sgqlc.types.Field(Date, graphql_name='availableFrom')
    current_date = sgqlc.types.Field(Date, graphql_name='currentDate')


class Beta(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    rolled_over_from = sgqlc.types.Field(Date, graphql_name='rolledOverFrom')
    predicted = sgqlc.types.Field(Float, graphql_name='predicted')
    historical = sgqlc.types.Field(Float, graphql_name='historical')


class BetaContributor(sgqlc.types.Type):
    __schema__ = schema
    asset_class = sgqlc.types.Field(String, graphql_name='assetClass')
    asset_subclass = sgqlc.types.Field(String, graphql_name='assetSubclass')
    id = sgqlc.types.Field(String, graphql_name='id')
    country = sgqlc.types.Field(String, graphql_name='country')
    currency = sgqlc.types.Field(String, graphql_name='currency')
    sector = sgqlc.types.Field(String, graphql_name='sector')
    classification = sgqlc.types.Field('SecurityClassification', graphql_name='classification', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('tier', sgqlc.types.Arg(String, graphql_name='tier', default=None)),
))
    )
    description = sgqlc.types.Field(String, graphql_name='description')
    percent_equity = sgqlc.types.Field(Float, graphql_name='percentEquity')
    sedol = sgqlc.types.Field(Sedol, graphql_name='sedol')
    isin = sgqlc.types.Field(Isin, graphql_name='isin')
    cusip = sgqlc.types.Field(Cusip, graphql_name='cusip')
    predicted = sgqlc.types.Field(Float, graphql_name='predicted')
    historical = sgqlc.types.Field(Float, graphql_name='historical')


class BetaContributorDate(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    rolled_over_from = sgqlc.types.Field(Date, graphql_name='rolledOverFrom')
    contributors = sgqlc.types.Field(sgqlc.types.list_of(BetaContributor), graphql_name='contributors')


class BetaContributorGroup(sgqlc.types.Type):
    __schema__ = schema
    name = sgqlc.types.Field(String, graphql_name='name')
    id = sgqlc.types.Field(String, graphql_name='id')
    total_percent_equity = sgqlc.types.Field(Float, graphql_name='totalPercentEquity')
    contributors = sgqlc.types.Field(sgqlc.types.list_of(BetaContributor), graphql_name='contributors')
    predicted = sgqlc.types.Field(Float, graphql_name='predicted')
    historical = sgqlc.types.Field(Float, graphql_name='historical')


class Category(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    factors = sgqlc.types.Field(sgqlc.types.list_of('CategoryFactor'), graphql_name='factors')


class CategoryFactor(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')


class Classification(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    versions = sgqlc.types.Field(sgqlc.types.list_of('ClassificationVersion'), graphql_name='versions')
    version = sgqlc.types.Field('ClassificationVersion', graphql_name='version', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
))
    )


class ClassificationDeleteResult(sgqlc.types.Type):
    __schema__ = schema
    count = sgqlc.types.Field(Int, graphql_name='count')


class ClassificationDetailsDate(sgqlc.types.Type):
    __schema__ = schema
    as_of = sgqlc.types.Field(Date, graphql_name='asOf')
    securities = sgqlc.types.Field(sgqlc.types.list_of('ClassificationSecurity'), graphql_name='securities')


class ClassificationMetadata(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    versions = sgqlc.types.Field(sgqlc.types.list_of('ClassificationVersion'), graphql_name='versions')


class ClassificationSecurity(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field('UniversalId', graphql_name='id')
    as_of = sgqlc.types.Field(Date, graphql_name='asOf')
    classification = sgqlc.types.Field('ClassificationSecurityValue', graphql_name='classification')


class ClassificationSecurityValue(sgqlc.types.Type):
    __schema__ = schema
    value = sgqlc.types.Field(String, graphql_name='value')


class ClassificationTiers(sgqlc.types.Type):
    __schema__ = schema
    level = sgqlc.types.Field(Int, graphql_name='level')
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')


class ClassificationUpdateResult(sgqlc.types.Type):
    __schema__ = schema
    success_count = sgqlc.types.Field(Int, graphql_name='successCount')
    unmapped_securities = sgqlc.types.Field(sgqlc.types.list_of(ClassificationSecurity), graphql_name='unmappedSecurities')


class ClassificationValue(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    values = sgqlc.types.Field(sgqlc.types.list_of('ClassificationValue'), graphql_name='values')


class ClassificationVersion(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    as_of = sgqlc.types.Field(Date, graphql_name='asOf')
    tiers = sgqlc.types.Field(sgqlc.types.list_of(ClassificationTiers), graphql_name='tiers')
    values = sgqlc.types.Field(sgqlc.types.list_of(ClassificationValue), graphql_name='values', args=sgqlc.types.ArgDict((
        ('tier', sgqlc.types.Arg(String, graphql_name='tier', default=None)),
))
    )


class Composition(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    gmv = sgqlc.types.Field(Float, graphql_name='gmv')
    modeled_gmv = sgqlc.types.Field(Float, graphql_name='modeledGmv')
    equity = sgqlc.types.Field(Float, graphql_name='equity')
    reference_equity = sgqlc.types.Field(Float, graphql_name='referenceEquity')
    positions_count = sgqlc.types.Field(Int, graphql_name='positionsCount')
    summary_stats = sgqlc.types.Field('CompositionSummaryStats', graphql_name='summaryStats')
    concentration = sgqlc.types.Field('CompositionConcentration', graphql_name='concentration')
    composition_by = sgqlc.types.Field(sgqlc.types.list_of('CompositionGroup'), graphql_name='compositionBy', args=sgqlc.types.ArgDict((
        ('group_by', sgqlc.types.Arg(sgqlc.types.non_null(ContributorGroupType), graphql_name='groupBy', default=None)),
        ('classification_id', sgqlc.types.Arg(String, graphql_name='classificationId', default=None)),
        ('classification_tier', sgqlc.types.Arg(String, graphql_name='classificationTier', default=None)),
))
    )
    positions = sgqlc.types.Field(sgqlc.types.list_of('CompositionPositions'), graphql_name='positions')


class CompositionConcentration(sgqlc.types.Type):
    __schema__ = schema
    min = sgqlc.types.Field(Float, graphql_name='min')
    max = sgqlc.types.Field(Float, graphql_name='max')


class CompositionGroup(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    description = sgqlc.types.Field(String, graphql_name='description')
    percent_equity = sgqlc.types.Field(Float, graphql_name='percentEquity')
    economic_exposure = sgqlc.types.Field(Float, graphql_name='economicExposure')


class CompositionPositions(sgqlc.types.Type):
    __schema__ = schema
    asset_class = sgqlc.types.Field(String, graphql_name='assetClass')
    asset_subclass = sgqlc.types.Field(String, graphql_name='assetSubclass')
    id = sgqlc.types.Field(String, graphql_name='id')
    country = sgqlc.types.Field(String, graphql_name='country')
    currency = sgqlc.types.Field(String, graphql_name='currency')
    industry_classification = sgqlc.types.Field('SecurityDescriptor', graphql_name='industryClassification', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(sgqlc.types.non_null(IndustryClassificationType), graphql_name='type', default=None)),
))
    )
    classification = sgqlc.types.Field('SecurityClassification', graphql_name='classification', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('tier', sgqlc.types.Arg(String, graphql_name='tier', default=None)),
))
    )
    description = sgqlc.types.Field(String, graphql_name='description')
    economic_exposure = sgqlc.types.Field(Float, graphql_name='economicExposure')
    average_daily_volume = sgqlc.types.Field(Float, graphql_name='averageDailyVolume')
    market_cap = sgqlc.types.Field(Float, graphql_name='marketCap')


class CompositionSummaryStats(sgqlc.types.Type):
    __schema__ = schema
    average = sgqlc.types.Field('CompositionSummaryStatsAverage', graphql_name='average')
    max = sgqlc.types.Field('CompositionSummaryStatsMax', graphql_name='max')


class CompositionSummaryStatsAverage(sgqlc.types.Type):
    __schema__ = schema
    market_capitalization = sgqlc.types.Field(Float, graphql_name='marketCapitalization')


class CompositionSummaryStatsMax(sgqlc.types.Type):
    __schema__ = schema
    days_to_liquidate = sgqlc.types.Field(Float, graphql_name='daysToLiquidate')


class ContentSet(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    availability = sgqlc.types.Field('ContentSetAvailability', graphql_name='availability')
    factors = sgqlc.types.Field(sgqlc.types.list_of('ContentSetFactor'), graphql_name='factors', args=sgqlc.types.ArgDict((
        ('category', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='category', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='id', default=None)),
))
    )
    categories = sgqlc.types.Field(sgqlc.types.list_of(Category), graphql_name='categories', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='id', default=None)),
))
    )
    dates = sgqlc.types.Field(sgqlc.types.list_of('ContentSetDate'), graphql_name='dates', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
))
    )


class ContentSetAvailability(sgqlc.types.Type):
    __schema__ = schema
    start_date = sgqlc.types.Field(Date, graphql_name='startDate')
    current_date = sgqlc.types.Field(Date, graphql_name='currentDate')


class ContentSetDate(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    securities = sgqlc.types.Field(sgqlc.types.list_of('ContentSetDateSecurity'), graphql_name='securities')


class ContentSetDateSecurity(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field('UniversalId', graphql_name='id')
    factors = sgqlc.types.Field(sgqlc.types.list_of('ContentSetFactorValue'), graphql_name='factors')


class ContentSetFactor(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    category = sgqlc.types.Field(String, graphql_name='category')


class ContentSetFactorValue(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    value = sgqlc.types.Field(Float, graphql_name='value')


class ContentSetMetadata(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    factors = sgqlc.types.Field(sgqlc.types.list_of(ContentSetFactor), graphql_name='factors')
    categories = sgqlc.types.Field(sgqlc.types.list_of(Category), graphql_name='categories')


class Coverage(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    summary = sgqlc.types.Field('CoverageSummary', graphql_name='summary')
    missing_equities = sgqlc.types.Field(sgqlc.types.list_of('MissingEquity'), graphql_name='missingEquities')
    missing_currencies = sgqlc.types.Field(sgqlc.types.list_of('MissingOtherAsset'), graphql_name='missingCurrencies')
    missing_swaps = sgqlc.types.Field(sgqlc.types.list_of('MissingOtherAsset'), graphql_name='missingSwaps')
    missing_commodities = sgqlc.types.Field(sgqlc.types.list_of('MissingOtherAsset'), graphql_name='missingCommodities')
    missing_indices = sgqlc.types.Field(sgqlc.types.list_of('MissingOtherAsset'), graphql_name='missingIndices')
    missing_fixed_income = sgqlc.types.Field(sgqlc.types.list_of('MissingFixedIncome'), graphql_name='missingFixedIncome')
    missing_other_assets = sgqlc.types.Field(sgqlc.types.list_of('MissingOtherAsset'), graphql_name='missingOtherAssets')


class CoverageSummary(sgqlc.types.Type):
    __schema__ = schema
    percent_gmv_available = sgqlc.types.Field(Float, graphql_name='percentGmvAvailable')
    percent_gmv_not_available = sgqlc.types.Field(Float, graphql_name='percentGmvNotAvailable')


class DailyPnlDate(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    amount = sgqlc.types.Field(Float, graphql_name='amount')


class DeleteResult(sgqlc.types.Type):
    __schema__ = schema
    count = sgqlc.types.Field(Int, graphql_name='count')


class Experiment(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    available_from = sgqlc.types.Field(Date, graphql_name='availableFrom')
    type = sgqlc.types.Field(ExperimentType, graphql_name='type')
    dates = sgqlc.types.Field(sgqlc.types.list_of('PositionSetDate'), graphql_name='dates', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
))
    )
    last_updated = sgqlc.types.Field(Date, graphql_name='lastUpdated')


class ExperimentMetadata(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    type = sgqlc.types.Field(ExperimentType, graphql_name='type')
    available_from = sgqlc.types.Field(Date, graphql_name='availableFrom')
    last_updated = sgqlc.types.Field(Date, graphql_name='lastUpdated')


class Exposure(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    rolled_over_from = sgqlc.types.Field(Date, graphql_name='rolledOverFrom')
    factors = sgqlc.types.Field(sgqlc.types.list_of('ExposureFactor'), graphql_name='factors', args=sgqlc.types.ArgDict((
        ('category', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='category', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='id', default=None)),
))
    )


class ExposureContributor(sgqlc.types.Type):
    __schema__ = schema
    asset_class = sgqlc.types.Field(String, graphql_name='assetClass')
    asset_subclass = sgqlc.types.Field(String, graphql_name='assetSubclass')
    id = sgqlc.types.Field(String, graphql_name='id')
    country = sgqlc.types.Field(String, graphql_name='country')
    currency = sgqlc.types.Field(String, graphql_name='currency')
    sector = sgqlc.types.Field(String, graphql_name='sector')
    classification = sgqlc.types.Field('SecurityClassification', graphql_name='classification', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('tier', sgqlc.types.Arg(String, graphql_name='tier', default=None)),
))
    )
    description = sgqlc.types.Field(String, graphql_name='description')
    percent_equity = sgqlc.types.Field(Float, graphql_name='percentEquity')
    sedol = sgqlc.types.Field(Sedol, graphql_name='sedol')
    isin = sgqlc.types.Field(Isin, graphql_name='isin')
    cusip = sgqlc.types.Field(Cusip, graphql_name='cusip')
    factors = sgqlc.types.Field(sgqlc.types.list_of('ExposureContributorFactor'), graphql_name='factors', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='id', default=None)),
        ('category', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='category', default=None)),
))
    )


class ExposureContributorDate(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    rolled_over_from = sgqlc.types.Field(Date, graphql_name='rolledOverFrom')
    contributors = sgqlc.types.Field(sgqlc.types.list_of(ExposureContributor), graphql_name='contributors')


class ExposureContributorFactor(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    category = sgqlc.types.Field(String, graphql_name='category')
    z_score = sgqlc.types.Field(Float, graphql_name='zScore')
    security_exposure = sgqlc.types.Field(Float, graphql_name='securityExposure')
    contribution = sgqlc.types.Field(Float, graphql_name='contribution')
    gross_contribution = sgqlc.types.Field(Float, graphql_name='grossContribution')
    net_contribution = sgqlc.types.Field(Float, graphql_name='netContribution')


class ExposureContributorGroup(sgqlc.types.Type):
    __schema__ = schema
    name = sgqlc.types.Field(String, graphql_name='name')
    id = sgqlc.types.Field(String, graphql_name='id')
    total_percent_equity = sgqlc.types.Field(Float, graphql_name='totalPercentEquity')
    contributors = sgqlc.types.Field(sgqlc.types.list_of(ExposureContributor), graphql_name='contributors')
    factors = sgqlc.types.Field(sgqlc.types.list_of('ExposureContributorGroupFactor'), graphql_name='factors', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='id', default=None)),
        ('category', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='category', default=None)),
))
    )


class ExposureContributorGroupFactor(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    category = sgqlc.types.Field(String, graphql_name='category')
    net_exposure = sgqlc.types.Field(Float, graphql_name='netExposure')
    gross_contribution = sgqlc.types.Field(Float, graphql_name='grossContribution')
    net_contribution = sgqlc.types.Field(Float, graphql_name='netContribution')


class ExposureFactor(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    category = sgqlc.types.Field(String, graphql_name='category')
    net = sgqlc.types.Field(Float, graphql_name='net')
    long = sgqlc.types.Field(Float, graphql_name='long')
    short = sgqlc.types.Field(Float, graphql_name='short')


class Factor(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    category = sgqlc.types.Field(String, graphql_name='category')
    performance = sgqlc.types.Field(sgqlc.types.list_of('FactorPerformance'), graphql_name='performance', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('aggregation', sgqlc.types.Arg(Aggregation, graphql_name='aggregation', default=None)),
        ('interval', sgqlc.types.Arg(Interval, graphql_name='interval', default=None)),
))
    )
    covariance = sgqlc.types.Field('FactorCovariance', graphql_name='covariance', args=sgqlc.types.ArgDict((
        ('on', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='on', default=None)),
))
    )


class FactorCovariance(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    factors = sgqlc.types.Field(sgqlc.types.list_of('FactorCovarianceValue'), graphql_name='factors', args=sgqlc.types.ArgDict((
        ('category', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='category', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='id', default=None)),
))
    )


class FactorCovarianceValue(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    category = sgqlc.types.Field(String, graphql_name='category')
    annualized_percent_squared = sgqlc.types.Field(Float, graphql_name='annualizedPercentSquared')


class FactorPerformance(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    percent_price_change1_day = sgqlc.types.Field(Float, graphql_name='percentPriceChange1Day')
    percent_price_change_cumulative = sgqlc.types.Field(Float, graphql_name='percentPriceChangeCumulative')
    normalized_return = sgqlc.types.Field(Float, graphql_name='normalizedReturn')


class Forecast(sgqlc.types.Type):
    __schema__ = schema
    horizon = sgqlc.types.Field(Int, graphql_name='horizon')
    total = sgqlc.types.Field(Float, graphql_name='total')
    equities = sgqlc.types.Field(sgqlc.types.list_of('ForecastEquity'), graphql_name='equities')
    swaps = sgqlc.types.Field(sgqlc.types.list_of('ForecastSwap'), graphql_name='swaps')


class ForecastDeleteResult(sgqlc.types.Type):
    __schema__ = schema
    count = sgqlc.types.Field(Int, graphql_name='count')


class ForecastDetails(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(ShortId, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')
    dates = sgqlc.types.Field(sgqlc.types.list_of('ForecastDetailsDate'), graphql_name='dates', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
))
    )
    security_dates = sgqlc.types.Field(sgqlc.types.list_of('ForecastSecurity'), graphql_name='securityDates', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(UniversalIdInput), graphql_name='id', default=None)),
        ('id_date', sgqlc.types.Arg(Date, graphql_name='idDate', default=None)),
))
    )


class ForecastDetailsDate(sgqlc.types.Type):
    __schema__ = schema
    as_of = sgqlc.types.Field(Date, graphql_name='asOf')
    securities = sgqlc.types.Field(sgqlc.types.list_of('ForecastSecurity'), graphql_name='securities')


class ForecastEquity(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field('PositionSetEquityId', graphql_name='id')
    expected_percent_return = sgqlc.types.Field(Float, graphql_name='expectedPercentReturn')


class ForecastExpectedReturn(sgqlc.types.Type):
    __schema__ = schema
    return_ = sgqlc.types.Field(Float, graphql_name='return')
    horizon = sgqlc.types.Field(Int, graphql_name='horizon')


class ForecastMeta(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(ShortId, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')


class ForecastSecurity(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field('UniversalId', graphql_name='id')
    label = sgqlc.types.Field(String, graphql_name='label')
    as_of = sgqlc.types.Field(Date, graphql_name='asOf')
    expected_return = sgqlc.types.Field(ForecastExpectedReturn, graphql_name='expectedReturn')


class ForecastSwap(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    expected_percent_return = sgqlc.types.Field(Float, graphql_name='expectedPercentReturn')


class ForecastTypes(sgqlc.types.Type):
    __schema__ = schema
    implied_returns = sgqlc.types.Field(Forecast, graphql_name='impliedReturns', args=sgqlc.types.ArgDict((
        ('risk_factors', sgqlc.types.Arg(sgqlc.types.non_null(ImpliedReturnsType), graphql_name='riskFactors', default=None)),
))
    )
    custom = sgqlc.types.Field(Forecast, graphql_name='custom', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ShortId), graphql_name='id', default=None)),
))
    )


class ForecastUpdateResult(sgqlc.types.Type):
    __schema__ = schema
    success_count = sgqlc.types.Field(Int, graphql_name='successCount')
    unmapped_securities = sgqlc.types.Field(sgqlc.types.list_of(ForecastSecurity), graphql_name='unmappedSecurities')


class GroupedBetaContributorDate(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    rolled_over_from = sgqlc.types.Field(Date, graphql_name='rolledOverFrom')
    grouped_contributors = sgqlc.types.Field(sgqlc.types.list_of(BetaContributorGroup), graphql_name='groupedContributors')


class GroupedExposureContributorDate(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    rolled_over_from = sgqlc.types.Field(Date, graphql_name='rolledOverFrom')
    grouped_contributors = sgqlc.types.Field(sgqlc.types.list_of(ExposureContributorGroup), graphql_name='groupedContributors')


class MarketImpact(sgqlc.types.Type):
    __schema__ = schema
    cost = sgqlc.types.Field(Float, graphql_name='cost')
    contributors = sgqlc.types.Field(sgqlc.types.list_of('MarketImpactContributor'), graphql_name='contributors')


class MarketImpactContributor(sgqlc.types.Type):
    __schema__ = schema
    asset_class = sgqlc.types.Field(String, graphql_name='assetClass')
    asset_subclass = sgqlc.types.Field(String, graphql_name='assetSubclass')
    id = sgqlc.types.Field(String, graphql_name='id')
    country = sgqlc.types.Field(String, graphql_name='country')
    currency = sgqlc.types.Field(String, graphql_name='currency')
    industry_classification = sgqlc.types.Field('SecurityDescriptor', graphql_name='industryClassification', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(sgqlc.types.non_null(IndustryClassificationType), graphql_name='type', default=None)),
))
    )
    classification = sgqlc.types.Field('SecurityClassification', graphql_name='classification', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('tier', sgqlc.types.Arg(String, graphql_name='tier', default=None)),
))
    )
    cost = sgqlc.types.Field(Float, graphql_name='cost')


class MaxDrawdown(sgqlc.types.Type):
    __schema__ = schema
    drawdown = sgqlc.types.Field(Float, graphql_name='drawdown')
    from_ = sgqlc.types.Field(Date, graphql_name='from')
    to = sgqlc.types.Field(Date, graphql_name='to')
    days_between = sgqlc.types.Field(Int, graphql_name='daysBetween')


class Meta(sgqlc.types.Type):
    __schema__ = schema
    points = sgqlc.types.Field('MetaPoints', graphql_name='points')
    optimization = sgqlc.types.Field('OptimizationMeta', graphql_name='optimization')


class MetaPoints(sgqlc.types.Type):
    __schema__ = schema
    cost = sgqlc.types.Field(Int, graphql_name='cost')
    points_left = sgqlc.types.Field(Int, graphql_name='pointsLeft')
    seconds_to_points_reset = sgqlc.types.Field(Int, graphql_name='secondsToPointsReset')


class MissingEquity(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field('PositionSetEquityId', graphql_name='id')
    percent_gmv = sgqlc.types.Field(Float, graphql_name='percentGmv')


class MissingFixedIncome(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field('PositionSetFixedIncomeId', graphql_name='id')
    percent_gmv = sgqlc.types.Field(Float, graphql_name='percentGmv')


class MissingOtherAsset(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    percent_gmv = sgqlc.types.Field(Float, graphql_name='percentGmv')


class Model(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    availability = sgqlc.types.Field('ModelAvailability', graphql_name='availability')
    benchmarks = sgqlc.types.Field(sgqlc.types.list_of(BenchmarkMetadata), graphql_name='benchmarks')
    factors = sgqlc.types.Field(sgqlc.types.list_of(Factor), graphql_name='factors', args=sgqlc.types.ArgDict((
        ('category', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='category', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='id', default=None)),
))
    )
    categories = sgqlc.types.Field(sgqlc.types.list_of(Category), graphql_name='categories', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='id', default=None)),
))
    )
    security = sgqlc.types.Field('Security', graphql_name='security', args=sgqlc.types.ArgDict((
        ('ticker', sgqlc.types.Arg(String, graphql_name='ticker', default=None)),
        ('exchange', sgqlc.types.Arg(String, graphql_name='exchange', default=None)),
        ('mic', sgqlc.types.Arg(String, graphql_name='mic', default=None)),
        ('sedol', sgqlc.types.Arg(Sedol, graphql_name='sedol', default=None)),
        ('isin', sgqlc.types.Arg(Isin, graphql_name='isin', default=None)),
        ('cusip', sgqlc.types.Arg(Cusip, graphql_name='cusip', default=None)),
        ('model_provider_id', sgqlc.types.Arg(String, graphql_name='modelProviderId', default=None)),
))
    )
    portfolio = sgqlc.types.Field('ModelPortfolio', graphql_name='portfolio', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
))
    )
    simulation = sgqlc.types.Field('ModelSimulation', graphql_name='simulation', args=sgqlc.types.ArgDict((
        ('position_set', sgqlc.types.Arg(sgqlc.types.non_null(PositionSetInput), graphql_name='positionSet', default=None)),
        ('base', sgqlc.types.Arg(sgqlc.types.list_of(PositionSetInput), graphql_name='base', default=None)),
        ('from_', sgqlc.types.Arg(Date, graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(Date, graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
))
    )
    optimization = sgqlc.types.Field('ModelOptimization', graphql_name='optimization', args=sgqlc.types.ArgDict((
        ('position_set', sgqlc.types.Arg(PositionSetInput, graphql_name='positionSet', default=None)),
        ('base', sgqlc.types.Arg(sgqlc.types.list_of(PositionSetInput), graphql_name='base', default=None)),
        ('on', sgqlc.types.Arg(sgqlc.types.list_of(Date), graphql_name='on', default=None)),
        ('objective', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(OptimizationObjective)), graphql_name='objective', default=None)),
        ('constraints', sgqlc.types.Arg(sgqlc.types.non_null(OptimizationConstraints), graphql_name='constraints', default=None)),
        ('securities', sgqlc.types.Arg(OptimizationSecuritiesInput, graphql_name='securities', default=None)),
        ('constants', sgqlc.types.Arg(OptimizationConstantsInput, graphql_name='constants', default=None)),
        ('options', sgqlc.types.Arg(OptimizationOptionsInput, graphql_name='options', default=None)),
        ('forecast', sgqlc.types.Arg(ForecastInput, graphql_name='forecast', default=None)),
))
    )
    security_search = sgqlc.types.Field('SecuritySearchResult', graphql_name='securitySearch', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(SecuritySearchFilter))), graphql_name='filter', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(SecuritySearchSort), graphql_name='sort', default=None)),
        ('on', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='on', default=None)),
        ('take', sgqlc.types.Arg(Int, graphql_name='take', default=None)),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
))
    )


class ModelAvailability(sgqlc.types.Type):
    __schema__ = schema
    current_date = sgqlc.types.Field(Date, graphql_name='currentDate')
    factors_start_date = sgqlc.types.Field(Date, graphql_name='factorsStartDate')
    securities_start_date = sgqlc.types.Field(Date, graphql_name='securitiesStartDate')
    dates = sgqlc.types.Field(sgqlc.types.list_of(Date), graphql_name='dates', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
))
    )


class ModelMetadata(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    short_name = sgqlc.types.Field(String, graphql_name='shortName')
    availability = sgqlc.types.Field(ModelAvailability, graphql_name='availability')


class ModelOptimization(sgqlc.types.Type):
    __schema__ = schema
    positions_delta = sgqlc.types.Field(sgqlc.types.list_of('OptimizationPositionsDelta'), graphql_name='positionsDelta')
    risk = sgqlc.types.Field(sgqlc.types.list_of('Risk'), graphql_name='risk')
    risk_contributors = sgqlc.types.Field(sgqlc.types.list_of('RiskContributor'), graphql_name='riskContributors', args=sgqlc.types.ArgDict((
        ('on', sgqlc.types.Arg(Date, graphql_name='on', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
))
    )
    exposure = sgqlc.types.Field(sgqlc.types.list_of(Exposure), graphql_name='exposure', args=sgqlc.types.ArgDict((
        ('content_set_id', sgqlc.types.Arg(String, graphql_name='contentSetId', default=None)),
))
    )
    exposure_contributors = sgqlc.types.Field(sgqlc.types.list_of(ExposureContributorDate), graphql_name='exposureContributors', args=sgqlc.types.ArgDict((
        ('content_set_id', sgqlc.types.Arg(String, graphql_name='contentSetId', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('active', sgqlc.types.Arg(ActiveContributorType, graphql_name='active', default=None)),
))
    )
    beta = sgqlc.types.Field(sgqlc.types.list_of(Beta), graphql_name='beta')
    beta_contributors = sgqlc.types.Field(sgqlc.types.list_of(BetaContributorDate), graphql_name='betaContributors', args=sgqlc.types.ArgDict((
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('active', sgqlc.types.Arg(ActiveContributorType, graphql_name='active', default=None)),
))
    )
    performance = sgqlc.types.Field(sgqlc.types.list_of('Performance'), graphql_name='performance', args=sgqlc.types.ArgDict((
        ('aggregation', sgqlc.types.Arg(Aggregation, graphql_name='aggregation', default=None)),
        ('to', sgqlc.types.Arg(Date, graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
))
    )
    positions = sgqlc.types.Field('OptimizedPositionSet', graphql_name='positions', args=sgqlc.types.ArgDict((
        ('as_of', sgqlc.types.Arg(Date, graphql_name='asOf', default=None)),
))
    )
    period_performance = sgqlc.types.Field('PeriodPerformance', graphql_name='periodPerformance', args=sgqlc.types.ArgDict((
        ('to', sgqlc.types.Arg(Date, graphql_name='to', default=None)),
        ('risk_free_rate', sgqlc.types.Arg(Float, graphql_name='riskFreeRate', default=None)),
))
    )
    correlation = sgqlc.types.Field(Float, graphql_name='correlation', args=sgqlc.types.ArgDict((
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
))
    )
    composition = sgqlc.types.Field(sgqlc.types.list_of(Composition), graphql_name='composition', args=sgqlc.types.ArgDict((
        ('scale_format', sgqlc.types.Arg(ScaleFormat, graphql_name='scaleFormat', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
))
    )
    market_impact = sgqlc.types.Field(MarketImpact, graphql_name='marketImpact', args=sgqlc.types.ArgDict((
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('scale_format', sgqlc.types.Arg(ScaleFormat, graphql_name='scaleFormat', default=None)),
))
    )
    turnover = sgqlc.types.Field('Turnover', graphql_name='turnover', args=sgqlc.types.ArgDict((
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('scale_format', sgqlc.types.Arg(ScaleFormat, graphql_name='scaleFormat', default=None)),
))
    )


class ModelPortfolio(sgqlc.types.Type):
    __schema__ = schema
    coverage = sgqlc.types.Field(sgqlc.types.list_of(Coverage), graphql_name='coverage', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
))
    )
    performance = sgqlc.types.Field(sgqlc.types.list_of('Performance'), graphql_name='performance', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('aggregation', sgqlc.types.Arg(Aggregation, graphql_name='aggregation', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
))
    )
    performance_contributors = sgqlc.types.Field(sgqlc.types.list_of('PerformanceContributor'), graphql_name='performanceContributors', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
))
    )
    grouped_performance_contributors = sgqlc.types.Field(sgqlc.types.list_of('PerformanceContributorGroup'), graphql_name='groupedPerformanceContributors', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('group_by', sgqlc.types.Arg(sgqlc.types.non_null(ContributorGroupType), graphql_name='groupBy', default=None)),
        ('classification_id', sgqlc.types.Arg(String, graphql_name='classificationId', default=None)),
        ('classification_tier', sgqlc.types.Arg(String, graphql_name='classificationTier', default=None)),
))
    )
    risk = sgqlc.types.Field(sgqlc.types.list_of('Risk'), graphql_name='risk', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
))
    )
    risk_contributors = sgqlc.types.Field(sgqlc.types.list_of('RiskContributor'), graphql_name='riskContributors', args=sgqlc.types.ArgDict((
        ('on', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='on', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
))
    )
    grouped_risk_contributors = sgqlc.types.Field(sgqlc.types.list_of('RiskContributorGroup'), graphql_name='groupedRiskContributors', args=sgqlc.types.ArgDict((
        ('on', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='on', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('group_by', sgqlc.types.Arg(sgqlc.types.non_null(ContributorGroupType), graphql_name='groupBy', default=None)),
        ('classification_id', sgqlc.types.Arg(String, graphql_name='classificationId', default=None)),
        ('classification_tier', sgqlc.types.Arg(String, graphql_name='classificationTier', default=None)),
))
    )
    exposure = sgqlc.types.Field(sgqlc.types.list_of(Exposure), graphql_name='exposure', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
        ('content_set_id', sgqlc.types.Arg(String, graphql_name='contentSetId', default=None)),
))
    )
    exposure_contributors = sgqlc.types.Field(sgqlc.types.list_of(ExposureContributorDate), graphql_name='exposureContributors', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
        ('content_set_id', sgqlc.types.Arg(String, graphql_name='contentSetId', default=None)),
))
    )
    grouped_exposure_contributors = sgqlc.types.Field(sgqlc.types.list_of(GroupedExposureContributorDate), graphql_name='groupedExposureContributors', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
        ('group_by', sgqlc.types.Arg(sgqlc.types.non_null(ContributorGroupType), graphql_name='groupBy', default=None)),
        ('content_set_id', sgqlc.types.Arg(String, graphql_name='contentSetId', default=None)),
        ('classification_id', sgqlc.types.Arg(String, graphql_name='classificationId', default=None)),
        ('classification_tier', sgqlc.types.Arg(String, graphql_name='classificationTier', default=None)),
))
    )
    beta = sgqlc.types.Field(sgqlc.types.list_of(Beta), graphql_name='beta', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
))
    )
    beta_contributors = sgqlc.types.Field(sgqlc.types.list_of(BetaContributorDate), graphql_name='betaContributors', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
))
    )
    grouped_beta_contributors = sgqlc.types.Field(sgqlc.types.list_of(GroupedBetaContributorDate), graphql_name='groupedBetaContributors', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('group_by', sgqlc.types.Arg(sgqlc.types.non_null(ContributorGroupType), graphql_name='groupBy', default=None)),
        ('classification_id', sgqlc.types.Arg(String, graphql_name='classificationId', default=None)),
        ('classification_tier', sgqlc.types.Arg(String, graphql_name='classificationTier', default=None)),
))
    )
    forecast = sgqlc.types.Field(ForecastTypes, graphql_name='forecast', args=sgqlc.types.ArgDict((
        ('on', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='on', default=None)),
        ('horizon', sgqlc.types.Arg(Int, graphql_name='horizon', default=None)),
))
    )
    period_performance = sgqlc.types.Field('PeriodPerformance', graphql_name='periodPerformance', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('risk_free_rate', sgqlc.types.Arg(Float, graphql_name='riskFreeRate', default=None)),
))
    )
    correlation = sgqlc.types.Field(Float, graphql_name='correlation', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('with_', sgqlc.types.Arg(sgqlc.types.non_null(PositionSetInput), graphql_name='with', default=None)),
))
    )
    composition = sgqlc.types.Field(sgqlc.types.list_of(Composition), graphql_name='composition', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
        ('scale_format', sgqlc.types.Arg(ScaleFormat, graphql_name='scaleFormat', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
))
    )
    market_impact = sgqlc.types.Field(MarketImpact, graphql_name='marketImpact', args=sgqlc.types.ArgDict((
        ('position_set_delta', sgqlc.types.Arg(sgqlc.types.non_null(PositionSetDateInput), graphql_name='positionSetDelta', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('scale_format', sgqlc.types.Arg(ScaleFormat, graphql_name='scaleFormat', default=None)),
))
    )


class ModelSimulation(sgqlc.types.Type):
    __schema__ = schema
    coverage = sgqlc.types.Field(sgqlc.types.list_of(Coverage), graphql_name='coverage')
    performance = sgqlc.types.Field(sgqlc.types.list_of('Performance'), graphql_name='performance', args=sgqlc.types.ArgDict((
        ('aggregation', sgqlc.types.Arg(Aggregation, graphql_name='aggregation', default=None)),
))
    )
    performance_contributors = sgqlc.types.Field(sgqlc.types.list_of('PerformanceContributor'), graphql_name='performanceContributors', args=sgqlc.types.ArgDict((
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
))
    )
    grouped_performance_contributors = sgqlc.types.Field(sgqlc.types.list_of('PerformanceContributorGroup'), graphql_name='groupedPerformanceContributors', args=sgqlc.types.ArgDict((
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('group_by', sgqlc.types.Arg(sgqlc.types.non_null(ContributorGroupType), graphql_name='groupBy', default=None)),
        ('classification_id', sgqlc.types.Arg(String, graphql_name='classificationId', default=None)),
        ('classification_tier', sgqlc.types.Arg(String, graphql_name='classificationTier', default=None)),
))
    )
    risk = sgqlc.types.Field(sgqlc.types.list_of('Risk'), graphql_name='risk')
    risk_contributors = sgqlc.types.Field(sgqlc.types.list_of('RiskContributor'), graphql_name='riskContributors', args=sgqlc.types.ArgDict((
        ('on', sgqlc.types.Arg(Date, graphql_name='on', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
))
    )
    grouped_risk_contributors = sgqlc.types.Field(sgqlc.types.list_of('RiskContributorGroup'), graphql_name='groupedRiskContributors', args=sgqlc.types.ArgDict((
        ('on', sgqlc.types.Arg(Date, graphql_name='on', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('group_by', sgqlc.types.Arg(sgqlc.types.non_null(ContributorGroupType), graphql_name='groupBy', default=None)),
        ('classification_id', sgqlc.types.Arg(String, graphql_name='classificationId', default=None)),
        ('classification_tier', sgqlc.types.Arg(String, graphql_name='classificationTier', default=None)),
))
    )
    exposure = sgqlc.types.Field(sgqlc.types.list_of(Exposure), graphql_name='exposure', args=sgqlc.types.ArgDict((
        ('content_set_id', sgqlc.types.Arg(String, graphql_name='contentSetId', default=None)),
))
    )
    exposure_contributors = sgqlc.types.Field(sgqlc.types.list_of(ExposureContributorDate), graphql_name='exposureContributors', args=sgqlc.types.ArgDict((
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('content_set_id', sgqlc.types.Arg(String, graphql_name='contentSetId', default=None)),
        ('active', sgqlc.types.Arg(ActiveContributorType, graphql_name='active', default=None)),
))
    )
    grouped_exposure_contributors = sgqlc.types.Field(sgqlc.types.list_of(GroupedExposureContributorDate), graphql_name='groupedExposureContributors', args=sgqlc.types.ArgDict((
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('group_by', sgqlc.types.Arg(sgqlc.types.non_null(ContributorGroupType), graphql_name='groupBy', default=None)),
        ('content_set_id', sgqlc.types.Arg(String, graphql_name='contentSetId', default=None)),
        ('active', sgqlc.types.Arg(ActiveContributorType, graphql_name='active', default=None)),
        ('classification_id', sgqlc.types.Arg(String, graphql_name='classificationId', default=None)),
        ('classification_tier', sgqlc.types.Arg(String, graphql_name='classificationTier', default=None)),
))
    )
    beta = sgqlc.types.Field(sgqlc.types.list_of(Beta), graphql_name='beta')
    beta_contributors = sgqlc.types.Field(sgqlc.types.list_of(BetaContributorDate), graphql_name='betaContributors', args=sgqlc.types.ArgDict((
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('active', sgqlc.types.Arg(ActiveContributorType, graphql_name='active', default=None)),
))
    )
    grouped_beta_contributors = sgqlc.types.Field(sgqlc.types.list_of(GroupedBetaContributorDate), graphql_name='groupedBetaContributors', args=sgqlc.types.ArgDict((
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('group_by', sgqlc.types.Arg(sgqlc.types.non_null(ContributorGroupType), graphql_name='groupBy', default=None)),
        ('active', sgqlc.types.Arg(ActiveContributorType, graphql_name='active', default=None)),
        ('classification_id', sgqlc.types.Arg(String, graphql_name='classificationId', default=None)),
        ('classification_tier', sgqlc.types.Arg(String, graphql_name='classificationTier', default=None)),
))
    )
    forecast = sgqlc.types.Field(ForecastTypes, graphql_name='forecast', args=sgqlc.types.ArgDict((
        ('on', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='on', default=None)),
        ('horizon', sgqlc.types.Arg(Int, graphql_name='horizon', default=None)),
))
    )
    period_performance = sgqlc.types.Field('PeriodPerformance', graphql_name='periodPerformance', args=sgqlc.types.ArgDict((
        ('risk_free_rate', sgqlc.types.Arg(Float, graphql_name='riskFreeRate', default=None)),
))
    )
    correlation = sgqlc.types.Field(Float, graphql_name='correlation', args=sgqlc.types.ArgDict((
        ('with_', sgqlc.types.Arg(sgqlc.types.non_null(PositionSetInput), graphql_name='with', default=None)),
))
    )
    composition = sgqlc.types.Field(sgqlc.types.list_of(Composition), graphql_name='composition', args=sgqlc.types.ArgDict((
        ('scale_format', sgqlc.types.Arg(ScaleFormat, graphql_name='scaleFormat', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
))
    )
    market_impact = sgqlc.types.Field(MarketImpact, graphql_name='marketImpact', args=sgqlc.types.ArgDict((
        ('position_set_delta', sgqlc.types.Arg(sgqlc.types.non_null(PositionSetDateInput), graphql_name='positionSetDelta', default=None)),
        ('equity_id_format', sgqlc.types.Arg(EquityIdFormat, graphql_name='equityIdFormat', default=None)),
        ('scale_format', sgqlc.types.Arg(ScaleFormat, graphql_name='scaleFormat', default=None)),
))
    )


class Mutation(sgqlc.types.Type):
    __schema__ = schema
    upload_content_set_date = sgqlc.types.Field('UploadContentSetResult', graphql_name='uploadContentSetDate', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('data', sgqlc.types.Arg(sgqlc.types.non_null(ContentSetDateInput), graphql_name='data', default=None)),
))
    )
    delete_content_set_dates = sgqlc.types.Field(DeleteResult, graphql_name='deleteContentSetDates', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('from_', sgqlc.types.Arg(Date, graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(Date, graphql_name='to', default=None)),
        ('all_dates', sgqlc.types.Arg(Boolean, graphql_name='allDates', default=None)),
))
    )
    upload_daily_pnl = sgqlc.types.Field('UploadDailyPnlResult', graphql_name='uploadDailyPnl', args=sgqlc.types.ArgDict((
        ('portfolio_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='portfolioId', default=None)),
        ('date', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='date', default=None)),
        ('amount', sgqlc.types.Arg(sgqlc.types.non_null(Float), graphql_name='amount', default=None)),
))
    )
    delete_daily_pnl = sgqlc.types.Field(DeleteResult, graphql_name='deleteDailyPnl', args=sgqlc.types.ArgDict((
        ('portfolio_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='portfolioId', default=None)),
        ('dates', sgqlc.types.Arg(sgqlc.types.list_of(Date), graphql_name='dates', default=None)),
        ('all_dates', sgqlc.types.Arg(Boolean, graphql_name='allDates', default=None)),
))
    )
    create_experiment = sgqlc.types.Field(Experiment, graphql_name='createExperiment', args=sgqlc.types.ArgDict((
        ('portfolio_id', sgqlc.types.Arg(String, graphql_name='portfolioId', default=None)),
        ('resource_id', sgqlc.types.Arg(String, graphql_name='resourceId', default=None)),
        ('resource_type', sgqlc.types.Arg(ResourceType, graphql_name='resourceType', default=None)),
        ('experiment', sgqlc.types.Arg(sgqlc.types.non_null(NewExperiment), graphql_name='experiment', default=None)),
))
    )
    update_experiment = sgqlc.types.Field(Experiment, graphql_name='updateExperiment', args=sgqlc.types.ArgDict((
        ('portfolio_id', sgqlc.types.Arg(String, graphql_name='portfolioId', default=None)),
        ('experiment_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='experimentId', default=None)),
        ('experiment', sgqlc.types.Arg(sgqlc.types.non_null(UpdateExperiment), graphql_name='experiment', default=None)),
))
    )
    delete_experiment = sgqlc.types.Field('SingleDeleteResult', graphql_name='deleteExperiment', args=sgqlc.types.ArgDict((
        ('portfolio_id', sgqlc.types.Arg(String, graphql_name='portfolioId', default=None)),
        ('experiment_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='experimentId', default=None)),
))
    )
    upload_experiment_date = sgqlc.types.Field('UploadPositionSetResult', graphql_name='uploadExperimentDate', args=sgqlc.types.ArgDict((
        ('portfolio_id', sgqlc.types.Arg(String, graphql_name='portfolioId', default=None)),
        ('experiment_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='experimentId', default=None)),
        ('data', sgqlc.types.Arg(sgqlc.types.non_null(PositionSetDateInput), graphql_name='data', default=None)),
))
    )
    delete_experiment_dates = sgqlc.types.Field(DeleteResult, graphql_name='deleteExperimentDates', args=sgqlc.types.ArgDict((
        ('portfolio_id', sgqlc.types.Arg(String, graphql_name='portfolioId', default=None)),
        ('experiment_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='experimentId', default=None)),
        ('from_', sgqlc.types.Arg(Date, graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(Date, graphql_name='to', default=None)),
        ('all_dates', sgqlc.types.Arg(Boolean, graphql_name='allDates', default=None)),
))
    )
    create_forecast = sgqlc.types.Field(ForecastMeta, graphql_name='createForecast', args=sgqlc.types.ArgDict((
        ('forecast', sgqlc.types.Arg(sgqlc.types.non_null(ForecastCreate), graphql_name='forecast', default=None)),
))
    )
    update_forecast = sgqlc.types.Field(ForecastMeta, graphql_name='updateForecast', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ShortId), graphql_name='id', default=None)),
        ('update', sgqlc.types.Arg(sgqlc.types.non_null(ForecastUpdate), graphql_name='update', default=None)),
))
    )
    delete_forecast = sgqlc.types.Field('SingleDeleteResult', graphql_name='deleteForecast', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ShortId), graphql_name='id', default=None)),
))
    )
    upload_forecast_securities = sgqlc.types.Field(ForecastUpdateResult, graphql_name='uploadForecastSecurities', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ShortId), graphql_name='id', default=None)),
        ('values', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ForecastSecurityInput))), graphql_name='values', default=None)),
))
    )
    delete_forecast_securities = sgqlc.types.Field(ForecastDeleteResult, graphql_name='deleteForecastSecurities', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ShortId), graphql_name='id', default=None)),
        ('values', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DeleteForecastSecurityInput))), graphql_name='values', default=None)),
))
    )
    upload_pnl_date = sgqlc.types.Field('UploadPnlResult', graphql_name='uploadPnlDate', args=sgqlc.types.ArgDict((
        ('portfolio_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='portfolioId', default=None)),
        ('data', sgqlc.types.Arg(sgqlc.types.non_null(PnlDateInput), graphql_name='data', default=None)),
))
    )
    delete_pnl_dates = sgqlc.types.Field(DeleteResult, graphql_name='deletePnlDates', args=sgqlc.types.ArgDict((
        ('portfolio_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='portfolioId', default=None)),
        ('from_', sgqlc.types.Arg(Date, graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(Date, graphql_name='to', default=None)),
        ('all_dates', sgqlc.types.Arg(Boolean, graphql_name='allDates', default=None)),
))
    )
    update_portfolio = sgqlc.types.Field('Portfolio', graphql_name='updatePortfolio', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('portfolio', sgqlc.types.Arg(sgqlc.types.non_null(PortfolioUpdate), graphql_name='portfolio', default=None)),
))
    )
    create_portfolio = sgqlc.types.Field('Portfolio', graphql_name='createPortfolio', args=sgqlc.types.ArgDict((
        ('portfolio', sgqlc.types.Arg(sgqlc.types.non_null(NewPortfolio), graphql_name='portfolio', default=None)),
))
    )
    delete_portfolio = sgqlc.types.Field('SingleDeleteResult', graphql_name='deletePortfolio', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
))
    )
    upload_position_set_date = sgqlc.types.Field('UploadPositionSetResult', graphql_name='uploadPositionSetDate', args=sgqlc.types.ArgDict((
        ('portfolio_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='portfolioId', default=None)),
        ('data', sgqlc.types.Arg(sgqlc.types.non_null(PositionSetDateInput), graphql_name='data', default=None)),
))
    )
    delete_position_set_dates = sgqlc.types.Field(DeleteResult, graphql_name='deletePositionSetDates', args=sgqlc.types.ArgDict((
        ('portfolio_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='portfolioId', default=None)),
        ('dates', sgqlc.types.Arg(sgqlc.types.list_of(Date), graphql_name='dates', default=None)),
        ('from_', sgqlc.types.Arg(Date, graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(Date, graphql_name='to', default=None)),
        ('all_dates', sgqlc.types.Arg(Boolean, graphql_name='allDates', default=None)),
        ('delete_related_pnl', sgqlc.types.Arg(Boolean, graphql_name='deleteRelatedPnl', default=None)),
))
    )
    create_research_topic = sgqlc.types.Field('ResearchTopic', graphql_name='createResearchTopic', args=sgqlc.types.ArgDict((
        ('research_topic', sgqlc.types.Arg(sgqlc.types.non_null(NewResearchTopic), graphql_name='researchTopic', default=None)),
))
    )
    update_research_topic = sgqlc.types.Field('ResearchTopic', graphql_name='updateResearchTopic', args=sgqlc.types.ArgDict((
        ('research_topic_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='researchTopicId', default=None)),
        ('research_topic', sgqlc.types.Arg(sgqlc.types.non_null(UpdateResearchTopic), graphql_name='researchTopic', default=None)),
))
    )
    delete_research_topic = sgqlc.types.Field('SingleDeleteResult', graphql_name='deleteResearchTopic', args=sgqlc.types.ArgDict((
        ('research_topic_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='researchTopicId', default=None)),
))
    )
    create_swap = sgqlc.types.Field('Swap', graphql_name='createSwap', args=sgqlc.types.ArgDict((
        ('swap', sgqlc.types.Arg(sgqlc.types.non_null(NewSwap), graphql_name='swap', default=None)),
))
    )
    update_swap = sgqlc.types.Field('Swap', graphql_name='updateSwap', args=sgqlc.types.ArgDict((
        ('ticker', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='ticker', default=None)),
        ('swap', sgqlc.types.Arg(sgqlc.types.non_null(SwapUpdate), graphql_name='swap', default=None)),
))
    )
    delete_swap = sgqlc.types.Field('SingleDeleteResult', graphql_name='deleteSwap', args=sgqlc.types.ArgDict((
        ('ticker', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='ticker', default=None)),
))
    )
    upload_swap_date = sgqlc.types.Field('UploadPositionSetResult', graphql_name='uploadSwapDate', args=sgqlc.types.ArgDict((
        ('ticker', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='ticker', default=None)),
        ('data', sgqlc.types.Arg(sgqlc.types.non_null(PositionSetDateInput), graphql_name='data', default=None)),
))
    )
    delete_swap_dates = sgqlc.types.Field(DeleteResult, graphql_name='deleteSwapDates', args=sgqlc.types.ArgDict((
        ('ticker', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='ticker', default=None)),
        ('from_', sgqlc.types.Arg(Date, graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(Date, graphql_name='to', default=None)),
        ('all_dates', sgqlc.types.Arg(Boolean, graphql_name='allDates', default=None)),
))
    )
    create_watchlist = sgqlc.types.Field('WatchlistMeta', graphql_name='createWatchlist', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
        ('description', sgqlc.types.Arg(String, graphql_name='description', default=None)),
        ('alias', sgqlc.types.Arg(String, graphql_name='alias', default=None)),
))
    )
    delete_watchlist = sgqlc.types.Field('SingleDeleteResult', graphql_name='deleteWatchlist', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
))
    )
    update_watchlist = sgqlc.types.Field('WatchlistMeta', graphql_name='updateWatchlist', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('update', sgqlc.types.Arg(sgqlc.types.non_null(WatchlistUpdate), graphql_name='update', default=None)),
))
    )
    add_watchlist_securities = sgqlc.types.Field('Watchlist', graphql_name='addWatchlistSecurities', args=sgqlc.types.ArgDict((
        ('watchlist_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='watchlistId', default=None)),
        ('securities', sgqlc.types.Arg(sgqlc.types.non_null(WatchlistSecuritiesInput), graphql_name='securities', default=None)),
        ('as_of', sgqlc.types.Arg(Date, graphql_name='asOf', default=None)),
))
    )
    remove_watchlist_securities = sgqlc.types.Field('Watchlist', graphql_name='removeWatchlistSecurities', args=sgqlc.types.ArgDict((
        ('watchlist_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='watchlistId', default=None)),
        ('securities', sgqlc.types.Arg(sgqlc.types.non_null(WatchlistSecuritiesInput), graphql_name='securities', default=None)),
))
    )
    clear_watchlist_securities = sgqlc.types.Field('Watchlist', graphql_name='clearWatchlistSecurities', args=sgqlc.types.ArgDict((
        ('watchlist_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='watchlistId', default=None)),
))
    )


class OptimizationMeta(sgqlc.types.Type):
    __schema__ = schema
    burst_enabled = sgqlc.types.Field(Boolean, graphql_name='burstEnabled')


class OptimizationPositionsDelta(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    equities = sgqlc.types.Field(sgqlc.types.list_of('PositionSetEquity'), graphql_name='equities')
    swaps = sgqlc.types.Field(sgqlc.types.list_of('PositionSetOtherAsset'), graphql_name='swaps')


class OptimizedPositionSet(sgqlc.types.Type):
    __schema__ = schema
    dates = sgqlc.types.Field(sgqlc.types.list_of('PositionSetDate'), graphql_name='dates')


class Performance(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    rolled_over_from = sgqlc.types.Field(Date, graphql_name='rolledOverFrom')
    percent_return_cumulative = sgqlc.types.Field('PerformanceItem', graphql_name='percentReturnCumulative')


class PerformanceAttribution(sgqlc.types.Type):
    __schema__ = schema
    summary = sgqlc.types.Field('PerformanceAttributionSummary', graphql_name='summary')
    factors = sgqlc.types.Field(sgqlc.types.list_of('PerformanceAttributionFactor'), graphql_name='factors', args=sgqlc.types.ArgDict((
        ('category', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='category', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='id', default=None)),
))
    )


class PerformanceAttributionFactor(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    category = sgqlc.types.Field(String, graphql_name='category')
    value = sgqlc.types.Field(Float, graphql_name='value')


class PerformanceAttributionSummary(sgqlc.types.Type):
    __schema__ = schema
    trading = sgqlc.types.Field(Float, graphql_name='trading')
    factors = sgqlc.types.Field(Float, graphql_name='factors')
    specific = sgqlc.types.Field(Float, graphql_name='specific')


class PerformanceContributor(sgqlc.types.Type):
    __schema__ = schema
    asset_class = sgqlc.types.Field(String, graphql_name='assetClass')
    asset_subclass = sgqlc.types.Field(String, graphql_name='assetSubclass')
    id = sgqlc.types.Field(String, graphql_name='id')
    country = sgqlc.types.Field(String, graphql_name='country')
    currency = sgqlc.types.Field(String, graphql_name='currency')
    sector = sgqlc.types.Field(String, graphql_name='sector')
    classification = sgqlc.types.Field('SecurityClassification', graphql_name='classification', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('tier', sgqlc.types.Arg(String, graphql_name='tier', default=None)),
))
    )
    description = sgqlc.types.Field(String, graphql_name='description')
    sedol = sgqlc.types.Field(Sedol, graphql_name='sedol')
    isin = sgqlc.types.Field(Isin, graphql_name='isin')
    cusip = sgqlc.types.Field(Cusip, graphql_name='cusip')
    average_percent_equity = sgqlc.types.Field(Float, graphql_name='averagePercentEquity')
    total = sgqlc.types.Field(Float, graphql_name='total')
    attribution = sgqlc.types.Field('PerformanceContributorAttribution', graphql_name='attribution')


class PerformanceContributorAttribution(sgqlc.types.Type):
    __schema__ = schema
    summary = sgqlc.types.Field('PerformanceContributorAttributionSummary', graphql_name='summary')
    factors = sgqlc.types.Field(sgqlc.types.list_of('PerformanceContributorAttributionFactor'), graphql_name='factors')


class PerformanceContributorAttributionFactor(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    category = sgqlc.types.Field(String, graphql_name='category')
    value = sgqlc.types.Field(Float, graphql_name='value')


class PerformanceContributorAttributionSummary(sgqlc.types.Type):
    __schema__ = schema
    factors = sgqlc.types.Field(Float, graphql_name='factors')
    specific = sgqlc.types.Field(Float, graphql_name='specific')
    trading = sgqlc.types.Field(Float, graphql_name='trading')


class PerformanceContributorGroup(sgqlc.types.Type):
    __schema__ = schema
    name = sgqlc.types.Field(String, graphql_name='name')
    id = sgqlc.types.Field(String, graphql_name='id')
    total = sgqlc.types.Field(Float, graphql_name='total')
    contributors = sgqlc.types.Field(sgqlc.types.list_of(PerformanceContributor), graphql_name='contributors')
    attribution = sgqlc.types.Field(PerformanceContributorAttribution, graphql_name='attribution')
    average_percent_equity = sgqlc.types.Field(Float, graphql_name='averagePercentEquity')


class PerformanceItem(sgqlc.types.Type):
    __schema__ = schema
    total = sgqlc.types.Field(Float, graphql_name='total')
    attribution = sgqlc.types.Field(PerformanceAttribution, graphql_name='attribution')


class PeriodPerformance(sgqlc.types.Type):
    __schema__ = schema
    annualized_returns = sgqlc.types.Field(Float, graphql_name='annualizedReturns')
    annualized_volatility = sgqlc.types.Field(Float, graphql_name='annualizedVolatility')
    information_ratio = sgqlc.types.Field(Float, graphql_name='informationRatio')
    sortino_ratio = sgqlc.types.Field(Float, graphql_name='sortinoRatio')
    max_drawdown = sgqlc.types.Field(MaxDrawdown, graphql_name='maxDrawdown')


class PnlDate(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(sgqlc.types.non_null(Date), graphql_name='date')
    equities = sgqlc.types.Field(sgqlc.types.list_of('PnlEquity'), graphql_name='equities')
    currencies = sgqlc.types.Field(sgqlc.types.list_of('PnlOtherAsset'), graphql_name='currencies')
    swaps = sgqlc.types.Field(sgqlc.types.list_of('PnlOtherAsset'), graphql_name='swaps')
    fixed_income = sgqlc.types.Field(sgqlc.types.list_of('PnlFixedIncome'), graphql_name='fixedIncome')
    commodities = sgqlc.types.Field(sgqlc.types.list_of('PnlOtherAsset'), graphql_name='commodities')
    indices = sgqlc.types.Field(sgqlc.types.list_of('PnlOtherAsset'), graphql_name='indices')
    other_assets = sgqlc.types.Field(sgqlc.types.list_of('PnlOtherAsset'), graphql_name='otherAssets')


class PnlEquity(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field('PositionSetEquityId', graphql_name='id')
    amount = sgqlc.types.Field(Float, graphql_name='amount')


class PnlFixedIncome(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field('PositionSetFixedIncomeId', graphql_name='id')
    amount = sgqlc.types.Field(Float, graphql_name='amount')


class PnlOtherAsset(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    amount = sgqlc.types.Field(Float, graphql_name='amount')


class Portfolio(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    default_model_id = sgqlc.types.Field(String, graphql_name='defaultModelId')
    available_from = sgqlc.types.Field(Date, graphql_name='availableFrom')
    dates = sgqlc.types.Field(sgqlc.types.list_of('PositionSetDate'), graphql_name='dates', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
        ('model_id', sgqlc.types.Arg(String, graphql_name='modelId', default=None)),
))
    )
    daily_pnl = sgqlc.types.Field(sgqlc.types.list_of(DailyPnlDate), graphql_name='dailyPnl', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
))
    )
    per_security_pnl = sgqlc.types.Field(sgqlc.types.list_of(PnlDate), graphql_name='perSecurityPnl', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
))
    )
    experiments = sgqlc.types.Field(sgqlc.types.list_of(ExperimentMetadata), graphql_name='experiments', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(ExperimentType, graphql_name='type', default=None)),
))
    )
    experiment = sgqlc.types.Field(Experiment, graphql_name='experiment', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
))
    )
    rollover_position_set_to_current_date = sgqlc.types.Field(Boolean, graphql_name='rolloverPositionSetToCurrentDate')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')


class PortfolioMetadata(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    available_from = sgqlc.types.Field(Date, graphql_name='availableFrom')
    rollover_position_set_to_current_date = sgqlc.types.Field(Boolean, graphql_name='rolloverPositionSetToCurrentDate')
    model_id = sgqlc.types.Field(String, graphql_name='modelId')
    default_model_id = sgqlc.types.Field(String, graphql_name='defaultModelId')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')


class PositionSetDate(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    equity = sgqlc.types.Field(Float, graphql_name='equity')
    gmv = sgqlc.types.Field(Float, graphql_name='gmv')
    long_market_value = sgqlc.types.Field(Float, graphql_name='longMarketValue')
    short_market_value = sgqlc.types.Field(Float, graphql_name='shortMarketValue')
    rolled_over_from = sgqlc.types.Field(Date, graphql_name='rolledOverFrom')
    equities = sgqlc.types.Field(sgqlc.types.list_of('PositionSetEquity'), graphql_name='equities')
    currencies = sgqlc.types.Field(sgqlc.types.list_of('PositionSetOtherAsset'), graphql_name='currencies')
    swaps = sgqlc.types.Field(sgqlc.types.list_of('PositionSetOtherAsset'), graphql_name='swaps')
    fixed_income = sgqlc.types.Field(sgqlc.types.list_of('PositionSetFixedIncome'), graphql_name='fixedIncome')
    commodities = sgqlc.types.Field(sgqlc.types.list_of('PositionSetOtherAsset'), graphql_name='commodities')
    indices = sgqlc.types.Field(sgqlc.types.list_of('PositionSetOtherAsset'), graphql_name='indices')
    other_assets = sgqlc.types.Field(sgqlc.types.list_of('PositionSetOtherAsset'), graphql_name='otherAssets')


class PositionSetEquity(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field('PositionSetEquityId', graphql_name='id')
    economic_exposure = sgqlc.types.Field(Float, graphql_name='economicExposure')
    country = sgqlc.types.Field(String, graphql_name='country')
    currency = sgqlc.types.Field(String, graphql_name='currency')
    sector = sgqlc.types.Field(String, graphql_name='sector')
    classification = sgqlc.types.Field('SecurityClassification', graphql_name='classification', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('tier', sgqlc.types.Arg(String, graphql_name='tier', default=None)),
))
    )
    trade_as_percent_adv = sgqlc.types.Field(Float, graphql_name='tradeAsPercentADV')


class PositionSetEquityId(sgqlc.types.Type):
    __schema__ = schema
    ticker = sgqlc.types.Field(String, graphql_name='ticker')
    mic = sgqlc.types.Field(String, graphql_name='mic')
    sedol = sgqlc.types.Field(Sedol, graphql_name='sedol')
    isin = sgqlc.types.Field(Isin, graphql_name='isin')
    cusip = sgqlc.types.Field(Cusip, graphql_name='cusip')
    model_provider_id = sgqlc.types.Field(String, graphql_name='modelProviderId')


class PositionSetFixedIncome(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field('PositionSetFixedIncomeId', graphql_name='id')
    economic_exposure = sgqlc.types.Field(Float, graphql_name='economicExposure')


class PositionSetFixedIncomeId(sgqlc.types.Type):
    __schema__ = schema
    isin = sgqlc.types.Field(Isin, graphql_name='isin')


class PositionSetOtherAsset(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    economic_exposure = sgqlc.types.Field(Float, graphql_name='economicExposure')


class Query(sgqlc.types.Type):
    __schema__ = schema
    benchmarks = sgqlc.types.Field(sgqlc.types.list_of(BenchmarkMetadata), graphql_name='benchmarks')
    classifications = sgqlc.types.Field(sgqlc.types.list_of(ClassificationMetadata), graphql_name='classifications')
    classification = sgqlc.types.Field(Classification, graphql_name='classification', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
))
    )
    content_sets = sgqlc.types.Field(sgqlc.types.list_of(ContentSetMetadata), graphql_name='contentSets')
    content_set = sgqlc.types.Field(ContentSet, graphql_name='contentSet', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
))
    )
    daily_pnl = sgqlc.types.Field(sgqlc.types.list_of(DailyPnlDate), graphql_name='dailyPnl', args=sgqlc.types.ArgDict((
        ('portfolio_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='portfolioId', default=None)),
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
))
    )
    forecasts = sgqlc.types.Field(sgqlc.types.list_of(ForecastMeta), graphql_name='forecasts')
    forecast = sgqlc.types.Field(ForecastDetails, graphql_name='forecast', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ShortId), graphql_name='id', default=None)),
))
    )
    meta = sgqlc.types.Field(Meta, graphql_name='meta')
    model = sgqlc.types.Field(Model, graphql_name='model', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
))
    )
    models = sgqlc.types.Field(sgqlc.types.list_of(ModelMetadata), graphql_name='models')
    portfolios = sgqlc.types.Field(sgqlc.types.list_of(PortfolioMetadata), graphql_name='portfolios')
    portfolio = sgqlc.types.Field(Portfolio, graphql_name='portfolio', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
))
    )
    research_topics = sgqlc.types.Field(sgqlc.types.list_of('ResearchTopicMetadata'), graphql_name='researchTopics')
    research_topic = sgqlc.types.Field('ResearchTopic', graphql_name='researchTopic', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
))
    )
    swaps = sgqlc.types.Field(sgqlc.types.list_of('SwapMetadata'), graphql_name='swaps')
    swap = sgqlc.types.Field('Swap', graphql_name='swap', args=sgqlc.types.ArgDict((
        ('ticker', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='ticker', default=None)),
))
    )
    watchlists = sgqlc.types.Field(sgqlc.types.list_of('WatchlistMeta'), graphql_name='watchlists')
    watchlist = sgqlc.types.Field('Watchlist', graphql_name='watchlist', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
))
    )


class ReferenceInstrument(sgqlc.types.Type):
    __schema__ = schema
    type = sgqlc.types.Field(ReferenceInstrumentType, graphql_name='type')
    security_id = sgqlc.types.Field('UniversalId', graphql_name='securityId')


class ResearchTopic(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    reference_instrument = sgqlc.types.Field(ReferenceInstrument, graphql_name='referenceInstrument')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')
    experiments = sgqlc.types.Field(sgqlc.types.list_of(ExperimentMetadata), graphql_name='experiments', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(ExperimentType, graphql_name='type', default=None)),
))
    )
    experiment = sgqlc.types.Field(Experiment, graphql_name='experiment', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
))
    )


class ResearchTopicMetadata(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    reference_instrument = sgqlc.types.Field(ReferenceInstrument, graphql_name='referenceInstrument')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')


class Risk(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    rolled_over_from = sgqlc.types.Field(Date, graphql_name='rolledOverFrom')
    total = sgqlc.types.Field(Float, graphql_name='total')
    attribution = sgqlc.types.Field('RiskAttribution', graphql_name='attribution')


class RiskAttribution(sgqlc.types.Type):
    __schema__ = schema
    summary = sgqlc.types.Field('RiskAttributionSummary', graphql_name='summary')
    factors = sgqlc.types.Field(sgqlc.types.list_of('RiskAttributionFactor'), graphql_name='factors', args=sgqlc.types.ArgDict((
        ('category', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='category', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='id', default=None)),
))
    )


class RiskAttributionFactor(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    category = sgqlc.types.Field(String, graphql_name='category')
    value = sgqlc.types.Field(Float, graphql_name='value')


class RiskAttributionSummary(sgqlc.types.Type):
    __schema__ = schema
    factors = sgqlc.types.Field(Float, graphql_name='factors')
    specific = sgqlc.types.Field(Float, graphql_name='specific')


class RiskContributor(sgqlc.types.Type):
    __schema__ = schema
    asset_class = sgqlc.types.Field(String, graphql_name='assetClass')
    asset_subclass = sgqlc.types.Field(String, graphql_name='assetSubclass')
    id = sgqlc.types.Field(String, graphql_name='id')
    country = sgqlc.types.Field(String, graphql_name='country')
    currency = sgqlc.types.Field(String, graphql_name='currency')
    sector = sgqlc.types.Field(String, graphql_name='sector')
    classification = sgqlc.types.Field('SecurityClassification', graphql_name='classification', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('tier', sgqlc.types.Arg(String, graphql_name='tier', default=None)),
))
    )
    description = sgqlc.types.Field(String, graphql_name='description')
    sedol = sgqlc.types.Field(Sedol, graphql_name='sedol')
    isin = sgqlc.types.Field(Isin, graphql_name='isin')
    cusip = sgqlc.types.Field(Cusip, graphql_name='cusip')
    percent_equity = sgqlc.types.Field(Float, graphql_name='percentEquity')
    total = sgqlc.types.Field(Float, graphql_name='total')
    attribution = sgqlc.types.Field('RiskContributorAttribution', graphql_name='attribution')


class RiskContributorAttribution(sgqlc.types.Type):
    __schema__ = schema
    summary = sgqlc.types.Field('RiskContributorAttributionSummary', graphql_name='summary')
    factors = sgqlc.types.Field(sgqlc.types.list_of('RiskContributorAttributionFactor'), graphql_name='factors')


class RiskContributorAttributionFactor(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    category = sgqlc.types.Field(String, graphql_name='category')
    value = sgqlc.types.Field(Float, graphql_name='value')


class RiskContributorAttributionSummary(sgqlc.types.Type):
    __schema__ = schema
    factors = sgqlc.types.Field(Float, graphql_name='factors')
    specific = sgqlc.types.Field(Float, graphql_name='specific')


class RiskContributorGroup(sgqlc.types.Type):
    __schema__ = schema
    name = sgqlc.types.Field(String, graphql_name='name')
    id = sgqlc.types.Field(String, graphql_name='id')
    total_percent_equity = sgqlc.types.Field(Float, graphql_name='totalPercentEquity')
    contributors = sgqlc.types.Field(sgqlc.types.list_of(RiskContributor), graphql_name='contributors')
    attribution = sgqlc.types.Field(RiskContributorAttribution, graphql_name='attribution')


class SearchResultFacet(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    count = sgqlc.types.Field(Int, graphql_name='count')


class Security(sgqlc.types.Type):
    __schema__ = schema
    descriptors = sgqlc.types.Field('SecurityDescriptors', graphql_name='descriptors', args=sgqlc.types.ArgDict((
        ('on', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='on', default=None)),
))
    )
    classification = sgqlc.types.Field('SecurityClassification', graphql_name='classification', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('on', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='on', default=None)),
        ('tier', sgqlc.types.Arg(String, graphql_name='tier', default=None)),
))
    )
    availability = sgqlc.types.Field('SecurityAvailability', graphql_name='availability')
    performance = sgqlc.types.Field(sgqlc.types.list_of('SecurityPerformance'), graphql_name='performance', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('aggregation', sgqlc.types.Arg(Aggregation, graphql_name='aggregation', default=None)),
        ('interval', sgqlc.types.Arg(Interval, graphql_name='interval', default=None)),
))
    )
    exposure = sgqlc.types.Field(sgqlc.types.list_of('SecurityExposure'), graphql_name='exposure', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(Interval, graphql_name='interval', default=None)),
        ('content_set_id', sgqlc.types.Arg(String, graphql_name='contentSetId', default=None)),
))
    )
    risk = sgqlc.types.Field(sgqlc.types.list_of('SecurityPredictedRisk'), graphql_name='risk', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(Interval, graphql_name='interval', default=None)),
))
    )
    beta = sgqlc.types.Field(sgqlc.types.list_of('SecurityBeta'), graphql_name='beta', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(Interval, graphql_name='interval', default=None)),
))
    )


class SecurityAvailability(sgqlc.types.Type):
    __schema__ = schema
    from_ = sgqlc.types.Field(Date, graphql_name='from')
    to = sgqlc.types.Field(Date, graphql_name='to')


class SecurityBeta(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    predicted = sgqlc.types.Field(Float, graphql_name='predicted')
    historical = sgqlc.types.Field(Float, graphql_name='historical')


class SecurityClassification(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')


class SecurityDescriptor(sgqlc.types.Type):
    __schema__ = schema
    code = sgqlc.types.Field(String, graphql_name='code')
    description = sgqlc.types.Field(String, graphql_name='description')


class SecurityDescriptors(sgqlc.types.Type):
    __schema__ = schema
    name = sgqlc.types.Field(String, graphql_name='name')
    ticker = sgqlc.types.Field(String, graphql_name='ticker')
    mic = sgqlc.types.Field(String, graphql_name='mic')
    exchange = sgqlc.types.Field(String, graphql_name='exchange')
    country = sgqlc.types.Field(String, graphql_name='country')
    currency = sgqlc.types.Field(String, graphql_name='currency')
    sector = sgqlc.types.Field(String, graphql_name='sector')
    model_provider_id = sgqlc.types.Field(String, graphql_name='modelProviderId')
    asset_class = sgqlc.types.Field(String, graphql_name='assetClass')
    asset_subclass = sgqlc.types.Field(String, graphql_name='assetSubclass')
    sedol = sgqlc.types.Field(Sedol, graphql_name='sedol')
    isin = sgqlc.types.Field(Isin, graphql_name='isin')
    cusip = sgqlc.types.Field(Cusip, graphql_name='cusip')
    average_daily_volume = sgqlc.types.Field(Float, graphql_name='averageDailyVolume')
    market_cap = sgqlc.types.Field(Float, graphql_name='marketCap')


class SecurityExposure(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    factors = sgqlc.types.Field(sgqlc.types.list_of('SecurityExposureFactor'), graphql_name='factors', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='id', default=None)),
        ('category', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='category', default=None)),
))
    )


class SecurityExposureFactor(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    category = sgqlc.types.Field(String, graphql_name='category')
    z_score = sgqlc.types.Field(Float, graphql_name='zScore')


class SecurityPerformance(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    percent_price_change_cumulative = sgqlc.types.Field('SecurityPerformanceItem', graphql_name='percentPriceChangeCumulative')


class SecurityPerformanceAttribution(sgqlc.types.Type):
    __schema__ = schema
    summary = sgqlc.types.Field('SecurityPerformanceAttributionSummary', graphql_name='summary')
    factors = sgqlc.types.Field(sgqlc.types.list_of('SecurityPerformanceAttributionFactor'), graphql_name='factors', args=sgqlc.types.ArgDict((
        ('category', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='category', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='id', default=None)),
))
    )


class SecurityPerformanceAttributionFactor(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    category = sgqlc.types.Field(String, graphql_name='category')
    value = sgqlc.types.Field(Float, graphql_name='value')


class SecurityPerformanceAttributionSummary(sgqlc.types.Type):
    __schema__ = schema
    factors = sgqlc.types.Field(Float, graphql_name='factors')
    specific = sgqlc.types.Field(Float, graphql_name='specific')


class SecurityPerformanceItem(sgqlc.types.Type):
    __schema__ = schema
    total = sgqlc.types.Field(Float, graphql_name='total')
    attribution = sgqlc.types.Field(SecurityPerformanceAttribution, graphql_name='attribution')


class SecurityPredictedRisk(sgqlc.types.Type):
    __schema__ = schema
    date = sgqlc.types.Field(Date, graphql_name='date')
    total = sgqlc.types.Field(Float, graphql_name='total')
    attribution = sgqlc.types.Field(RiskAttribution, graphql_name='attribution')


class SecurityResult(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    sedol = sgqlc.types.Field(String, graphql_name='sedol')
    asset_class = sgqlc.types.Field(String, graphql_name='assetClass')
    asset_subclass = sgqlc.types.Field(String, graphql_name='assetSubclass')
    ticker = sgqlc.types.Field(String, graphql_name='ticker')
    mic = sgqlc.types.Field(String, graphql_name='mic')
    description = sgqlc.types.Field(String, graphql_name='description')
    average_daily_volume = sgqlc.types.Field(Float, graphql_name='averageDailyVolume')
    market_capitalization = sgqlc.types.Field(Float, graphql_name='marketCapitalization')
    country = sgqlc.types.Field(String, graphql_name='country')
    sector = sgqlc.types.Field(String, graphql_name='sector')
    classification = sgqlc.types.Field(SecurityClassification, graphql_name='classification', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('tier', sgqlc.types.Arg(String, graphql_name='tier', default=None)),
))
    )
    currency = sgqlc.types.Field(String, graphql_name='currency')
    model_provider_id = sgqlc.types.Field(String, graphql_name='modelProviderId')
    factor_exposure = sgqlc.types.Field(sgqlc.types.list_of(SecurityExposureFactor), graphql_name='factorExposure', args=sgqlc.types.ArgDict((
        ('content_set_id', sgqlc.types.Arg(String, graphql_name='contentSetId', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='id', default=None)),
        ('category', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='category', default=None)),
))
    )
    risk = sgqlc.types.Field('SecurityRisk', graphql_name='risk')
    beta = sgqlc.types.Field('SecurityResultBeta', graphql_name='beta')


class SecurityResultBeta(sgqlc.types.Type):
    __schema__ = schema
    predicted = sgqlc.types.Field(Float, graphql_name='predicted')
    historical = sgqlc.types.Field(Float, graphql_name='historical')


class SecurityRisk(sgqlc.types.Type):
    __schema__ = schema
    standard_deviation = sgqlc.types.Field('SecurityRiskStandardDeviation', graphql_name='standardDeviation')
    variance_decomposition = sgqlc.types.Field('SecurityRiskVarianceDecomposition', graphql_name='varianceDecomposition')


class SecurityRiskStandardDeviation(sgqlc.types.Type):
    __schema__ = schema
    total = sgqlc.types.Field(Float, graphql_name='total')


class SecurityRiskVarianceDecomposition(sgqlc.types.Type):
    __schema__ = schema
    summary = sgqlc.types.Field('SecurityRiskVarianceDecompositionSummary', graphql_name='summary')


class SecurityRiskVarianceDecompositionSummary(sgqlc.types.Type):
    __schema__ = schema
    specific = sgqlc.types.Field(Float, graphql_name='specific')
    factors = sgqlc.types.Field(Float, graphql_name='factors')


class SecuritySearchResult(sgqlc.types.Type):
    __schema__ = schema
    securities = sgqlc.types.Field(sgqlc.types.list_of(SecurityResult), graphql_name='securities')
    count = sgqlc.types.Field(Int, graphql_name='count')
    countries = sgqlc.types.Field(sgqlc.types.list_of(SearchResultFacet), graphql_name='countries')
    currencies = sgqlc.types.Field(sgqlc.types.list_of(SearchResultFacet), graphql_name='currencies')
    sectors = sgqlc.types.Field(sgqlc.types.list_of(SearchResultFacet), graphql_name='sectors')
    classification = sgqlc.types.Field(sgqlc.types.list_of(SearchResultFacet), graphql_name='classification', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
))
    )


class SingleDeleteResult(sgqlc.types.Type):
    __schema__ = schema
    ok = sgqlc.types.Field(Boolean, graphql_name='ok')


class Swap(sgqlc.types.Type):
    __schema__ = schema
    ticker = sgqlc.types.Field(String, graphql_name='ticker')
    description = sgqlc.types.Field(String, graphql_name='description')
    available_from = sgqlc.types.Field(Date, graphql_name='availableFrom')
    termination_date = sgqlc.types.Field(Date, graphql_name='terminationDate')
    dates = sgqlc.types.Field(sgqlc.types.list_of(PositionSetDate), graphql_name='dates', args=sgqlc.types.ArgDict((
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(Date), graphql_name='to', default=None)),
        ('interval', sgqlc.types.Arg(PositionSetInterval, graphql_name='interval', default=None)),
        ('model_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='modelId', default=None)),
))
    )
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')


class SwapMetadata(sgqlc.types.Type):
    __schema__ = schema
    ticker = sgqlc.types.Field(String, graphql_name='ticker')
    description = sgqlc.types.Field(String, graphql_name='description')
    available_from = sgqlc.types.Field(Date, graphql_name='availableFrom')
    termination_date = sgqlc.types.Field(Date, graphql_name='terminationDate')
    dates = sgqlc.types.Field(sgqlc.types.list_of(Date), graphql_name='dates')
    last_updated = sgqlc.types.Field(DateTime, graphql_name='lastUpdated')


class Turnover(sgqlc.types.Type):
    __schema__ = schema
    total = sgqlc.types.Field(Float, graphql_name='total')
    contributors = sgqlc.types.Field(sgqlc.types.list_of('TurnoverContributor'), graphql_name='contributors')


class TurnoverContributor(sgqlc.types.Type):
    __schema__ = schema
    asset_class = sgqlc.types.Field(String, graphql_name='assetClass')
    asset_subclass = sgqlc.types.Field(String, graphql_name='assetSubclass')
    id = sgqlc.types.Field(String, graphql_name='id')
    country = sgqlc.types.Field(String, graphql_name='country')
    currency = sgqlc.types.Field(String, graphql_name='currency')
    classification = sgqlc.types.Field(SecurityClassification, graphql_name='classification', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='id', default=None)),
        ('tier', sgqlc.types.Arg(String, graphql_name='tier', default=None)),
))
    )
    value = sgqlc.types.Field(Float, graphql_name='value')


class UniversalId(sgqlc.types.Type):
    __schema__ = schema
    sedol = sgqlc.types.Field(String, graphql_name='sedol')
    isin = sgqlc.types.Field(String, graphql_name='isin')
    ticker = sgqlc.types.Field(String, graphql_name='ticker')
    mic = sgqlc.types.Field(String, graphql_name='mic')
    country = sgqlc.types.Field(String, graphql_name='country')


class UploadContentSetResult(sgqlc.types.Type):
    __schema__ = schema
    ok = sgqlc.types.Field(Boolean, graphql_name='ok')


class UploadDailyPnlResult(sgqlc.types.Type):
    __schema__ = schema
    ok = sgqlc.types.Field(Boolean, graphql_name='ok')


class UploadPnlResult(sgqlc.types.Type):
    __schema__ = schema
    ok = sgqlc.types.Field(Boolean, graphql_name='ok')


class UploadPositionSetResult(sgqlc.types.Type):
    __schema__ = schema
    ok = sgqlc.types.Field(Boolean, graphql_name='ok')
    coverage = sgqlc.types.Field(Coverage, graphql_name='coverage', args=sgqlc.types.ArgDict((
        ('model_id', sgqlc.types.Arg(String, graphql_name='modelId', default=None)),
))
    )


class Watchlist(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    count = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='count')
    last_updated = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastUpdated')
    equities = sgqlc.types.Field(sgqlc.types.list_of('WatchlistEquity'), graphql_name='equities')
    currencies = sgqlc.types.Field(sgqlc.types.list_of('WatchlistOtherAsset'), graphql_name='currencies')
    swaps = sgqlc.types.Field(sgqlc.types.list_of('WatchlistOtherAsset'), graphql_name='swaps')
    fixed_income = sgqlc.types.Field(sgqlc.types.list_of('WatchlistFixedIncome'), graphql_name='fixedIncome')
    commodities = sgqlc.types.Field(sgqlc.types.list_of('WatchlistOtherAsset'), graphql_name='commodities')
    indices = sgqlc.types.Field(sgqlc.types.list_of('WatchlistOtherAsset'), graphql_name='indices')


class WatchlistEquity(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(PositionSetEquityId, graphql_name='id')
    added_on = sgqlc.types.Field(Date, graphql_name='addedOn')


class WatchlistFixedIncome(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(PositionSetFixedIncomeId, graphql_name='id')
    added_on = sgqlc.types.Field(Date, graphql_name='addedOn')


class WatchlistMeta(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    count = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='count')
    last_updated = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastUpdated')


class WatchlistOtherAsset(sgqlc.types.Type):
    __schema__ = schema
    id = sgqlc.types.Field(String, graphql_name='id')
    added_on = sgqlc.types.Field(Date, graphql_name='addedOn')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
schema.query_type = Query
schema.mutation_type = Mutation
schema.subscription_type = None

