import pandas as pd
import requests
from pymongo import MongoClient
from datetime import datetime

def download_and_normalize_data(file_path):
    url = 'https://api.mockaroo.com/api/501b2790?count=1000&key=8683a1c0'
    response = requests.get(url)
    
    if response.status_code == 200:
        # Save the CSV file locally
        with open(file_path, 'wb') as file:
            file.write(response.content)

        # Check if file is downloaded
        print(f"File downloaded to {file_path}")

        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Normalize data (example: remove leading/trailing spaces from column names and convert to lower case)
        df.columns = df.columns.str.strip().str.lower()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        # Add a timestamp column
        df['timestamp'] = datetime.utcnow()

        # Save the normalized data back to CSV
        df.to_csv(file_path, index=False)
        
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['data_db']  # Use or create the database
        collection = db['data_collection']  # Use or create the collection
        
        # Create TTL index on the timestamp field (expires after 10 minutes)
        collection.create_index([('timestamp', 1)], expireAfterSeconds=600)
        
        # Clear existing data before inserting new data
        collection.delete_many({})
        
        # Convert DataFrame to dictionary and insert into MongoDB
        data_dict = df.to_dict(orient='records')
        collection.insert_many(data_dict)
        
        print("Data saved to MongoDB successfully.")
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")
