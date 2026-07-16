SCREEN_WIDTH = 1980
SCREEN_HEIGHT = 1080
FPS = 60

# Career timeline
SEASON_START_YEAR = 2026

# Colors
BLACK = (20, 20, 24)
WHITE = (240, 240, 240)
GREY = (90, 96, 104)
ACCENT = (200, 200, 255)
GOOD = (80, 200, 140)
BAD = (220, 90, 90)
WARN = (255, 210, 80)

# Driver hiring rules
MIN_DRIVER_SIGNING_AGE = 18


# Fixed entry cost for participating in the season\'s official pre-season
# testing programme. Charged once after the final pre-season test concludes.
PRESEASON_TESTING_ENTRY_COST_M = 3.0
# ---------------------------------------------------------------------------
# Driver regen/rookie talent distribution
# ---------------------------------------------------------------------------
# Each entry is (weight, min_talent, max_talent). Weights are relative and do
# not need to sum to 1.0.
DRIVER_REGEN_TALENT_DISTRIBUTION = [
    (0.05, 90, 95),
    (0.15, 80, 90),
    (0.25, 70, 80),
    (0.25, 60, 70),
    (0.15, 50, 60),
    (0.15, 40, 50),
]

# ---------------------------------------------------------------------------
# Driver contract economics
# ---------------------------------------------------------------------------
# Salaries are expressed in $M per season.
# `DRIVER_SALARY_MAX_M` represents the expected salary for a 100-rated driver
# (before the per-driver expectation factor is applied).
DRIVER_SALARY_MIN_M = 1.0
DRIVER_SALARY_MAX_M = 60.0
DRIVER_SALARY_ELITE_THRESHOLD = 86.0
# Fraction of max salary reached at the elite threshold (steeper growth above).
DRIVER_SALARY_ELITE_SPLIT = 0.4
DRIVER_SALARY_GROWTH_BELOW_EXP = 3.0
DRIVER_SALARY_GROWTH_ABOVE_EXP = 1.8
# Maximum salary offer selectable in the driver negotiation UI slider ($M/season).
DRIVER_SALARY_OFFER_MAX_M = 80.0
DRIVER_BONUS_PER_POINT_MAX_M = 0.05
DRIVER_BONUS_PER_WIN_MAX_M = 1.0
DRIVER_BONUS_PER_PODIUM_MAX_M = 0.5
DRIVER_BONUS_PER_POINT_INTEREST_REFERENCE_M = 0.50
DRIVER_BONUS_PER_WIN_INTEREST_REFERENCE_M = 5.0
DRIVER_BONUS_PER_PODIUM_INTEREST_REFERENCE_M = 2.5
STAFF_BONUS_PER_POINT_MAX_M = 0.01
STAFF_BONUS_PER_WIN_MAX_M = 0.5
STAFF_BONUS_PER_PODIUM_MAX_M = 0.25
STAFF_BONUS_PER_POINT_INTEREST_REFERENCE_M = 0.50
STAFF_BONUS_PER_WIN_INTEREST_REFERENCE_M = 5.0
STAFF_BONUS_PER_PODIUM_INTEREST_REFERENCE_M = 2.5

# ---------------------------------------------------------------------------
# Staff contract economics
# ---------------------------------------------------------------------------
# Salaries are expressed in $M per season.
# Formula: expected_salary = STAFF_SALARY_PER_SKILL[role] * staff_skill
STAFF_SALARY_PER_SKILL = {
    "technical_director": 0.4,
    "chief_designer": 1.0,
    "head_of_aero": 0.5,
    "head_of_engine": 0.75,
    "head_of_dynamics": 0.25,
    "chief_mechanic": 0.5,
}

# Staff morale applies a flat skill modifier to every staff attribute.
# 50 morale = no modifier, 100 morale = +2, 0 morale = -2.
STAFF_MORALE_SKILL_DELTA_AT_EXTREME = 2.0

# ---------------------------------------------------------------------------
# Private testing (reserve driver development boost)
# ---------------------------------------------------------------------------
# Reserve drivers receive an end-of-season growth boost based on private test
# laps driven. The boost is applied as a multiplier to positive gains and
# inversely to age-related declines.
#
# Defaults preserve the current in-game behaviour:
# - First 100 laps: +0.002 per lap (1.20x at 100 laps)
# - Next 150 laps (to 250): +0.001 per lap (1.35x at 250 laps)
PRIVATE_TESTING_RESERVE_GROWTH_TIER1_LAPS = 100
PRIVATE_TESTING_RESERVE_GROWTH_TIER1_PER_LAP = 0.002
PRIVATE_TESTING_RESERVE_GROWTH_TIER2_LAPS = 250
PRIVATE_TESTING_RESERVE_GROWTH_TIER2_PER_LAP = 0.001

