import os
import sqlite3
import time

# Path to the directory containing the weather data files
data_dir = "/wx_data"

# Connect to the database
conn = sqlite3.connect("weather.db")

# Create a table for the weather data
create_table_sql = """
CREATE TABLE IF NOT EXISTS weather_data (
    
    station_id INTEGER NOT NULL,
    date INTEGER NOT NULL,
    max_temp REAL NOT NULL,
    min_temp REAL NOT NULL,
    precipitation REAL NOT NULL,
    PRIMARY KEY (station_id, date, max_temp, min_temp, precipitation)
)
"""
conn.execute(create_table_sql)

start_time = time.time()


# Iterate through the data files and insert data into the database
for filename in os.listdir(data_dir):
    if filename.startswith("USC"):
        station_id = filename[3:6]
        with open(os.path.join(data_dir, filename), "r") as f:
            for line in f:
                date, max_temp, min_temp, precipitation = line.strip().split("\t")
                # Skip lines with missing data
                if max_temp == "-9999" or min_temp == "-9999" or precipitation == "-9999":
                    continue
                insert_sql = """
                INSERT OR IGNORE INTO weather_data
                (station_id, date, max_temp, min_temp, precipitation)
                VALUES (?, ?, ?, ?, ?)
                """
                conn.execute(insert_sql, (int(station_id), int(date), int(max_temp)/10, int(min_temp)/10, int(precipitation)/10))
conn.commit()

# Print the number of records ingested
select_count_sql = "SELECT COUNT(*) FROM weather_data"
print(f"Number of records ingested: {conn.execute(select_count_sql).fetchone()[0]}")

# Close the connection
conn.close()
end_time = time.time()
print(f'Records were ingested in {end_time - start_time:.2f} seconds')
