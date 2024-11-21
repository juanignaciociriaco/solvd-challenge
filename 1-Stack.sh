#!/bin/bash
export AWS_ACCESS_KEY_ID="ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="SECRET_KEY"
export AWS_DEFAULT_REGION="us-east-1"
TEMPLATES_BUCKET_NAME="juan-cf-templates"
MAIN_STACK_NAME="main-challenge-stack"
if [ -z "$1" ]; then
  echo "You must use 'create' or 'update' as an argument."
  exit 1
fi

# Handle cases based on the provided argument
case "$1" in
  create)
    echo "Executing the create action..."
    aws cloudformation create-stack \
      --stack-name $MAIN_STACK_NAME \
      --template-body file://./MainStack.yaml \
      --parameters \
        ParameterKey=S3TemplateBucketName,ParameterValue=$TEMPLATES_BUCKET_NAME \
        ParameterKey=S3ChallengeBucketName,ParameterValue=juans-challenge-bucket-name1 \
      --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
    ;;
  update)
    echo "Executing the update action..."
    #The following command forces the error when updating the stack by using a non-compatible characters set for the bucket name
      aws cloudformation update-stack \
      --stack-name $MAIN_STACK_NAME \
      --template-body file://./MainStack.yaml \
      --parameters \
        ParameterKey=S3TemplateBucketName,ParameterValue=$TEMPLATES_BUCKET_NAME \
        ParameterKey=S3ChallengeBucketName,ParameterValue="juans-challenge-bucket-name@!" \
      --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
    ;;
  delete)
    echo "Executing the delete action..."
    #The following command forces the error when updating the stack by using a non-compatible characters set for the bucket name
      aws cloudformation delete-stack \
      --stack-name $MAIN_STACK_NAME 
    ;;   
  *)
    echo "Invalid argument. You must use 'create' or 'update'."
    exit 1
    ;;
esac