# Junior seat placement cost by tier (base + per junior-team quality step).
JUNIOR_SERIES_SEAT_COST_M = {
    4: {"base_m": 0.5, "quality_step_m": 0.05},
    3: {"base_m": 2.0, "quality_step_m": 0.10},
    2: {"base_m": 4.0, "quality_step_m": 0.25},
}

# Private testing lap costs in dollars.
PRIVATE_TESTING_COST_PER_LAP_TEST_TRACK = 2000
PRIVATE_TESTING_COST_PER_LAP_OTHER_TRACK = 5000

# Prestige tuning

# Race config
QUALI_GRID_LIMIT = 26  # Maximum starters; others are DNQ
QUALI_MIN_ENTRANTS = 20  # Minimum starters regardless of 107% rule
GRID_START_SPACING_KM = 0.016
RACE_START_LAUNCH_DURATION_S = 4.5

# Weekend cornering variability (applied as km/h bonus/penalty in corners only).
WEEKEND_CORNERING_VARIABILITY_LEVEL_MIN = 1
WEEKEND_CORNERING_VARIABILITY_LEVEL_MAX = 10
WEEKEND_CORNERING_VARIABILITY_KMH_PER_LEVEL = 0.25

# Speed model (sim-seconds per real-second)
SPEED_RATES = [2.0, 4.0, 8.0, 24.0, 48.0]
DEFAULT_SPEED_INDEX = 0  # 1x ≈ 4x real-time

# F1 points (top 10)
POINTS_TOP10 = [25,18,15,12,10,8,6,4,2,1]

# Added by patch
VERSION = '0.98.5'

# New chassis development structure
DEV_MAX_PROJECT_SPEND = 50.0  # Total chassis project investment cap (in millions)
DEV_PROTOTYPE_MIN_WEEKS = 2
DEV_PROTOTYPE_MAX_WEEKS = 40
DEV_DESIGN_MIN_WEEKS = 6
DEV_DESIGN_MAX_WEEKS = 80
DEV_HQ_LEVEL_FALLOFF = 0.95  # Post-level-two multiplier applied to additional HQ gains

DEV_CAR_CONCEPT_DEFAULT = "balanced"
DEV_CAR_CONCEPTS = {
    "cautious": {
        "label": "Cautious",
        "modifiers": {},
    },
    "balanced": {
        "label": "Balanced",
        "modifiers": {},
    },
    "aggressive": {
        "label": "Aggressive",
        "modifiers": {},
    },
    "experimental": {
        "label": "Experimental",
        "modifiers": {},
    },
}

# Chassis Development (rating-based potential model)
CHASSIS_DEV_RATING_MIN = 1.0
CHASSIS_DEV_RATING_MAX = 100.0
CHASSIS_DEV_INITIAL_POTENTIAL_MIN_BONUS = 5.0
CHASSIS_DEV_INITIAL_POTENTIAL_MAX_BONUS = 10.0
CHASSIS_DEV_CONCEPT_CARRYOVER = 0.75
CHASSIS_DEV_CONCEPT_BASE_STAFF_WEEKS = 100.0
CHASSIS_DEV_CONCEPT_TD_TIME_SKILL_MIN = 1
CHASSIS_DEV_CONCEPT_TD_TIME_SKILL_MAX = 20
CHASSIS_DEV_CONCEPT_TD_TIME_REDUCTION_PER_LEVEL = 0.025
CHASSIS_DEV_CONCEPT_RANDOM_MIN = -3.0
CHASSIS_DEV_CONCEPT_RANDOM_MAX = 3.0
CHASSIS_DEV_WIND_TUNNEL_MULT_PER_LEVEL = 0.015
CHASSIS_DEV_DESIGN_PHILOSOPHY_MULTIPLIERS = {
    "cautious": 0.975,
    "balanced": 1.0,
    "aggressive": 1.025,
    "experimental": 1.05,
}
CHASSIS_DEV_CATCHUP_THRESHOLD_PCT = 5.0
CHASSIS_DEV_CATCHUP_STEP_PCT = 2.0
CHASSIS_DEV_CATCHUP_STEP_VALUE = 0.0125
CHASSIS_DEV_CATCHUP_MULT_MIN = 0.50
CHASSIS_DEV_CATCHUP_MULT_MAX = 1.90
CHASSIS_DEV_CAR_CONCEPT_FILE = "car_concepts.json"
CHASSIS_DEV_DEFAULT_CAR_CONCEPT = "balanced"
CHASSIS_DEV_CAR_FOCUS_OPTIONS = {
    "slow": "Low Speed",
    "med": "Medium Speed",
    "high": "High Speed",
    "straight": "Straight-line",
    "tyre_management": "Tyre Wear",
    "chassis_reliability": "Chassis Reliability",
}
CHASSIS_DEV_DEFAULT_CAR_FOCUS = "slow"
CHASSIS_DEV_CAR_FOCUS_POTENTIAL_BONUS = 2.0

