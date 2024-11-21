# Challenge
# Write a python script that takes as input the name of a CloudFormation stack and
# 1. outputs the current status of the stack
# 2. if the stack is in a rollback state, outputs the name of the resource that triggered the rollback and the error message
# 3. (for extra points) if the resource in #3 is a nested stack, outputs the name of the resource in the nested stack that triggered the rollback and the error message
# Note:
# 1. AWS credentials and region will be supplied to the script as environment variables.
# 2. the script output should be JSON-formatted.
#
import boto3
import os
import json
import sys

def get_stack_status(stack_name):
    try:
        # Create CF Client
        cf_client = boto3.client(
            'cloudformation',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION')
        )

        # Get stack status passed as a arg
        response = cf_client.describe_stacks(StackName=stack_name)
        stack = response['Stacks'][0]
        status = stack['StackStatus']
        output = {"StackStatus": status}

        # If rollback state then show
        if status in ['ROLLBACK_IN_PROGRESS', 'ROLLBACK_COMPLETE', 'UPDATE_ROLLBACK_IN_PROGRESS', 'UPDATE_ROLLBACK_COMPLETE']:
            output["RollbackInfo"] = get_rollback_info(stack_name, cf_client)
        
        print(json.dumps(output, indent=4))
    except Exception as e:
        print(json.dumps({"Error": str(e)}))


def get_rollback_info(stack_name, cf_client):
    try:
        # Get events from stack
        response = cf_client.describe_stack_events(StackName=stack_name)
        events = response['StackEvents']
        
        rollback_info = []
        for event in events:
            if 'ROLLBACK' in event['ResourceStatus']:
                resource_name = event['LogicalResourceId']
                error_message = event.get('ResourceStatusReason', 'No error message')
                
                # Check if the resource is a stack - which will mean nested
                if event['ResourceType'] == 'AWS::CloudFormation::Stack':
                    nested_stack_name = event['PhysicalResourceId']
                    nested_stack_error_info = get_nested_stack_error(nested_stack_name, cf_client)
                    rollback_info.append({
                        "ResourceName": resource_name,
                        "ErrorMessage": error_message,
                        "NestedStackError": nested_stack_error_info
                    })
                else:
                    rollback_info.append({
                        "ResourceName": resource_name,
                        "ErrorMessage": error_message
                    })
        
        return rollback_info if rollback_info else {"Message": "No rollback resources found."}
    except Exception as e:
        return {"Error": str(e)}


def get_nested_stack_error(nested_stack_name, cf_client):
    try:
        # Gets nested stack errors
        response = cf_client.describe_stack_events(StackName=nested_stack_name)
        events = response['StackEvents']
        for event in events:
            if 'ROLLBACK' in event['ResourceStatus']:
                resource_name = event['LogicalResourceId']
                error_message = event.get('ResourceStatusReason', 'No error message')
                return {
                    "NestedStackResourceName": resource_name,
                    "NestedStackErrorMessage": error_message
                }
        return {"Message": "No rollback events found in nested stack"}
    except Exception as e:
        return {"Error": f"Failed to retrieve nested stack events: {str(e)}"}


if __name__ == "__main__":
    # Checks if length is more than two
    if len(sys.argv) != 2:
        print(json.dumps({"Error": "Please provide the stack name as an argument"}))
        sys.exit(1)
    
    stack_name = sys.argv[1]
    
    # Calling main function
    get_stack_status(stack_name)
