class InvalidClientError(Exception):
    def __str__(self):
        return "'client' is not a valid Boto3 or Botocore CloudFormation client."


class StackFailedError(Exception):
    stack_name: str

    def __init__(self, stack_name: str):
        self.stack_name = stack_name

    def __str__(self):
        return f'Stack {self.stack_name} is failed.'