# Chassis Development (prototype baseline model)
CHASSIS_DEV_PROTOTYPE_BASE_STAFF_HOURS = 300.0
CHASSIS_DEV_PROTOTYPE_BASELINE_BASE_SHARE = 0.70
CHASSIS_DEV_PROTOTYPE_BASELINE_TD_PER_SKILL = 0.0075
CHASSIS_DEV_PROTOTYPE_BASELINE_CFD_PER_LEVEL = 0.01
CHASSIS_DEV_PROTOTYPE_BASELINE_SHARE_MIN = 0.05
CHASSIS_DEV_PROTOTYPE_BASELINE_SHARE_MAX = 1.00
CHASSIS_DEV_PROTOTYPE_BASELINE_PHILOSOPHY_OFFSETS = {
    "cautious": 0.05,
    "balanced": 0.0,
    "aggressive": -0.05,
    "experimental": -0.10,
}
CHASSIS_DEV_DESIGN_BASE_STAFF_HOURS = 1000.0
CHASSIS_DEV_DESIGN_BASELINE_START_SHARE = 0.50
CHASSIS_DEV_BUDGET_OPTIONS = {
    "shoestring": {
        "label": "Shoestring Budget",
        "amount_m": 15.0,
        "current_amount_m": 10.0,
        "design_progress_mult": 0.90,
        "baseline_mult": 1.00,
        "current_staff_hours_mult": 1.20,
        "current_stat_gain_mult": 0.90,
    },
    "small": {
        "label": "Small Budget",
        "amount_m": 25.0,
        "current_amount_m": 20.0,
        "design_progress_mult": 0.95,
        "baseline_mult": 1.00,
        "current_staff_hours_mult": 1.10,
        "current_stat_gain_mult": 0.95,
    },
    "moderate": {
        "label": "Moderate Budget",
        "amount_m": 35.0,
        "current_amount_m": 25.0,
        "design_progress_mult": 1.00,
        "baseline_mult": 1.00,
        "current_staff_hours_mult": 1.00,
        "current_stat_gain_mult": 1.00,
    },
    "large": {
        "label": "Large Budget",
        "amount_m": 45.0,
        "current_amount_m": 35.0,
        "design_progress_mult": 1.05,
        "baseline_mult": 1.00,
        "current_staff_hours_mult": 0.90,
        "current_stat_gain_mult": 1.05,
    },
    "factory": {
        "label": "Factory Budget",
        "amount_m": 60.0,
        "current_amount_m": 45.0,
        "design_progress_mult": 1.10,
        "baseline_mult": 1.02,
        "current_staff_hours_mult": 0.80,
        "current_stat_gain_mult": 1.10,
    },
}
CHASSIS_DEV_DEFAULT_BUDGET = "moderate"
CHASSIS_DEV_CURRENT_PACKAGE_DEFAULT = "mechanical_platform"
CHASSIS_DEV_SPEC_B_PACKAGE_KEY = "spec_b_chassis"
CHASSIS_DEV_SPEC_B_CARRYOVER = 0.8
CHASSIS_DEV_SPEC_B_BUDGET_MULTIPLIER = 2.0
CHASSIS_DEV_CURRENT_PACKAGE_CONCEPT_SHARE = 0.20
CHASSIS_DEV_CURRENT_PACKAGE_CATCHUP_THRESHOLD_PCT = 5.0
CHASSIS_DEV_CURRENT_PACKAGE_CATCHUP_AHEAD_BASE_MULT = 0.95
CHASSIS_DEV_CURRENT_PACKAGE_CATCHUP_AHEAD_STEP_PCT = 1.0
CHASSIS_DEV_CURRENT_PACKAGE_CATCHUP_AHEAD_STEP_VALUE = 0.025
CHASSIS_DEV_CURRENT_PACKAGE_CATCHUP_BEHIND_BASE_MULT = 1.05
CHASSIS_DEV_CURRENT_PACKAGE_CATCHUP_BEHIND_STEP_PCT = 1.0
CHASSIS_DEV_CURRENT_PACKAGE_CATCHUP_BEHIND_STEP_VALUE = 0.035
CHASSIS_DEV_CURRENT_PACKAGE_CATCHUP_MULT_MIN = 0.40
CHASSIS_DEV_CURRENT_PACKAGE_CATCHUP_MULT_MAX = 2.00
CHASSIS_DEV_CURRENT_PACKAGE_DEFINITIONS = {
    "mechanical_platform": {
        "label": "Mechanical Platform Development Package",
        "total_staff_hours": 300.0,
        "formula": {
            "slow_cd_mult": 0.25,
            "slow_wind_mult": 0.50,
            "slow_random_min": 0.0,
            "slow_random_max": 3.0,
            "tyre_hvd_tire_mgmt_mult": 0.25,
            "tyre_td_skill_mult": 0.10,
            "tyre_random_min": 0.0,
            "tyre_random_max": 2.0,
            "dirty_cd_skill_mult": 0.25,
            "dirty_td_skill_mult": 0.25,
            "dirty_random_min": 0.0,
            "dirty_random_max": 2.0,
        },
    },
    "weight_distribution": {
        "label": "Weight Distribution & Mass Reduction Package",
        "total_staff_hours": 500.0,
        "formula": {
            "weight_td_weight_mult": 0.15,
            "weight_factory_mult": 0.25,
            "weight_random_min": 0.0,
            "weight_random_max": 2.0,
            "base_pace_cd_skill_mult": 0.10,
            "base_pace_td_skill_mult": 0.10,
            "base_pace_wind_mult": 0.25,
            "base_pace_cfd_mult": 0.10,
        },
    },
    "chassis_rigidity": {
        "label": "Chassis Rigidity Development Package",
        "total_staff_hours": 200.0,
        "formula": {
            "reliability_td_efficiency_mult": 0.25,
            "reliability_cm_setup_mult": 0.25,
        },
    },
    "drag_optimization": {
        "label": "Drag Optimization Development Package",
        "total_staff_hours": 400.0,
        "formula": {
            "straight_cd_mult": 0.25,
            "straight_wind_mult": 0.50,
            "straight_random_min": 0.0,
            "straight_random_max": 2.0,
            "accel_td_skill_mult": 0.05,
            "accel_cfd_mult": 0.10,
            "high_cd_mult": 0.25,
            "high_wind_mult": 0.50,
            "high_random_min": 0.0,
            "high_random_max": 2.0,
        },
    },
    "mid_corner_balance": {
        "label": "Mid-Corner Balance Development Package",
        "total_staff_hours": 400.0,
        "formula": {
            "med_cd_mult": 0.25,
            "med_wind_mult": 0.50,
            "med_cfd_mult": 0.25,
            "med_random_min": 0.0,
            "med_random_max": 2.0,
        },
    },
}
CHASSIS_DEV_WEIGHT_TD_SKILL_MIN = 1
CHASSIS_DEV_WEIGHT_TD_SKILL_MID = 10
CHASSIS_DEV_WEIGHT_TD_SKILL_MAX = 20
CHASSIS_DEV_WEIGHT_TD_KG_AT_MIN = 1.5
CHASSIS_DEV_WEIGHT_TD_KG_AT_MID = -0.5
CHASSIS_DEV_WEIGHT_TD_KG_AT_MAX = -2.5
CHASSIS_DEV_WEIGHT_NOISE_BY_PHILOSOPHY = {
    "cautious": (-2.0, 2.0),
    "balanced": (-2.0, 2.0),
    "aggressive": (-3.0, 3.0),
    "experimental": (-4.0, 5.0),
}

