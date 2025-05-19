import sys
import os
cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(cwd)
from config.constants import *
from modules.controllers.atd_view_controller import ATDController


import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

atd_controller = ATDController()

st.title(atd_controller.page_title)

selected_menu = option_menu(
    menu_title = atd_controller.menu_title,
    options = atd_controller.options,
    icons = atd_controller.icons,
    menu_icon = atd_controller.menu_icon,
    default_index = atd_controller.default_index,
    orientation = atd_controller.orientation,
)


if(selected_menu == atd_controller.options[0]):
    filtered_df, selections = atd_controller.get_filtered_data()
    selected_interval = selections[INTERVAL]
    selected_interval_column = atd_controller.get_interval_column(selected_interval)

    # Ensure datetime (if not already)
    interval_series = pd.to_datetime(filtered_df[DAY])
    # Get min/max dates
    start_date = interval_series.min().strftime(DAY_PATTERN)
    end_date = interval_series.max().strftime(DAY_PATTERN)
    st.markdown(
        f"""
        <div style='text-align: right;'>
            <em>*Data available from <span style='font-weight:600;'>{start_date}</span> to <span style='font-weight:600;'>{end_date}</span>.</em>
        </div>
        """,
        unsafe_allow_html=True
    )    
    
    # Step 1: Toggles
    st.subheader(atd_controller.page_subheader)
    toggles_to_show = atd_controller.get_toggles_to_show(selected_interval_column)
    toggle_cols = st.columns((len(toggles_to_show) + 1) * TOGGLES_COL_MULTIPLIER)
    toggle_states = {}

    for i, (toggle_id, toggle_cfg) in enumerate(toggles_to_show.items()):
        with toggle_cols[i]:
            toggle_states[toggle_id] = st.toggle(
                label=toggle_cfg[KEY_LABEL],
                value=toggle_cfg[KEY_VALUE],
                key=toggle_cfg[KEY_KEY]
            )

    show_deltas = toggle_states[KEY_SHOW_DELTA_TOGGLE]
    show_actuals = toggle_states[KEY_SHOW_RAW_TOGGLE]

    # Step 2: Aggregation for first level metrics
    grouped_df = atd_controller.get_aggregated_data(filtered_df, selected_interval_column)    

    # Step 3: Metric Calculations (scalar + formula-based)
    calculated_df = atd_controller.apply_metric_calculations(grouped_df)

    # Step 4: Filter & order positioned metrics only
    display_df = atd_controller.filter_positioned_metrics(calculated_df, selected_interval_column)
    display_df.sort_values(by=display_df.columns[0], inplace=True)

    # Step 5: Apply deltas if needed
    if(show_deltas):
        display_df = atd_controller.compute_deltas_as_columns(display_df, selected_interval_column, show_deltas)

    display_df = atd_controller.order_by_position(display_df, selected_interval_column, show_deltas)
    
    with st.expander("Key Metrics Overview", expanded=True):

        if(selected_interval_column == DAY and show_deltas):
            st.info(
                f"Delta values are calculated as {DAY_DELTA} (Day over Day compared to the same day of the previous week)",
                icon="ℹ️",
            )
        
        rename_dict = atd_controller.get_renamed_columns(display_df)
        renamed_df = display_df.rename(columns=rename_dict)

        renamed_df.set_index(renamed_df.columns[0], inplace=True)
        transposed = renamed_df.T  # Flip: metrics now as rows, dates as columns
        transposed = transposed.sort_index(axis=1, ascending=True)

        formated_column_names = transposed.iloc[0].tolist()
        
        transposed = transposed.iloc[1:] # Remove formatted date row
        transposed.columns = formated_column_names

        transposed.index.name = ATD_TRANSPOSED_INDEX

        # Generate sparkline values: list of numeric values per row
        sparkline_data = transposed.copy()
        sparkline_values = sparkline_data.iloc[:, :].apply(lambda row: row.tolist(), axis=1)

        # Insert the Sparkline column BEFORE reset_index
        transposed.insert(0, ATD_TRANSPOSED_SPARKLINE_COLUMN, sparkline_values)

        # Reset index so first column appears
        transposed = transposed.reset_index()

        if(show_actuals == False):
            formatted_transposed = atd_controller.format_transposed_data(transposed, selected_interval_column)
        else:
            formatted_transposed = transposed.copy()
        
        # Convert dataframe to AG-Grid compatible format
        grid_options = GridOptionsBuilder.from_dataframe(formatted_transposed)
        grid_options.configure_column(ATD_TRANSPOSED_INDEX, resizable=False, pinned="left")
        grid_options.configure_column(
            ATD_TRANSPOSED_SPARKLINE_COLUMN,
            header_name = ATD_TRANSPOSED_SPARKLINE_COLUMN,
            width=120,
            cellRenderer='agSparklineCellRenderer',
            cellRendererParams={
                "sparklineOptions": {
                    "type": "line",
                    "line": {"stroke": "#0F462D", "strokeWidth": 2},
                    "highlightStyle": {"size": 3, "fill": "#FF6937", "stroke": "#FF6937"},
                    "padding": {"top": 5, "bottom": 5},
                }
            }
        )

        cell_style_js = JsCode("""
                function(params) {
                    let value = params.value ? params.value.toString() : "";
                    let metricName = params.data?.Metric || "";

                    if (params.column.colId === "Metric" && params.data.Metric) {
                        const metric = params.data.Metric;
                        const deltaRegex = /^(MoM|DoD|WoW|YoY|QoQ)/;
                        const identRegex = /(Pickup|Dropoff)/;
                
                        if (deltaRegex.test(metric)) {
                            return {
                                fontStyle: "italic",
                                fontSize: "11px",
                                fontWeight: "300",
                                textAlign: "right",
                                paddingLeft: "24px",
                                
                            };
                        } 
                        else if(identRegex.test(metric)) {
                            return {
                                paddingLeft: "34px",
                                fontSize: "12px",
                                fontWeight: "bold",
                            };
                        }
                        else {
                            return {
                                fontSize: "13px",
                                fontWeight: "bold",
                            };
                        }
                    }

        
                    // All other columns: color arrows based on metric context
                    if (value.includes("▲") || value.includes("▼")) {
                        const badIfUp = / {2,}/i.test(metricName); // e.g., WoW    

                        const baseStyle = {
                            fontWeight: "300",
                            fontStyle: "italic",
                            fontSize: "11px"
                        };

                        if (value.includes("▲")) {
                            return {
                                ...baseStyle,
                                color: badIfUp ? "#ff8080" : "#349966"  // Red if up is bad
                            };
                        } else if (value.includes("▼")) {
                            return {
                                ...baseStyle,
                                color: badIfUp ? "#349966" : "#ff8080"  // Green if down is good
                            };
                        }
                    }
                               
                    return {};
                }
                """)

        for col in formatted_transposed.columns:
            if col not in [ATD_TRANSPOSED_SPARKLINE_COLUMN]:
                grid_options.configure_column(col, width=100, cellStyle=cell_style_js)

                
        grid_options.configure_default_column(filterable=True, sortable=False, editable=False)

        # Enable auto-sizing for all other columns
        grid_options.configure_grid_options(
                                            suppressMovableColumns=True,
                                            enableRangeSelection=True,
                                            enableCellTextSelection=True,
                                            suppressHorizontalScroll=False,
                                            suppressRowVirtualisation=False,
                                            suppressClipboardPaste=False,
                                            suppressCopyRowsToClipboard=False
                                            )

        # Apply header and first column color styles
        custom_css = {
            
            ".ag-header-cell.ag-focus-managed": {
                "background-color": "#0F462D !important",
                "color": "white !important",
                "font-weight": "bold !important",
                "font-size": "12px"
            },

            ".ag-row-hover": {
                "background-color": "#06C167 !important",
                "color": "black !important",
            },

            ".ag-icon-menu": {
                "color": "white !important",
            },
        
        }
        
        grid_options.configure_grid_options(domLayout="autoHeight")

        AgGrid(
            formatted_transposed,
            gridOptions = grid_options.build(),
            fit_columns_on_grid_load = False,
            allow_unsafe_jscode = True,  # Required for JavaScript-based styling
            custom_css = custom_css,
            theme = "balham",
        )
    
    st.divider()

    st.subheader("📊 Charts Overview (expand if needed)")
    
    with st.expander("ATD Charts Overview", expanded=True):
        st.info(
            f"""
            📌 Filters applied will be reflected in the charts below.
            📅 The charts are grouped by **{selected_interval_column}** and show the average ATD (Actual Time of Delivery) for each category.  
            🎯 **Dotted line** indicates the overall **average ATD** for the selected filters.  
            """
        )
        # Create columns for the charts
        col1, col2 = st.columns(2)

        # Chart 1: Trips by workflow (stacked by geo_strategy)
        with col1:
            atd_controller.display_line_chart(filtered_df, 
                                            selected_interval_column, 
                                            COL_COURIER_FLOW[0],
                                            (COL_ATD[0], "mean"), 
                                            (["Fleet", "UberX", "UberEats", "SUV", "Onboarder", "Logistics", "Motorbike"],
                                            ["#6c9df8", "#4fc78d", "#ffe27c", "#ff8961", "#ff7bb0", "#9a60ef", "#4ac8db"]),
                                            "Courier Flow",)
            
        with col2:
            atd_controller.display_line_chart(filtered_df, 
                                            selected_interval_column, 
                                            COL_TIME_OF_DAY[0],
                                            (COL_ATD[0], "mean"), 
                                            (["Late Night", "Dinner", "Breakfast", "Lunch"],
                                            ["#e11497", "#9b14e1", "#1a14e1", "#14cce1"]),
                                            "Time of Day",)
            

        col3, col4 = st.columns(2)
        with col3:
            atd_controller.display_line_chart(filtered_df, 
                                            selected_interval_column, 
                                            COL_WEEKDAY[0],
                                            (COL_ATD[0], "mean"), 
                                            (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                            ["#b39df4", "#f49de6", "#9da9f4", "#9df4eb", "#9df4a9", "#f4d09d", "#f49d9d"]),
                                            "Weekday",)
        
        with col4:
            atd_controller.display_line_chart(filtered_df, 
                                            selected_interval_column, 
                                            COL_MERCHANT_SURFACE[0],
                                            (COL_ATD[0], "mean"), 
                                            (["Other", "POS", "Tablet", "Unspecified", "Web/Mobile"],
                                            ["#6c9df8", "#4fc78d", "#ffe27c", "#ff8961", "#ff7bb0"]),
                                            "Merchant Surface",)

        col5, col6 = st.columns(2)
        with col5:
            atd_controller.display_line_chart(filtered_df, 
                                            selected_interval_column, 
                                            COL_GEO_STRATEGY[0],
                                            (COL_ATD[0], "mean"), 
                                            (["Drive momentum", "Play offense", "Defend CP", "Build experience", "Unlaunched", "Unspecified"],
                                            ["#fed743", "#03c167", "#004c28", "#980000", "#969696", "#565656"]),
                                            "Geo Strategy",)

        with col6:
            atd_controller.display_line_chart(filtered_df, 
                                            selected_interval_column, 
                                            COL_TERRITORY[0],
                                            (COL_ATD[0], "mean"), 
                                            (["Central", "North", "West", "South East", "Long Tail - Region"],
                                            ["#6bbb00", "#6c9df8", "#ff7373", "#ffe27c", "#f2998e"]),
                                            "Territory",)


