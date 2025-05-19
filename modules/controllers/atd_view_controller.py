import sys
import os
cwd = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(cwd)
from config.constants import *

import streamlit as st
import pandas as pd

import numpy as np
import glob
import math
from datetime import datetime, timedelta
import json
import hashlib
import altair as alt


class ATDController:
    def __init__(self):
        
        
        self.data_path = os.path.join(cwd, DATA_PATH)
        self.last_time_updated_file_path = os.path.join(self.data_path, LAST_UPDATE_FILE_NAME)
        self.data_file_path = os.path.join(self.data_path, DATA_DEFAULT_FILE_NAME + ".parquet")
        
        self.page_title = ATD_TITLE
        self.page_subheader = ATD_SUBHEADER
        self.menu_title = ATD_OPTION_MENU_TITLE
        self.options = ATD_OPTION_MENU_OPTIONS
        self.icons = ATD_OPTION_MENU_ICONS
        self.menu_icon = ATD_OPTION_MENU_ICON
        self.default_index = ATD_OPTION_DEFAULT_OPTION
        self.orientation = ATD_OPTION_ORIENTATION

        self.INTERVALS = {
            DAY: {
                KEY_SUFFIX: DATE_INTERVAL_DAILY,
                KEY_PATTERN: DAY_PATTERN,
                KEY_DELTA: DAY_DELTA,
                KEY_SHOW_DELTA_TOGGLE: True,
                KEY_SHOW_RAW_TOGGLE: True,
                KEY_SHIFT_PERIOD: 7,
            },
            WEEK: {
                KEY_SUFFIX: DATE_INTERVAL_WEEKLY,
                KEY_PATTERN: WEEK_PATTERN,
                KEY_DELTA: WEEK_DELTA,
                KEY_SHOW_DELTA_TOGGLE: True,
                KEY_SHOW_RAW_TOGGLE: True,
                KEY_SHIFT_PERIOD: 1,
            },
            MONTH: {
                KEY_SUFFIX: DATE_INTERVAL_MONTHLY,
                KEY_PATTERN: MONTH_PATTERN,
                KEY_DELTA: MONTH_DELTA,
                KEY_SHOW_DELTA_TOGGLE: True,
                KEY_SHOW_RAW_TOGGLE: True,
                KEY_SHIFT_PERIOD: 1,
            },
        }
        
        self.FILTER_COLUMNS = ATD_GROUP_BY_COLUMNS
        self.FILTERS = {
            INTERVAL: {
                KEY_FILTER_TYPE: FILTER_TYPE_SELECTBOX,
                KEY_LABEL: "Select interval",
                KEY_KEY: "interval_filter",
                KEY_OPTIONS: DATE_INTERVALS,
                KEY_DEFAULT: DATE_INTERVAL_WEEKLY,
                KEY_HELP: "Select the interval to filter the data.",
            },
            COL_REGION[0]: {
                KEY_FILTER_TYPE: FILTER_TYPE_MULTISELECT,
                KEY_LABEL: "Select a region",
                KEY_KEY: "region_filter",
                KEY_OPTIONS: [],
                KEY_DEFAULT: [DEFAULT_MX],
                KEY_HELP: "Choose a region to filter the data.",
            },
            COL_COUNTRY[0]: {
                KEY_FILTER_TYPE: FILTER_TYPE_MULTISELECT,
                KEY_LABEL: "Select a country",
                KEY_KEY: "country_filter",
                KEY_OPTIONS: [],
                KEY_DEFAULT: [DEFAULT_MX],
                KEY_HELP: "Choose a country to filter the data.",
            },
            COL_TERRITORY[0]: {
                KEY_FILTER_TYPE: FILTER_TYPE_MULTISELECT,
                KEY_LABEL: "Select a territory",
                KEY_KEY: "territory_filter",
                KEY_OPTIONS: [],
                KEY_DEFAULT: [],
                KEY_HELP: "Choose a territory to filter the data.",
            },
            COL_GEO_STRATEGY[0]: {
                KEY_FILTER_TYPE: FILTER_TYPE_MULTISELECT,
                KEY_LABEL: "Select a geo strategy",
                KEY_KEY: "geo_strategy_filter",
                KEY_OPTIONS: [],
                KEY_DEFAULT: [],
                KEY_HELP: "Based on Apollo classification.",
            },
            COL_COURIER_FLOW[0]: {
                KEY_FILTER_TYPE: FILTER_TYPE_MULTISELECT,
                KEY_LABEL: "Select a courier flow",
                KEY_KEY: "courier_flow_filter",
                KEY_OPTIONS: [],
                KEY_DEFAULT: [],
                KEY_HELP: "Choose a courier flow to filter the data.",
            },
            COL_MERCHANT_SURFACE[0]: {
                KEY_FILTER_TYPE: FILTER_TYPE_MULTISELECT,
                KEY_LABEL: "Select a merchant surface",
                KEY_KEY: "merchant_surface_filter",
                KEY_OPTIONS: [],
                KEY_DEFAULT: [],
                KEY_HELP: "Choose a merchant surface to filter the data.",
            },
        }

        self.METRICS_CONFIG = {
            COL_WORKFLOW[0]: {
                KEY_AGG: UNIQUE, # Aggregation method
                KEY_FORMAT: NUMBER, # Formatting type
                KEY_TITLE: COL_WORKFLOW[2], # Alternate title
                KEY_DIVIDE_BY: None, # Unit conversion (if applicable)
                KEY_DELTA_TYPE: PERCENTAGE, # Delta type (percentage or pp)
                KEY_DATA_TYPE: COL_WORKFLOW[1], # Data type (int or string)
                KEY_ADD_SPACES: 0, # Number of spaces to add to the delta title
                KEY_POSITION: 5, # Position for column ordering inside pillar
                KEY_GROWTH_GOOD: True, # Growth good flag
            },
            COL_DRIVER[0]: {
                KEY_AGG: UNIQUE, 
                KEY_FORMAT: NUMBER, 
                KEY_TITLE: COL_DRIVER[2], 
                KEY_DIVIDE_BY: None, 
                KEY_DELTA_TYPE: PERCENTAGE, 
                KEY_DATA_TYPE: COL_DRIVER[1],
                KEY_ADD_SPACES: 1, 
                KEY_POSITION: 4, 
                KEY_GROWTH_GOOD: True, 
            },
            COL_PICKUP_DISTANCE[0]: {
                KEY_AGG: AVG, 
                KEY_FORMAT: KM, 
                KEY_TITLE: COL_PICKUP_DISTANCE[2], 
                KEY_DIVIDE_BY: None, 
                KEY_DATA_TYPE: COL_PICKUP_DISTANCE[1],
                KEY_DELTA_TYPE: PERCENTAGE, 
                KEY_ADD_SPACES: 2, 
                KEY_POSITION: 2, 
                KEY_GROWTH_GOOD: False, 
            },
            COL_DROPOFF_DISTANCE[0]: {
                KEY_AGG: AVG, 
                KEY_FORMAT: KM, 
                KEY_TITLE: COL_DROPOFF_DISTANCE[2], 
                KEY_DIVIDE_BY: None, 
                KEY_DATA_TYPE: COL_DROPOFF_DISTANCE[1],
                KEY_DELTA_TYPE: PERCENTAGE, 
                KEY_ADD_SPACES: 3, 
                KEY_POSITION: 3, 
                KEY_GROWTH_GOOD: False, 
            },
            COL_ATD[0]: {
                KEY_AGG: AVG, 
                KEY_FORMAT: MINUTES, 
                KEY_TITLE: COL_ATD[2], 
                KEY_DIVIDE_BY: None, 
                KEY_DATA_TYPE: COL_ATD[1],
                KEY_DELTA_TYPE: PERCENTAGE, 
                KEY_ADD_SPACES: 6, 
                KEY_POSITION: 0, 
                KEY_GROWTH_GOOD: False, 
            },
            COL_TOTAL_DISTANCE[0]: {
                KEY_AGG: AVG, 
                KEY_FORMAT: KM, 
                KEY_TITLE: COL_TOTAL_DISTANCE[2], 
                KEY_DIVIDE_BY: None,
                KEY_DATA_TYPE: COL_TOTAL_DISTANCE[1], 
                KEY_DELTA_TYPE: PERCENTAGE, 
                KEY_ADD_SPACES: 5, 
                KEY_POSITION: 1, 
                KEY_GROWTH_GOOD: True, 
            },
        }


        
    @st.cache_data(show_spinner="Loading data...", ttl=3600, max_entries=10)
    def load_data(_self):
        """Load data from a PARQUET file."""
        
        try:
            file_path = os.path.join(_self.data_file_path)
            df = pd.read_parquet(file_path)
            df.replace('\\N', pd.NA, inplace=True)
        except FileNotFoundError:
            st.toast(f"No data file found!", icon="⚠️")
            st.stop()
        except Exception as e:
            st.toast(f"Error loading data: {e}", icon="🚨")
            st.stop()
        
        # === Gather all expected metric columns from METRICS_CONFIG ===
        expected_metrics = {}
        for metric_key, metric_config in _self.METRICS_CONFIG.items():
            expected_metrics[metric_key] = metric_config.get(KEY_DATA_TYPE, "float32")
        
        # === Ensure all metric columns exist and cast their data types ===
        for column, dtype in expected_metrics.items():
            if column not in df.columns:
                df[column] = np.nan  # or 0 if you prefer default zero
            try:
                df[column] = df[column].astype(dtype)
            except Exception:
                # fallback to numeric with coercion if type conversion fails
                df[column] = pd.to_numeric(df[column], errors='coerce')

        return df


    @st.cache_data(show_spinner=False)
    def get_unique_options(_self, df_hash: str, col: str, df: pd.DataFrame):
        """Return unique options for one column, cached by df-hash so it reruns only on new data."""
        return sorted(df[col].dropna().unique().tolist())


    def get_selectbox_with_memory(self, label, options, key, default=None, help=None):
        
        if default in options:
            default_index = options.index(default)
        else:
            default_index = 0

        return st.selectbox(label, options, index=default_index, key=key, help=help)


    def get_multiselect_with_memory(self, label, options, key, default=None, help=None):
        """
        Safe multiselect with a default. Avoids session state conflicts by
        only passing default when session state key is not yet initialized.
        """
        cleaned_default = [val for val in (default or []) if val in options]

        if key in st.session_state:
            # Streamlit already tracks the value — don't pass default again
            return st.multiselect(label=label, options=options, key=key, help=help)
        else:
            # First render — pass default
            return st.multiselect(label=label, options=options, default=cleaned_default, key=key, help=help)
    

    def render_single_filter(self, col_name, cfg, df_hash, working_df):
        """
        Helper to render a single filter widget and return its selected value.
        """
        label       = cfg[KEY_LABEL]
        key         = cfg[KEY_KEY]
        default     = cfg.get(KEY_DEFAULT, [])
        help_text   = cfg.get(KEY_HELP)
        filter_type = cfg.get(KEY_FILTER_TYPE, FILTER_TYPE_MULTISELECT)

        options = self.get_unique_options(df_hash, col_name, working_df)
        self.FILTERS[col_name][KEY_OPTIONS] = options

        if filter_type == FILTER_TYPE_SELECTBOX:
            default_val = default if default in options else (options[0] if options else None)
            return self.get_selectbox_with_memory(label, options, key, default_val, help_text)
        else:
            return self.get_multiselect_with_memory(label, options, key, default, help_text)
    

    def apply_selection(self, mask, df, col_name, cfg, selected):
        """
        Applies a filter selection to both the mask and the working DataFrame (cascading logic).
        """
        if selected:
            if isinstance(selected, list):
                mask &= df[col_name].isin(selected)
                df = df[df[col_name].isin(selected)]
            else:
                mask &= df[col_name] == selected
                df = df[df[col_name] == selected]

        return mask, df
    

    def get_interval_column(self, selected_interval: str) -> str:
        """
        Returns the interval column name based on the selected interval.
        """
        for key, props in self.INTERVALS.items():
            if props.get(KEY_SUFFIX) == selected_interval:
                return key
        return None


    def get_filtered_data(self) -> tuple[pd.DataFrame, dict]:
        """Render multiselects in a grid; preserve selections; return filtered df."""
        selections = {}

        # STEP 1: Interval filter first
        interval_config = self.FILTERS[INTERVAL]
        first_row = st.columns(MAX_FILTERS_PER_ROW)

        with first_row[0]:
            selected_interval = self.get_selectbox_with_memory(
                label   = interval_config.get(KEY_LABEL),
                options = interval_config.get(KEY_OPTIONS),
                key     = interval_config.get(KEY_KEY),
                default = interval_config.get(KEY_DEFAULT),
                help    = interval_config.get(KEY_HELP)
            )

        selections[INTERVAL] = selected_interval

        df = self.load_data()
        df_hash = hashlib.md5(pd.util.hash_pandas_object(df, index=False).values).hexdigest()

        mask = np.ones(len(df), dtype=bool)
        working_df = df.copy()  # used to limit filter options based on prior filters

        other_filters = {k: v for k, v in self.FILTERS.items() if k != INTERVAL}
        filter_names  = list(other_filters.keys())

        visible_filters = []
        for filter_name in filter_names:
            config = other_filters[filter_name]
            if config:
                visible_filters.append(filter_name)
        
        first_row_filters = visible_filters[:MAX_FILTERS_PER_ROW - 1] # -1 for interval filter
        remaining_filters = visible_filters[MAX_FILTERS_PER_ROW - 1:]

        for i, filter_name in enumerate(first_row_filters):
            cfg = other_filters[filter_name]
            with first_row[i + 1]:  # interval is at index 0
                selected = self.render_single_filter(filter_name, cfg, df_hash, working_df)
                selections[filter_name] = selected
                mask, working_df = self.apply_selection(mask, working_df, filter_name, cfg, selected)
        
        for row_start in range(0, len(remaining_filters), MAX_FILTERS_PER_ROW):
            row_filter_names = remaining_filters[row_start:row_start + MAX_FILTERS_PER_ROW]
            cols = st.columns(len(row_filter_names))

            for i, filter_name in enumerate(row_filter_names):
                cfg = other_filters[filter_name]
                with cols[i]:
                    selected = self.render_single_filter(filter_name, cfg, df_hash, working_df)
                    selections[filter_name] = selected
                    mask, working_df = self.apply_selection(mask, working_df, filter_name, cfg, selected)

        return df[mask], selections
    

    def get_toggles_to_show(self, interval_column: str) -> dict:
        """
        Dynamically returns a dictionary of toggles to render based on INTERVALS config.
        Only includes toggles where the config value is True.

        Returns:
            dict of {
                "toggle_id": {
                    "label": str,
                    "value": bool,
                    "key": str
                }
            }
        """
        toggles = {}

        # Toggle config: maps internal key -> display label
        toggle_definitions = {
            KEY_SHOW_DELTA_TOGGLE: {
                KEY_KEY: KEY_SHOW_DELTA_TOGGLE,
                KEY_LABEL: "Show deltas",
            },
            KEY_SHOW_RAW_TOGGLE: {
                KEY_KEY: KEY_SHOW_RAW_TOGGLE,
                KEY_LABEL: "Show actuals",
            },
        }

        interval_config = self.INTERVALS.get(interval_column, {})

        for toggle_id, config in toggle_definitions.items():
            flag = interval_config.get(config[KEY_KEY], False)
            if flag:
                toggles[toggle_id] = {
                    KEY_LABEL: config[KEY_LABEL],
                    KEY_VALUE: False,  # default unchecked
                    KEY_KEY: f"{toggle_id}_{interval_column}"
                }

        return toggles


    def get_aggregated_data(self, filtered_df: pd.DataFrame, interval_column: str) -> pd.DataFrame:
        """
        Groups and aggregates the filtered data based on METRICS_CONFIG.
        Returns a DataFrame grouped by interval + breakdown.
        """

        # === Step 1: Build aggregation dictionary ===
        agg_dict = {}

        for metric_key, metric_config in self.METRICS_CONFIG.items():
            agg_func = metric_config.get(KEY_AGG, SUM)
            agg_dict[metric_key] = agg_func

        # === Step 2: Determine grouping columns ===
        group_columns = [interval_column]

        # === Step 3: Perform aggregation ===
        aggregated_df = filtered_df.groupby(group_columns).agg(agg_dict).reset_index()

        return aggregated_df
    

    def apply_metric_calculations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        1. First computes all calculated metrics (formulas)
        2. Then applies scalar divisions (like FX)
        """

        df = df.copy()

        # === Step 1: Evaluate all calculated metrics first
        for metric_key, metric_config in self.METRICS_CONFIG.items():
            if metric_config.get(KEY_IS_CALCULATED, False):
                formula = metric_config.get(KEY_FORMULA)
                if not formula:
                    continue

                try:
                    df[metric_key] = df.eval(formula)
                except Exception as e:
                    st.warning(f"⚠️ Failed to compute '{metric_key}' with formula '{formula}': {e}")
                    df[metric_key] = np.nan

        # === Step 2: Apply scalar division (e.g., FX) AFTER formulas
        for metric_key, metric_config in self.METRICS_CONFIG.items():
            divide_by = metric_config.get(KEY_DIVIDE_BY)

            if divide_by and isinstance(divide_by, (int, float)) and divide_by != 0:
                if metric_key in df.columns:
                    try:
                        df[metric_key] = df[metric_key] / divide_by
                    except Exception as e:
                        st.warning(f"⚠️ Scalar division failed for '{metric_key}': {e}")
                        df[metric_key] = np.nan

        return df
    

    def filter_positioned_metrics(self, df: pd.DataFrame, interval_column: str) -> pd.DataFrame:
        """
        Returns a DataFrame containing only metrics that have a KEY_POSITION defined.
        """
        df, formatted_date_col = self.format_interval_dates(df, interval_column)
        metric_columns = [interval_column, formatted_date_col]

        for metric_key, config in self.METRICS_CONFIG.items():
            if KEY_POSITION in config:
                if metric_key in df.columns:
                    metric_columns.append(metric_key)

        return df[metric_columns]

    
    def format_interval_dates(self, df: pd.DataFrame, interval_column: str) -> tuple[pd.DataFrame, str]:
        """
        Formats the dates for display.
        """
        new_col_name = f"{interval_column}{DATE_FORMATTED_SUFFIX}"
        if interval_column == QUARTER:
            df[new_col_name] = QUARTER_PREFIX + df[interval_column].dt.quarter.astype(str) + " " + df[interval_column].dt.strftime("%y")
        else:
            try:
                display_format = self.INTERVALS[interval_column][KEY_PATTERN]
                df[new_col_name] = df[interval_column].dt.strftime(display_format)
            except KeyError:
                raise ValueError(f"No display format found for interval column '{interval_column}'")

        return df, new_col_name
    
    
    def compute_deltas_as_columns(self, df: pd.DataFrame, interval_column: str, show_delta: bool = False) -> pd.DataFrame:
        """
        Computes delta columns for metrics in-place, naming them using ADD_SPACES and INTERVALS config.
        Delta columns are added as extra columns to the wide-format DataFrame (pre-transpose).
        """
        
        if(show_delta):
            df = df.copy()
            df[interval_column] = pd.to_datetime(df[interval_column])
            df = df.sort_values(by=interval_column)

            interval_config = self.INTERVALS.get(interval_column, {})

            delta_label = interval_config.get(KEY_DELTA, MONTH_DELTA)
            shift_period_delta = interval_config.get(KEY_SHIFT_PERIOD, 1)

            for metric_key, config in self.METRICS_CONFIG.items():
                if metric_key not in df.columns:
                    continue

                add_spaces = config.get(KEY_ADD_SPACES, 0)
                delta_type = config.get(KEY_DELTA_TYPE, PERCENTAGE)

                # === Add delta column
                if show_delta:
                    delta_col = f"{delta_label}{' ' * add_spaces}"
                    shifted = df[metric_key].shift(shift_period_delta)
                    df[delta_col] = ((df[metric_key] / shifted) - 1) if delta_type == PERCENTAGE else (df[metric_key] - shifted) * 100
                    df[delta_col] = df[delta_col].fillna(0)

        return df


    def get_renamed_columns(self, df: pd.DataFrame) -> dict:
        """
        Returns a dictionary to rename metric columns to their display names.
        Only includes columns present in the DataFrame.
        """
        rename_dict = {}

        for metric_key, config in self.METRICS_CONFIG.items():
            if metric_key in df.columns:
                display_name = config.get(KEY_TITLE, metric_key)
                rename_dict[metric_key] = display_name

        return rename_dict
    

    def order_by_position(self, display_df: pd.DataFrame, interval_column: str, show_delta: bool = False) -> dict:
        
        
        interval_config = self.INTERVALS.get(interval_column, {})
        base_delta_suffix = interval_config.get(KEY_DELTA, MONTH_DELTA)

        # === Step 1: Filter + sort metric columns by position
        ordered_metrics = []
        for metric_key, config in self.METRICS_CONFIG.items():
            if metric_key in display_df.columns and KEY_POSITION in config:
                position = config[KEY_POSITION]
                ordered_metrics.append((metric_key, position, config))
        
        ordered_metrics.sort(key=lambda x: x[1])

        # Sort metrics by position
        metric_columns = []
        for metric_key, _, config in ordered_metrics:
            metric_columns.append(metric_key)

            add_spaces = " " * config.get(KEY_ADD_SPACES, 0)

            if show_delta:
                delta_col = f"{base_delta_suffix}{add_spaces}"
                if delta_col in display_df.columns:
                    metric_columns.append(delta_col)


        # === Step 2: Add shared non-metric columns (e.g., interval, geo)
        non_metric_columns = [interval_column, f"{interval_column}{DATE_FORMATTED_SUFFIX}"]
        all_columns = non_metric_columns + metric_columns

        return display_df[all_columns]
    

    def format_transposed_data(self, transposed: pd.DataFrame, interval_column: str) -> pd.DataFrame:
        """
        Formats numbers and delta rows in the transposed (metrics-as-rows) DataFrame.
        Applies formatting rules defined in METRICS_CONFIG.
        
        Args:
            transposed: Transposed DataFrame where rows are metric display names and columns are dates.
            selected_interval: Currently selected interval (e.g., 'month', 'week').

        Returns:
            Formatted DataFrame with values properly styled.
        """

        df = transposed.copy()
        df.set_index(ATD_TRANSPOSED_INDEX, inplace=True)

        # Determine delta label (e.g., "WoW", "DoD", "YoY")
        delta_label = self.INTERVALS[interval_column][KEY_DELTA]

        # Flatten all metric configs for easier lookup
        flat_metric_map = {}
        for metric_key, props in self.METRICS_CONFIG.items():
            display_name = props.get(KEY_TITLE)
            if display_name:
                flat_metric_map[display_name] = {
                    KEY_FORMAT: props.get(KEY_FORMAT),
                    KEY_DELTA_TYPE: props.get(KEY_DELTA_TYPE),
                    KEY_GROWTH_GOOD: props.get(KEY_GROWTH_GOOD),
                }

        last_base_metric = None

        # Format rows
        for row_name in df.index:
            base_name = row_name.strip()

            if base_name not in [delta_label]:
                last_base_metric = row_name
                metric_props = flat_metric_map.get(base_name)
                fmt_type = metric_props.get(KEY_FORMAT)
                if metric_props and fmt_type:
                    df.loc[row_name, df.columns[1:]] = df.loc[row_name, df.columns[1:]].map(
                        lambda x: self.format_numbers(x, fmt_type) if pd.notnull(x) else ""
                    )
            elif base_name in [delta_label] and last_base_metric:
                # Delta row
                metric_props = flat_metric_map.get(last_base_metric)
                delta_type = metric_props.get(KEY_DELTA_TYPE)
                growth_good = metric_props.get(KEY_GROWTH_GOOD)
                if metric_props and delta_type:
                    df.loc[row_name, df.columns[1:]] = df.loc[row_name, df.columns[1:]].map(
                        lambda x: self.format_numbers(x, delta_type, True, growth_good) if pd.notnull(x) else ""
                    )

        df.reset_index(inplace=True)
        
        return df
    
    
    def format_numbers(self, value, format_type=NUMBER, is_delta=False, growth_good=True):
        """
        Formats numbers as plain number, currency, or percentage.

        Parameters:
        - value: The numeric value to be formatted.
        - format_type: The format to apply. Options: NUMBER, CURRENCY, PERCENTAGE.

        Returns:
        - Formatted string representation of the value.
        """

        if isinstance(value, str):
            return value  # Return as-is if conversion fails
        
        # Format as percentage (multiply by 100 and append %)
        if format_type == PERCENTAGE:
            if is_delta:
                if value > 0:
                    return f"{DELTA_UP} {value * 100:.2f}%"
                elif value < 0:
                    return f"{DELTA_DOWN} {abs(value * 100):.2f}%"
                else:
                    return ""
            else:
                return f"{value * 100:.2f}%"

        elif format_type == PP:
            if is_delta:
                if value > 0:
                    return f"{DELTA_UP} {value * 1:.2f} pp"
                elif value < 0:
                    return f"{DELTA_DOWN} {abs(value * 1):.2f} pp"
                else:
                    return ""
            else:
                return f"{value * 1:.2f} pp"

        # Format as currency (assumes MXN, adds $ and thousands separator)
        elif format_type == CURRENCY:
            if value >= 1_000_000:
                return f"${value / 1_000_000:.2f} M"
            elif value >= 1_500:
                return f"${value / 1_000:.2f} K"
            else:
                return f"${value:,.2f}"

        # Default: Format as a number with K/M notation
        elif format_type == NUMBER:
            if value >= 1_000_000:
                return f"{value / 1_000_000:.2f} M"
            elif value >= 1_500:
                return f"{value / 1_000:.2f} K"
            else:
                return f"{value:,.2f}"
        
        elif format_type == MINUTES:
            return f"{value:,.2f} min"
        
        elif format_type == KM:
            return f"{value:,.2f} Km"

        return value  # Return unchanged if format_type is invalid
    

    def display_line_chart(self, filtered_df: pd.DataFrame, 
                           selected_interval_column: str, 
                           column_to_plot: str, 
                           column_to_aggregate: tuple[str, str], 
                           color: tuple[list, list],
                           title_column: str):
        """
        Displays a line chart of the filtered data, showing the average ATD per interval.
        """
        grouped = (
            filtered_df.groupby([selected_interval_column, column_to_plot])
            .agg({column_to_aggregate[0]: column_to_aggregate[1]})
            .reset_index()
        )
        # Calculate overall average ATD per interval
        avg_atd = (
            filtered_df.groupby(selected_interval_column)[column_to_aggregate[0]]
            .mean()
            .reset_index()
        )
        avg_atd[column_to_plot] = "Overall Average"
        # Merge for plotting
        combined_df = pd.concat([grouped, avg_atd])

        if not all(col in combined_df.columns for col in [selected_interval_column, column_to_plot, column_to_aggregate[0]]):
            st.error("Missing required columns for chart.")
            return

        # Split charts
        base_chart = alt.Chart(combined_df)

        color_scale = alt.Scale(domain=color[0], range=color[1])

        color_encoding = alt.Color(f"{column_to_plot}:N", scale=color_scale, title=title_column)

        # Solid lines for courier flows
        flow_chart = base_chart.transform_filter(
            alt.datum[column_to_plot] != "Overall Average"
        ).mark_line().encode(
            x=alt.X(f"{selected_interval_column}:T", title=selected_interval_column.upper()),
            y=alt.Y(f"{column_to_aggregate[0]}:Q", title=f"Average {column_to_aggregate[0]} (minutes)"),
            color=color_encoding,
            tooltip=[column_to_plot, selected_interval_column, f"{column_to_aggregate[0]}"]
        )

        # Dotted line for overall average
        avg_chart = base_chart.transform_filter(
            alt.datum[column_to_plot] == "Overall Average"
        ).mark_line(strokeDash=[4, 4], color='black', size=3.5).encode(
            x=alt.X(f"{selected_interval_column}:T"),
            y=f"{column_to_aggregate[0]}:Q",
            tooltip=[column_to_plot, selected_interval_column, f"{column_to_aggregate[0]}"]
        )

        # Combine
        chart = (flow_chart + avg_chart).properties(
            title=f"{column_to_aggregate[0].upper()} Trend by {title_column.upper()}",
            height=400
        )

        return st.altair_chart(chart, use_container_width=True)