DEV_CURRENT_WORK_SCALE = 0.5      # Current-season projects require half the base work

CHASSIS_RELIABILITY_MIN = 0.2  # Absolute floor for chassis reliability multipliers
CHASSIS_RELIABILITY_MAX = 3.0  # Absolute ceiling for chassis reliability multipliers
DIRTY_AIR_SENSITIVITY_MIN = 0.4  # Minimum effective dirty air sensitivity
DIRTY_AIR_SENSITIVITY_MAX = 1.6  # Maximum effective dirty air sensitivity

DEV_WIND_TUNNEL_EMPLOYEES_BASE = 20
DEV_WIND_TUNNEL_EMPLOYEES_STEP = 10
DEV_CFD_EMPLOYEES_BASE = 15
DEV_CFD_EMPLOYEES_STEP = 8
DEV_MIN_BUDGET_SHARE = 0.20  # Minimum effectiveness even with low budgets

# Reconnaissance tuning
RECON_STAFF_PER_LEVEL = 10  # Number of recon agents unlocked per building level
RECON_WEEKLY_HOURS_PER_STAFF = 1.0  # Staff-hours contributed per agent each week
RECON_REPORT_HOURS = 200.0  # Hours required against a rival before an insight email is triggered
# Espionage takes roughly the effort of generating five full intel reports
RECON_THEFT_REQUIRED_HOURS = RECON_REPORT_HOURS * 5  # Hours required to resolve an espionage operation
RECON_THEFT_BASE_FAIL_CHANCE = 0.12  # Baseline weekly failure chance for a theft attempt
RECON_THEFT_FAIL_PER_INSIGHT = 0.05  # Failure chance reduction per intel report spent
RECON_THEFT_FAIL_PER_LEVEL = 0.04  # Failure chance reduction per recon level advantage
RECON_THEFT_FAIL_MIN = 0.02  # Lower clamp for weekly failure chance
RECON_THEFT_FAIL_MAX = 0.85  # Upper clamp for weekly failure chance