elif (selected_menu == atd_controller.options[1]):
    st.subheader(ATD_OPTION_MENU_OPTIONS[1])
    st.markdown("""
    ### 📌 Key Metrics  
    1. **Region (string)**: The broader region the city belongs to. *(e.g. "Mexico")*  
    2. **Territory (string)**: A subdivision within a region that denotes a more specific zone, such as a territorial division or operational area *(e.g., "Central", "North", "West", "South East", "Long Tail - Region")*  
    3. **Country Name (string)**: The name of the country where the delivery or service is being performed *(e.g. "Mexico")*  
    4. **Workflow UUID (string)**: Unique identifier for a specific workflow *(e.g. "8c393c94-9282-41a6-a885-7a6e84b470d7")*  
    5. **Driver UUID (string)**: Unique identifier for the driver *(e.g. "d16e401c-795d-4295-96c0-85ca08ad8c42")*  
    6. **Delivery Trip UUID (string)**: Unique identifier for a specific delivery trip *(e.g. "715f96aa-0a31-46f6-b856-6ea6f87affad")*  
    7. **Courier Flow (string)**: The type of transport used *(e.g. "Motorbike", "UberEats", "Logistics")*  
    8. **Restaurant Offered Timestamp UTC (timestamp)**: When the restaurant received the order *(e.g. 2025-03-23 02:14:55.000)*  
    9. **Order Final State Timestamp Local (timestamp)**: When the order reached its final status *(e.g. 2025-03-22 21:05:52)*  
    10. **Eater Request Timestamp Local (timestamp)**: When the customer made the order *(e.g. 2025-03-22 20:14:54)*  
    11. **Geo Archetype (string)**: Strategic region classification *(e.g. "Play offense", "Defend CP")*  
    12. **Merchant Surface (string)**: Interface used by the merchant *(e.g. "Tablet", "POS", "Web/Mobile")*  
    13. **Pickup Distance (float)**: Distance from driver accept to pickup point *(e.g. 3.448)*  
    14. **Dropoff Distance (float)**: Distance from pickup point to delivery location *(e.g. 6.451)*  
    15. **Actual Time of Delivery - ATD (float)**: Time from offer to final delivery in minutes *(e.g. 50.97)*

    ---

    ### 🧮 Additional Metrics (calculated)

    1. **Hour (int64)**: Hour of the day (0–23) *(e.g. 14)*  
    2. **Weekday (string)**: Day of the week *(e.g. "Monday")*  
    3. **Day (datetime)**: Calendar day with time reset *(e.g. "2025-03-22 00:00:00")*  
    4. **Week (datetime)**: Start of the week *(e.g. "2025-03-17")*  
    5. **Month (datetime)**: First day of the month *(e.g. "2025-03-01")*  
    6. **Time of Day (string)**: Categorized hour bucket:
    - `Breakfast`: 5–11  
    - `Lunch`: 12–16  
    - `Dinner`: 17–23  
    - `Late Night`: 0–4  
    7. **Is Weekend? (bool)**: `True` if Saturday or Sunday *(e.g. True)*  
    8. **Is Holiday? (bool)**: `True` if the date is a known holiday *(e.g. False)*  
    9. **Total Distance (float)**: `Pickup Distance` + `Dropoff Distance` *(e.g. 4.5769997)*
    """)
