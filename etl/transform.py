import os
import pandas as pd
from config.config import DATABASE_CONFIG
import psycopg2

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=DATABASE_CONFIG['host'],
            port=DATABASE_CONFIG['port'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            database=DATABASE_CONFIG['database']
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def clean_csv_data(file_path):
    df = pd.read_csv(file_path)
    df = df.dropna()
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.drop_duplicates()
    df = df[df['email'].str.contains(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', na=False)]
    return df

def clean_json_data(file_path):
    df = pd.read_json(file_path)
    df = df.dropna()
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.drop_duplicates()
    df = df[df['email'].str.contains(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', na=False)]

    return df

def save_cleaned_data(df, file_path):
    if file_path.endswith(".csv"):
        df.to_csv(file_path, index=False)
    elif file_path.endswith(".json"):
        df.to_json(file_path, orient="records", lines=True)
    print(f"Исходный файл успешно обновлен: {file_path}")

def process_data(base_path):
    for root, _, files in os.walk(base_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            print(f"Processing file: {file_path}")

            if file_name.endswith(".csv"):
                cleaned_df = clean_csv_data(file_path)
            elif file_name.endswith(".json"):
                cleaned_df = clean_json_data(file_path)
            else:
                print(f"Unsupported file type: {file_name}")
                continue

            save_cleaned_data(cleaned_df, file_path)

if __name__ == "__main__":
    base_path = "../data_lake"
    process_data(base_path)