# Driver systems development (driver aids)
DRIVER_SYSTEMS_STAFF_PER_LEVEL = 10  # Driver Systems Engineers unlocked per Driver Centre level
DRIVER_AID_MAX_LEVEL = 5
DRIVER_AID_PROGRESS_REQUIRED = 2000.0  # Staff-weeks needed per aid level (50 staff ~40 weeks)
DRIVER_AID_WEEKLY_PROGRESS_PER_STAFF = 1.0
DRIVER_AID_WETNESS_THRESHOLD = 1.0  # mm of water required before wet-weather aids activate
DRIVER_AID_BAN_DETECTION_CHANCE = 0.10  # Chance per race weekend that banned aids are discovered
DRIVER_AID_BUILD_COST_M = 0.5  # $500k
DRIVER_AID_BUILD_STAFF_HOURS = 100
DRIVER_AID_MAX_BUILDS_PER_LEVEL = 3  # 2 race cars + test car
OLD_CHASSIS_RATING_PENALTY = 5.0

# Aerodynamic development tuning
AERO_EFFICIENCY_MIN = 0.5
AERO_EFFICIENCY_MAX = 1.5
AERO_EFFICIENCY_BASE_MIN = 0.9
AERO_EFFICIENCY_BASE_MAX = 1.1
AERO_CONCEPT_WEEKS = 2
AERO_CONCEPT_FEE_M = 1.0  # One-time fee charged when an aero concept project begins
AERO_DEV_BUDGET_OPTIONS = {
    "shoestring": {
        "label": "Shoestring",
        "development_amount_m": 5.0,
        "spec_amount_m": 3.0,
        "gain_mult": 0.75,
    },
    "standard": {
        "label": "Standard",
        "development_amount_m": 7.5,
        "spec_amount_m": 5.0,
        "gain_mult": 1.0,
    },
    "factory": {
        "label": "Factory",
        "development_amount_m": 12.0,
        "spec_amount_m": 8.0,
        "gain_mult": 1.2,
    },
}
AERO_DEV_DEFAULT_BUDGET = "standard"
AERO_DESIGN_MIN_WEEKS = 4
AERO_DESIGN_MAX_WEEKS = 40
AERO_DESIGN_WORK_BASE = 400.0  # Work units required for a full aero design cycle at baseline staffing
AERO_SPEC_MIN_WEEKS = 2
AERO_SPEC_MAX_WEEKS = 12
AERO_SPEC_WORK_BASE = 100.0  # Work units required for an aero spec upgrade at baseline staffing
AERO_SPEC_MULTIPLIERS = {
    "B": 0.60,
    "C": 0.40,
    "D": 0.20,
    "E": 0.20,
}

# Tyre management limits used when translating development into race wear multipliers
TYRE_MANAGEMENT_MIN = 0.5
TYRE_MANAGEMENT_MAX = 1.5

# Car parts management
PART_INITIAL_STOCK = 2
# Additional spare parts provided per Factory level (beyond base stock)
FACTORY_PART_STOCK_BONUS = 2
PART_WEAR_PER_LAP = {
    "front_wing": 0.25,
    "rear_wing": 0.25,
    "underfloor": 0.15,
    "suspension": 0.15,
    "chassis": 0.10,
}
PART_CRASH_DAMAGE = 20.0

