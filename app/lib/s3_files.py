# app/lib/s3_files.py
import os
import boto3
from ..lib.cache_it import cache_it_sync, cache_it_async

def get_s3_client():
    return boto3.client(
        's3',
        region_name=os.getenv('FS_REGION'),
        endpoint_url=os.getenv('FS_ENDPOINT'),
        aws_access_key_id=os.getenv('FS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('FS_SECRET_ACCESS_KEY')
    )

def upload_to_s3(file_key, file_content, bucket=os.getenv('FS_BUCKET_NAME')):
    s3 = get_s3_client()
    try:
        s3.put_object(Bucket=bucket, Key=file_key, Body=file_content)
        print("Upload Successful")
        return True
    except Exception as e:
        print("An error occurred:", e)
        return False 

def check_file_exists(file_path, bucket=os.getenv('FS_BUCKET_NAME')):
    s3 = get_s3_client()
    try:
        s3.head_object(Bucket=bucket, Key=file_path)
        return True
    except s3.exceptions.NoSuchKey:
        return False
    except Exception as e:
        return False

def generate_presigned_url(file_key, expiration=3600, bucket=os.getenv('FS_BUCKET_NAME')):
    s3 = get_s3_client()
    try:
        if not check_file_exists(file_key): # Added Extra Check if file exists
            return None            
        response = s3.generate_presigned_url('get_object',
                                              Params={'Bucket': bucket,
                                                      'Key': file_key},
                                              ExpiresIn=expiration)
        return response
    except Exception as e:
        print("An error occurred:", e)
        return None    
    
    
@cache_it_sync()
def get_one_file_in_bucket(prefix, bucket=os.getenv('FS_BUCKET_NAME')):
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=1)
    files = [obj for obj in response.get('Contents', []) if not obj['Key'].endswith("/")]
    if not files:
        return None
    return files[0]['Key']

def move_file_in_bucket(old_file_key, new_file_key, bucket=os.getenv('FS_BUCKET_NAME')):
    s3 = get_s3_client()
    try:
        s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': old_file_key}, Key=new_file_key)
        s3.delete_object(Bucket=bucket, Key=old_file_key)
        print("Move Successful")
        return True
    except Exception as e:
        print("An error occurred:", e)
        return False

def delete_file_from_bucket(file_key, bucket=os.getenv('FS_BUCKET_NAME')):
    s3 = get_s3_client()
    try:
        s3.delete_object(Bucket=bucket, Key=file_key)
        print("Delete Successful")
        return True
    except Exception as e:
        print("An error occurred:", e)
        return False