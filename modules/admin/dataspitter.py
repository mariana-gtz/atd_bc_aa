import sys
import os
cwd = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(cwd)
from config.constants import *

import pandas as pd
import json
from datetime import datetime


class DataSpitter:
    def __init__(self):

        self.data_path = os.path.join(cwd, DATA_PATH)
        self.last_time_updated_file = os.path.join(self.data_path, LAST_UPDATE_FILE_NAME)

    def save_parquet(self, csv_path: str, parquet_path: str = None):
        """Saves the queried data as a Parquet file."""
        
        if parquet_path is None:
            parquet_path = csv_path.replace('.csv', '.parquet')
        
        string_cols = {
            COL_REGION[0]: COL_REGION[1],
            COL_TERRITORY[0]: COL_TERRITORY[1],
            COL_COUNTRY[0]: COL_COUNTRY[1],
            COL_WORKFLOW[0]: COL_WORKFLOW[1],
            COL_DRIVER[0]: COL_DRIVER[1],
            COL_DELIVERY_TRIP[0]: COL_DELIVERY_TRIP[1],
            COL_COURIER_FLOW[0]: COL_COURIER_FLOW[1],
            COL_GEO_STRATEGY[0]: COL_GEO_STRATEGY[1],
            COL_MERCHANT_SURFACE[0]: COL_MERCHANT_SURFACE[1],
        }

        numeric_cols = {
            COL_PICKUP_DISTANCE[0]: COL_PICKUP_DISTANCE[1],
            COL_DROPOFF_DISTANCE[0]: COL_DROPOFF_DISTANCE[1],
            COL_ATD[0]: COL_ATD[1],
        }

        datetime_cols = [
            COL_RESTO_OFFERED_UTC[0],
            COL_ORDER_FINAL_STATE_LOCAL[0],
            COL_EATER_REQUEST_LOCAL[0],
        ]

        print(f"📥 Loading CSV: {csv_path}")
        df = pd.read_csv(csv_path, dtype=string_cols)
        
        df.replace('\\N', pd.NA, inplace=True)

        print(f"🔄 Processing DataFrame...")
        for col, dtype in numeric_cols.items():
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(dtype)

        for col in datetime_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Calculate additional columns
        df = self.calculate_columns(df)

        print(f"💾 Converting to Parquet: {parquet_path}")
        df.to_parquet(parquet_path, index=False)

        print("\n✅ Conversion Complete!\n")
        print("🔍 Dataset Summary:")
        print("-" * 40)
        print(f"📊 Rows: {df.shape[0]}")
        print(f"📊 Columns: {df.shape[1]}")
        print(f"📦 File size (Parquet): {os.path.getsize(parquet_path) / 1_000_000:.2f} MB\n")
        print("🧱 Columns and Types:")
        print(df.dtypes)
        print("\n📈 Quick Stats:")
        print(df.describe(include='all').transpose())

        return df

    def update_last_time_updated(self, file_name: str):
        """Updates the timestamp for the last data fetch."""
        last_time_updated = {}
        
        if os.path.exists(self.last_time_updated_file):
            with open(self.last_time_updated_file, "r", encoding=ENCODING) as f:
                last_time_updated = json.load(f)

        last_time_updated[file_name] = datetime.now().isoformat(sep=SEP_ISOFORMAT, timespec=TIMESPEC_ISOFORMAT) + SEP_ISOFORMAT + UTC_TIME_ZONE
        
        with open(self.last_time_updated_file, "w", encoding=ENCODING) as f:
            json.dump(last_time_updated, f, indent=4)

        print(f"Updated '{self.last_time_updated_file}' with timestamps for '{file_name}'")
    
    
    def calculate_columns(self, df: pd.DataFrame):
        """Calculates additional columns based on existing data."""
        
        request_time_col = pd.to_datetime(df[COL_EATER_REQUEST_LOCAL[0]])

        df[COL_HOUR[0]] = request_time_col.dt.hour.astype(COL_HOUR[1])
        df[COL_WEEKDAY[0]] = request_time_col.dt.day_name().astype(COL_WEEKDAY[1])
        
        df[COL_DAY[0]] = request_time_col.dt.date.astype(COL_DAY[1])
        
        df[COL_WEEK[0]] = request_time_col - pd.to_timedelta(request_time_col.dt.weekday, unit='d')
        df[COL_WEEK[0]] = df[COL_WEEK[0]].dt.date.astype(COL_WEEK[1])
        
        df[COL_MONTH[0]] = request_time_col.dt.to_period("M").astype(COL_MONTH[1])

        df[COL_TIME_OF_DAY[0]] = df[COL_HOUR[0]].apply(self.map_day_part).astype(COL_TIME_OF_DAY[1])

        # COL_IS_WEEKEND: True if Saturday or Sunday
        df[COL_IS_WEEKEND[0]] = request_time_col.dt.weekday >= 5

        df[COL_IS_SEASONALITY[0]] = df[COL_DAY[0]].apply(
            lambda d: (
                d.strftime(MMDD) in FIXED_SEASONALITIES_MMDD or
                d.isoformat() in VARIABLE_SEASONALITIES_DATES
            )
        )

        df[COL_TOTAL_DISTANCE[0]] = df[COL_PICKUP_DISTANCE[0]] + df[COL_DROPOFF_DISTANCE[0]]

        return df

    # Categorize hour into time blocks
    def map_day_part(self, hour: int) -> str:
        for label, start, end in DAY_PART_RANGES:
            if start <= hour <= end:
                return label
        return "Unknown"
    
    def run(self, csv_path: str, default_file_name: str):
        """Main function to run the data spitter."""
        print("Starting Data Spitter...")
        self.save_parquet(csv_path)
        self.update_last_time_updated(default_file_name)
        print("Data Spitter completed successfully!")
        print("📁 Data Path:", self.data_path)
        print("--------------------------------------------------")


dataspitter = DataSpitter()
dataspitter.run(
    os.path.join(cwd, DATA_PATH, DATA_DEFAULT_FILE_NAME + ".csv"),
    DATA_DEFAULT_FILE_NAME
)