# External supplier pricing bands ($M).
# Managers linearly interpolate supplier rankings between these min/max values.
ENGINE_UNIT_COST_RANGE_M = (1.0, 3.0)
EXTERNAL_PARTS_COST_RANGES_M = {
    "fuel": (1.0, 5.0),
    "gearbox": (0.5, 1.0),
    "suspension": (0.5, 1.0),
    "brakes": (0.5, 1.0),
    "ecu": (0.5, 1.0),
}

# Engine system constants
ENGINE_CUSTOMER_PENALTY = 0.15  # s/lap slower for customer teams
ENGINE_POWER_TOKEN = -0.05      # lap-time delta per power upgrade level
ENGINE_RELIABILITY_TOKEN = 0.05  # reliability multiplier change per level
# Passive works engine development (ratings-based).
ENGINE_DEV_POWER_GAIN_PER_SKILL = 0.25
ENGINE_DEV_RELIABILITY_GAIN_PER_SKILL = 0.25
ENGINE_DEV_EFFICIENCY_GAIN_PER_SKILL = 0.25

# Applied after staff skill gains. Level 1 = 1.01, level 10 = 1.10.
ENGINE_DEV_PLANT_MULT_PER_LEVEL = 0.01

# Random end-of-cycle variation applied after all deterministic gain inputs.
ENGINE_DEV_RANDOM_MIN = -2.0
ENGINE_DEV_RANDOM_MAX = 2.0

# Power-only catch-up / diminishing return multiplier on seasonal gain.
ENGINE_DEV_POWER_BALANCE_THRESHOLD = 5.0
ENGINE_DEV_POWER_AHEAD_BASE_MULT = 0.85
ENGINE_DEV_POWER_BEHIND_BASE_MULT = 1.20
ENGINE_DEV_POWER_BALANCE_STEP = 0.05
ENGINE_DEV_POWER_GAIN_MULT_MIN = 0.25
ENGINE_DEV_POWER_GAIN_MULT_MAX = 2.0

# Passive project duration by Head of Engine "time" skill (linear interpolation).
ENGINE_DEV_WEEKS_AT_TIME_SKILL_1 = 50.0
ENGINE_DEV_WEEKS_AT_TIME_SKILL_20 = 40.0

# Passive engine weight development (kg-based).
ENGINE_DEV_WEIGHT_MIN_KG = 100.0
ENGINE_DEV_WEIGHT_MAX_KG = 200.0
ENGINE_DEV_WEIGHT_BRACKET_SIZE_KG = 10.0
ENGINE_DEV_WEIGHT_BRACKET_FACTOR_BASE = 1.0
ENGINE_DEV_WEIGHT_BRACKET_FACTOR_STEP = 0.01
ENGINE_DEV_WEIGHT_KG_PER_SKILL = 0.25
ENGINE_DEV_WEIGHT_PLANT_MULT_AT_LEVEL_1 = 0.99
ENGINE_DEV_WEIGHT_PLANT_MULT_AT_LEVEL_10 = 0.90
ENGINE_DEV_WEIGHT_RANDOM_MIN_KG = -5.0
ENGINE_DEV_WEIGHT_RANDOM_MAX_KG = 5.0
# External suppliers convert season budget into equivalent plant level:
# 20M => level 2, 40M => level 3, ... ; clamped in code to level 1..10.
ENGINE_DEV_SUPPLIER_BUDGET_PER_PLANT_LEVEL_M = 20.0

# Public-team share price drift (market pricing vs fair valuation).
# `market_multiplier` is clamped to [0.5, 1.5] of fair price and moves gradually.
SHARE_PRICE_MULTIPLIER_MIN = 0.5
SHARE_PRICE_MULTIPLIER_MAX = 1.5
SHARE_PRICE_MAX_WEEKLY_MOVE = 0.02   # max change in multiplier per week (≈2%)
SHARE_PRICE_WEEKLY_NOISE = 0.01      # random noise component (≈1%)
SHARE_PRICE_MEAN_REVERSION = 0.06    # pulls multiplier back toward 1.0 each week
SHARE_PRICE_HISTORY_MAX_POINTS = 4000
TEAM_MIN_VALUATION_M = 50.0

# Fuel system constants
FUEL_REFERENCE_EFFICIENCY = 50.0
FUEL_PER_LAP_CONSTANT = 100.0  # Reference kg-per-lap mass before efficiency/track modifiers
FUEL_LAPTIME_PENALTY_PER_KG = 0.05  # Seconds added to lap time per kilogram of fuel onboard
FUEL_TRACK_MIN_CONSUMPTION = 0.8
FUEL_TRACK_MAX_CONSUMPTION = 1.2

