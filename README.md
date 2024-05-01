# Application Status

Work in progress. PDF file types are not supported currently.

# Setup: Backend

- Requirements: AWS Textract, S3 Buckets, Lambda, DynamoDB, and Python.
- Create a default S3 bucket with a folder named "upload/" for receipts.
- Configure a lambda with the necessary code from the provided backend folder.
- Add AWS Layer to lambda: AWSSDKPandas-Python312, version 4.
- Connect the S3 buckets to the Lambda by creating a trigger in the Lambda
- Generate Access Key ID and Secret Access Key from your AWS account. 

# Setup: Frontend

- Navigate to frontend/src/pages/homePage.
- Update the S3 upload function with Access Key ID, Secret Access Key, and region (Should be around line 13).
- Replace the "Bucket" field with your S3 bucket name (Around line 42)
- Repeat the following in the "View Pages" file, but for the "Tablename: " field in the deleteScan function and the useEffect function, update it so that it matches your DynamoDB table name.

# Known Bugs / Limitations

- Uploading a PDF image to S3 results in an "unsupported file type" error.
