#!/bin/bash
export AWS_ACCESS_KEY_ID="ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="SECRET_KEY"
export AWS_DEFAULT_REGION="us-east-1"
BUCKET_NAME="juan-cf-templates"
FILE_PATH="./Substack.yaml"
S3_PATH="s3://$BUCKET_NAME/Substack.yaml"

# Check if the bucket exists
aws s3api head-bucket --bucket $BUCKET_NAME 2>/dev/null

# If the bucket does not exist, create it
if [ $? -ne 0 ]; then
  echo "Bucket does not exist. Creating the bucket..."
  aws s3api create-bucket --bucket $BUCKET_NAME --region $AWS_DEFAULT_REGION
fi

# Upload the file to S3
echo "Uploading the file to S3 bucket..."
aws s3 cp $FILE_PATH $S3_PATH

echo "File successfully uploaded to $S3_PATH"