# Tyre development constants
TYRE_BASE_RATE = 0.05           # Progress per $1M weekly spend
TYRE_TRACK_MULT = 0.10          # Extra progress per test track level
TYRE_PACE_SCALE = -0.15         # Lap-time delta at 100% pace weighting
TYRE_DURABILITY_SCALE = 0.02    # Durability bonus at 100% durability weighting
TYRE_UPGRADE_PACE_RATING_POINTS = 2.0
TYRE_UPGRADE_DURABILITY_RATING_POINTS = 2.0

# Seasons between mandatory regulation resets that fully equalize performance
REG_RESET_MIN_SEASONS = 3
REG_RESET_MAX_SEASONS = 8

# Governmental-body next-season chassis reset tuning.
GOV_RESET_RETENTION = 0.25
GOV_RESET_STAFF_MULT = 2.0
GOV_RESET_FACILITY_MULT = 2.0
GOV_RESET_RANDOM_MULT = 2.0
GOV_RESET_PARTS_SUPPLIER_RETENTION = 0.55
GOV_RESET_PARTS_SUPPLIER_BUDGET_PER_M = 0.1
GOV_RESET_PARTS_SUPPLIER_SWING = 10.0

# Minimum fraction of team balance to hold as reserve when AI plans spending
CONTRACT_RESERVE_PCT = 0.05

# Portion of the next HQ upgrade cost AI teams will keep in reserve
AI_HQ_RESERVE_PCT = 0.1

# ---------------------------------------------------------------------------
# Race operations costs ($M per event)
# ---------------------------------------------------------------------------
# Baseline operational cost per race weekend and an additional cost per DNF.
RACE_OPERATION_COST_PER_EVENT_M = 1.0
RACE_DNF_COST_M = 1.0

# ---------------------------------------------------------------------------
# Equity taxes
# ---------------------------------------------------------------------------
# Applied as a one-time outflow on cash proceeds from equity sales (IPO / sell stake / buyouts).
CAPITAL_GAINS_TAX_RATE = 0.25

# Share of discretionary funds AI teams keep as a rainy-day reserve
AI_DEV_RESERVE_RATIO = 0.1

# Additional cushion AI teams require in their HQ pool before purchasing upgrades
AI_DEV_HQ_BUFFER_M = 5.0

# Maximum fraction of the next HQ upgrade cost earmarked as a seasonal target
AI_DEV_HQ_SEASON_CAP_RATIO = 0.6

# Balance threshold (in millions) where AI teams stop hoarding cash and immediately
# buy their next HQ upgrade if possible.
AI_HQ_FORCE_SPEND_BALANCE_M = 250.0

# Development budget pool keys used across AI budgeting logic
AI_DEV_POOL_KEYS = ("current", "future", "aero", "hq")

# Weighted budget variants sampled per competitiveness bracket each season
AI_DEV_POOL_VARIANTS = {
    "backmarker": [
        ("catchup", {"current": 0.24, "future": 0.54, "aero": 0.11, "hq": 0.11}),
        ("future_push", {"current": 0.18, "future": 0.59, "aero": 0.11, "hq": 0.12}),
        ("recovery", {"current": 0.20, "future": 0.49, "aero": 0.12, "hq": 0.19}),
    ],
    "midfield": [
        ("balanced", {"current": 0.28, "future": 0.37, "aero": 0.13, "hq": 0.22}),
        ("future_bias", {"current": 0.26, "future": 0.41, "aero": 0.13, "hq": 0.20}),
        ("pace_chaser", {"current": 0.32, "future": 0.33, "aero": 0.14, "hq": 0.21}),
    ],
    "contender": [
        ("maintain", {"current": 0.36, "future": 0.30, "aero": 0.14, "hq": 0.20}),
        ("aggressive", {"current": 0.33, "future": 0.30, "aero": 0.16, "hq": 0.21}),
        ("infrastructure", {"current": 0.30, "future": 0.28, "aero": 0.14, "hq": 0.28}),
    ],
}

# Fraction of wind-tunnel staffing AI allocates per project type by competitiveness tier
AI_DEV_STAFF_FRACTIONS = {
    "future": {"backmarker": 0.7, "midfield": 0.8, "contender": 0.9},
    "current": {"backmarker": 0.45, "midfield": 0.55, "contender": 0.65},
    "aero": {"backmarker": 0.35, "midfield": 0.45, "contender": 0.55},
    "spec": {"backmarker": 0.25, "midfield": 0.35, "contender": 0.45},
}

