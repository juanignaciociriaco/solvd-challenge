
export AWS_ACCESS_KEY_ID="ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="SECRET_KEY"
export AWS_DEFAULT_REGION="us-east-1"
MAIN_STACK_NAME="main-challenge-stack"
pip3 install boto3 --break-system-packages &>/dev/null
python3 stack-status.py $MAIN_STACK_NAME
