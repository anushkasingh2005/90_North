# Lambda function to add two numbers (lambda_add.py)
import json

def lambda_handler(event, context):
    try:
        num1 = event['num1']
        num2 = event['num2']
        result = num1 + num2
        return {
            'statusCode': 200,
            'body': json.dumps({'result': result})
        }
    except (KeyError, TypeError):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input. Provide num1 and num2 as numbers.'})
        }

# Lambda function to store a file in S3 (lambda_s3_upload.py)
import boto3
import json
import base64

s3 = boto3.client('s3')
BUCKET_NAME = 'your-s3-bucket-name' # Replace with your bucket name

def lambda_handler(event, context):
    try:
        # Get file information from the event
        file_content = base64.b64decode(event['body'])  # Decode base64 encoded file
        file_name = event['headers']['file-name']
        content_type = event['headers'].get('Content-Type', 'application/octet-stream') # Get content type or set default

        # Upload the file to S3
        s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=file_content, ContentType=content_type)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'File uploaded successfully!'})
        }
    except Exception as e:
        print(f"Error uploading file: {e}") # Log the error for debugging
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}) # Return the error message
        }