# Weekly spend targets (in millions) the AI aims for when budgeting projects
AI_DEV_WEEKLY_BUDGETS = {
    "future": {"backmarker": 4.5, "midfield": 5.0, "contender": 5.0},
    "current": {"backmarker": 3.0, "midfield": 3.5, "contender": 4.0},
    "aero": {"backmarker": 0.45, "midfield": 0.65, "contender": 0.85},
    "spec": {"backmarker": 0.3, "midfield": 0.4, "contender": 0.5},
}

# Minimum weekly investment (in millions) the AI will consider when launching a project
AI_DEV_MIN_WEEKLY_SPEND = 0.5

# Latest week (1-indexed) AI will start new current-season chassis projects
AI_DEV_CURRENT_LAUNCH_CUTOFF_WEEK = 34

# Week window (1-indexed) when AI begins winding down current-season chassis work
AI_DEV_CURRENT_WRAP_TARGET_WEEK = 36

# Hard cutoff week (1-indexed) for forcing delivery of current-season chassis projects
AI_DEV_CURRENT_WRAP_FORCE_WEEK = 38

# Minimum design completion ratio before AI voluntarily delivers current projects
AI_DEV_CURRENT_WRAP_PROGRESS_THRESHOLD = 0.65

# Week (1-indexed) by which AI future-season chassis projects should be wrapped up
AI_DEV_FUTURE_FINALIZE_WEEK = 51

# Multiplier applied to work targets when AI develops future-season chassis
# projects, letting them complete offseason builds roughly 50% faster without
# affecting the delivered quality.
AI_FUTURE_CHASSIS_TIME_SCALE = 0.5

# Probability weight the AI gives to retaining its current car concept when
# beginning a new future-season chassis project. The remaining weight is split
# evenly across the other available concepts to keep variety on the grid.
AI_FUTURE_CONCEPT_CURRENT_WEIGHT = 0.5

# Maximum number of simultaneous aero projects (development + spec) the AI will run
AI_DEV_AERO_MAX_ACTIVE = 2

# Minimum projected lap-time gain (in seconds) the AI expects from aero work
# before committing funds to a project. Spec upgrades can be lighter, but still
# need to clear a small benefit to justify the spend, while full redesigns
# demand a larger improvement to balance their longer timelines.
AI_DEV_AERO_SPEC_MIN_GAIN = 0.018
AI_DEV_AERO_DEV_MIN_GAIN = 0.03

# Spec B is an exceptional current-season overhaul. AI teams only consider it
# when its deterministic expected gain is large enough to justify its cost and
# is meaningfully better than a conventional chassis package.
AI_DEV_SPEC_B_MIN_GAIN_SECONDS = 0.25
AI_DEV_SPEC_B_MIN_NORMAL_GAIN_MULTIPLIER = 2.0
AI_DEV_SPEC_B_MANUFACTURE_BUFFER_WEEKS = 2
# AI-only progress speed for Spec B chassis projects. Does not affect players
# or any conventional current/future chassis project.
AI_DEV_SPEC_B_PROGRESS_MULTIPLIER = 1.5

# Starting cash balance for teams in the inaugural season
INITIAL_TEAM_BALANCE_M = 65.0

# Constructors' championship prize payouts in millions, ordered by final position
PRIZE_MONEY_PAYOUTS_M = [225, 200, 180, 160, 140, 120, 100, 80, 60, 50]

# AI development strategy budget weights
# Fractions of available funds allocated to immediate car upgrades vs headquarters
# improvements once long-term projects are funded
DEV_STRATEGY_WEIGHTS = {
    "current": {"upgrades": 0.7, "hq": 0.3},
    "balanced": {"upgrades": 0.5, "hq": 0.5},
    "future": {"upgrades": 0.3, "hq": 0.7},
    "future_only": {"upgrades": 0.0, "hq": 1.0},
}

# AI sponsor signing behaviour
# If more than AI_SPONSOR_SIGN_DEADLINE_WEEKS remain in the season, AI teams may
# defer signing to preserve negotiation points for a better deal.
AI_SPONSOR_SIGN_DEADLINE_WEEKS = 4

# Multiplier applied only to AI sponsor negotiations so their estimated progress
# and weekly work ramp up faster than the human-controlled team.
AI_SPONSOR_PROGRESS_MULTIPLIER = 1.5
