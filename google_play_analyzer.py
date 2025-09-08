import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandasql import sqldf

# --- 1. Data Collection & Initial Assessment ---
file_path = 'googleplaystore.csv'

try:
    df = pd.read_csv(file_path)
    
    # --- 2. Data Cleaning ---
    df = df.drop(df[df['Category'] == '1.9'].index)
    df['Rating'] = df['Rating'].fillna(df['Rating'].mean())
    df.dropna(inplace=True)
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
    df['Installs'] = df['Installs'].apply(lambda x: x.replace(',', '').replace('+', ''))
    df['Installs'] = pd.to_numeric(df['Installs'])
    df['Price'] = df['Price'].apply(lambda x: x.replace('$', ''))
    df['Price'] = pd.to_numeric(df['Price'])
    
    # --- 3. Exploratory Data Analysis (EDA) with Python ---
    print("\n--- Exploring Key Trends with Python ---")
    
    # Analysis 1: Top 10 App Categories by Average Rating
    avg_ratings = df.groupby('Category')['Rating'].mean().sort_values(ascending=False).head(10)
    print("\nTop 10 App Categories by Average Rating (Python):")
    print(avg_ratings)
    
    # Analysis 2: Total Installs by App Type (Free vs. Paid)
    app_type_installs = df.groupby('Type')['Installs'].sum().sort_values(ascending=False)
    print("\nTotal Installs by App Type (Python):")
    print(app_type_installs)


    # --- 4. Running SQL Queries on the DataFrame ---
    print("\n--- Verifying Findings with SQL ---")
    
    # We will use this line to create a temporary table for our queries.
    globals()['df'] = df

    # SQL Query 1: Find the top 10 app categories by average rating, just like we did with Python.
    sql_query_1 = """
    SELECT Category, AVG(Rating) AS AverageRating
    FROM df
    GROUP BY Category
    ORDER BY AverageRating DESC
    LIMIT 10;
    """
    top_categories_sql = sqldf(sql_query_1)
    print("\nTop 10 App Categories by Average Rating (SQL):")
    print(top_categories_sql)

    # SQL Query 2: Find the total number of installs by app type (Free vs. Paid).
    sql_query_2 = """
    SELECT Type, SUM(Installs) AS TotalInstalls
    FROM df
    GROUP BY Type
    ORDER BY TotalInstalls DESC;
    """
    app_type_installs_sql = sqldf(sql_query_2)
    print("\nTotal Installs by App Type (SQL):")
    print(app_type_installs_sql)

    # SQL Query 3: Find the top 5 most expensive apps
    sql_query_3 = """
    SELECT App, Price
    FROM df
    ORDER BY Price DESC
    LIMIT 5;
    """
    most_expensive_apps = sqldf(sql_query_3)
    print("\nTop 5 Most Expensive Apps (SQL):")
    print(most_expensive_apps)
    
    print("\n--- Project complete and matches your resume! ---")
    
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    print("Please make sure you have downloaded the CSV file and placed it in the correct folder.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
