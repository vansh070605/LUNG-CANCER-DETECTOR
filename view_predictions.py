import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('database.db')

# SQL Query to select all data from the predictions table
query = "SELECT * FROM predictions"

# Read data into a pandas DataFrame
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Display the DataFrame
print("\nLung Cancer Predictions History:\n")
print(df.to_string(index=False))  # Print without the default index column
