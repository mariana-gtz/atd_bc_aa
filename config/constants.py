ENCODING = 'utf-8'
SEP_ISOFORMAT = " "
TIMESPEC_ISOFORMAT = "minutes"
UTC_TIME_ZONE = "UTC"

""" Date related constants. """
INTERVAL = "interval"
DAY = "day"
WEEK = "week"
MONTH = "month"
QUARTER = "quarter"
YEAR = "year"
DATE_INTERVAL_DAILY = "Daily"
DATE_INTERVAL_WEEKLY = "Weekly"
DATE_INTERVAL_MONTHLY = "Monthly"
DAY_PATTERN = "%a %b %d %y"
WEEK_PATTERN = "%b %d %y"
MONTH_PATTERN = "%b %y"
DAY_DELTA = "DoD"
WEEK_DELTA = "WoW"
MONTH_DELTA = "MoM"
QUARTER_PREFIX = "Q"

DATE_INTERVALS = [DATE_INTERVAL_DAILY, DATE_INTERVAL_WEEKLY, DATE_INTERVAL_MONTHLY]
DEFAULT_PERIODS_TO_DISPLAY = 10


""" Filter related constants. """
MAX_FILTERS_PER_ROW = 4
TOGGLES_COL_MULTIPLIER = 3
KEY_FILTER_TYPE = "filter_type"
FILTER_TYPE_SELECTBOX = "selectbox"
FILTER_TYPE_MULTISELECT = "multiselect"
KEY_LABEL = "label"
KEY_OPTIONS = "options"
KEY_KEY = "key"
KEY_VALUE = "value"
KEY_DEFAULT = "default"
KEY_HELP = "help"
KEY_SUFFIX = "suffix"
KEY_PATTERN = "pattern"
KEY_DELTA = "delta"
KEY_DELTA_TYPE = "delta_type"
KEY_AGG = "agg"
KEY_FORMAT = "format"
KEY_TITLE = "title"
KEY_DATA_TYPE = "data_type"
KEY_SHIFT_PERIOD = "shift_period"
KEY_SHOW_DELTA_TOGGLE = "show_delta_toggle"
KEY_SHOW_RAW_TOGGLE = "show_raw_toggle"
KEY_DIVIDE_BY = "divide_by"
KEY_ADD_SPACES = "add_spaces"
KEY_POSITION = "position"
KEY_GROWTH_GOOD = "growth_good"
KEY_IS_CALCULATED = "is_calculated"
KEY_FORMULA = "formula"

DEFAULT_MX = "Mexico"
DELTA_UP = "▲"
DELTA_DOWN = "▼"

SUM = "sum"
AVG = "mean"
MEDIAN = "median"
UNIQUE = "nunique"

NUMBER = "number"
PERCENTAGE = "percentage"
KM = "km"
PP = "pp"
MINUTES = "min"
CURRENCY = "currency"
DATE_FORMATTED_SUFFIX = "_formatted"


""" Constants for file paths and names."""
DATA_PATH = "data/"
ASSETS_PATH = "assets/"
DATA_DEFAULT_FILE_NAME = "BC_A&A_with_ATD"
LAST_UPDATE_FILE_NAME = "last_time_updated.json"
LARGE_IMAGE_NAME = "UE_Horizontal_White_Large.png"
SMALL_IMAGE_NAME = "UE_Horizontal_Black_Small.png"

""" Constants for Dataspitter."""
"""Constants from original CSV file."""
COL_REGION = ["region", "string", "Region"]
COL_TERRITORY = ["territory", "string", "Territory"]
COL_COUNTRY = ["country_name", "string", "Country"]
COL_WORKFLOW = ["workflow_uuid", "string", "Completed Trips"]
COL_DRIVER = ["driver_uuid", "string", "Active Drivers"]
COL_DELIVERY_TRIP = ["delivery_trip_uuid", "string", "Delivery Trip"]
COL_COURIER_FLOW = ["courier_flow", "string", "Courier Flow"]
COL_GEO_STRATEGY = ["geo_archetype", "string", "Geo Strategy"]
COL_MERCHANT_SURFACE = ["merchant_surface", "string", "Merchant Surface"]

COL_RESTO_OFFERED_UTC = ["restaurant_offered_timestamp_utc", "datetime64[ns]", "Restaurant Offered UTC"]
COL_ORDER_FINAL_STATE_LOCAL = ["order_final_state_timestamp_local", "datetime64[ns]", "Order Final State Local"]
COL_EATER_REQUEST_LOCAL = ["eater_request_timestamp_local", "datetime64[ns]", "Eater Request Local"]

COL_PICKUP_DISTANCE = ["pickup_distance", "float32", "Avg. Pickup Distance (Km)"]
COL_DROPOFF_DISTANCE = ["dropoff_distance", "float32", "Avg. Dropoff Distance (Km)"]
COL_ATD = ["ATD", "float32", "Actual Time of Delivery (min)"]
COL_TOTAL_DISTANCE = ["total_distance", "float32", "Avg. Total Trip Distance (Km)"]


"""Constants CALCULATED from original CSV file."""
COL_HOUR = ["hour", "int64", "Hour"]
COL_WEEKDAY = ["weekday", "string", "Weekday"]
COL_DAY = ["day", "datetime64[ns]", "Day"]
COL_WEEK = ["week", "datetime64[ns]", "Week"]
COL_MONTH = ["month", "datetime64[ns]", "Month"]

COL_TIME_OF_DAY = ["time_of_day", "string", "Time of Day"]
DAY_PART_RANGES = [
    ("Breakfast", 5, 11),
    ("Lunch", 12, 16),
    ("Dinner", 17, 23),
    ("Late Night", 0, 4),
]
COL_IS_WEEKEND = ["is_weekend", "boolean", "Is Weekend?"]
COL_IS_SEASONALITY = ["is_seasonality", "boolean", "Is Seasonality?"]
MMDD = "%m-%d"
FIXED_SEASONALITIES_MMDD = {
    "01-01": "New Year's Day",
    "02-05": "Feb 5th",
    "02-14": "Valentine's Day",
    "04-30": "Children's Day",
    "05-05": "May 5th",
    "05-10": "Mother's Day",
    "09-15": "Sep 15th",
    "09-16": "Sep 16th",
    "11-02": "Day of the Dead",
    "11-20": "Revolution Day",
    "12-12": "Day of the Virgin",
    "12-24": "Christmas Eve",
    "12-25": "Christmas Day",
    "12-31": "New Year's Eve"
}
VARIABLE_SEASONALITIES_DATES = {
    "2025-02-09": "Super Bowl",
    # Add more as needed
}

""" Constants for the ATD Controller."""
ATD_TITLE = "ATD Overview"
ATD_SUBHEADER = "Choose your table display options"
ATD_OPTION_MENU_TITLE = None
ATD_OPTION_MENU_OPTIONS = ["ATD Overview", "Good to know"]
ATD_OPTION_MENU_ICONS = ["bar-chart-fill", "info-circle-fill"]
ATD_OPTION_MENU_ICON = "cast"
ATD_OPTION_DEFAULT_OPTION = 0
ATD_OPTION_ORIENTATION = "horizontal"

ATD_GROUP_BY_COLUMNS = [COL_REGION, 
                        COL_TERRITORY, 
                        COL_COUNTRY, 
                        COL_GEO_STRATEGY, 
                        COL_COURIER_FLOW, 
                        COL_MERCHANT_SURFACE]

ATD_TRANSPOSED_INDEX = "Metric"
ATD_TRANSPOSED_SPARKLINE_COLUMN = "Sparkline"
