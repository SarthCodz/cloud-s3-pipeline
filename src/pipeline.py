import os
import boto3
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def get_s3_client():
    """Initializes and returns the boto3 S3 client using credentials from environment variables."""
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=AWS_REGION
    )

def process_cloud_data(file_key: str):
    """
    Downloads a raw dataset from S3, cleans/transforms it with Pandas,
    and uploads the processed result back to S3.
    """
    s3 = get_s3_client()
    
    print(f"--> Fetching S3 Object: s3://{BUCKET_NAME}/{file_key}")
    
    # 1. Local path execution setup
    local_input = "temp_input.csv"
    local_output = "temp_output.csv"
    
    try:
        # 2. Download raw file from S3 bucket
        s3.download_file(BUCKET_NAME, file_key, local_input)
        print("--> Raw file successfully downloaded locally.")
        
        # 3. Perform data cleaning & transformation using Pandas
        df = pd.read_csv(local_input)
        
        # Clean missing values and reset index
        df.dropna(inplace=True)
        
        # Save processed data locally before upload
        df.to_csv(local_output, index=False)
        print("--> Data transformation complete.")
        
        # 4. Upload processed data back to S3
        file_name = file_key.split("/")[-1]
        output_key = f"processed/cleaned_{file_name}"
        
        s3.upload_file(local_output, BUCKET_NAME, output_key)
        print(f"--> Success! Processed dataset saved to: s3://{BUCKET_NAME}/{output_key}")

    except Exception as e:
        print(f"Error executing cloud pipeline: {str(e)}")
        
    finally:
        # 5. Clean up temporary local files to prevent residual data storage
        if os.path.exists(local_input):
            os.remove(local_input)
        if os.path.exists(local_output):
            os.remove(local_output)

if __name__ == "__main__":
    print("Cloud Data Pipeline Service Initialized.")