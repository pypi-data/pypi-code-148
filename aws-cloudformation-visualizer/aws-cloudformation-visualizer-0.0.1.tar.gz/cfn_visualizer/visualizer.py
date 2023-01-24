import time
import botocore.client

from .exceptions import InvalidClientError, StackFailedError
from .utils import print_event


def visualizer(client: botocore.client.BaseClient, stack_name: str):
    try:
        if isinstance(client, botocore.client.BaseClient):
            event_count = _initial_visualize(client, stack_name)

            while True:
                stack_response = client.describe_stacks(StackName=stack_name)
                stack_status = stack_response['Stacks'][0]['StackStatus']
                stack_name = stack_response['Stacks'][0]['StackId']

                if 'FAILED' in stack_status or 'ROLLBACK' in stack_status:  # creation, deletion, update failed
                    raise StackFailedError(stack_name)

                elif 'COMPLETE' in stack_status:
                    return

                else:
                    events = client.describe_stack_events(StackName=stack_name)['StackEvents']

                    if len(events) > event_count:
                        remainder_count = len(events) - event_count

                        for i in range(remainder_count - 1, 0, -1):
                            print_event(events[i])

                        event_count = len(events)

                    time.sleep(1)

        else:
            raise InvalidClientError

    except InvalidClientError as e:
        print(e)

    except StackFailedError as e:
        print(e)

    except KeyboardInterrupt:
        return


def _initial_visualize(client: botocore.client.BaseClient, stack_name: str):
    events = client.describe_stack_events(StackName=stack_name)['StackEvents']
    events = sorted(events, key=lambda x: x['Timestamp'])
    event_count = 0

    for event in events:
        print_event(event)

        event_count += 1

    return event_count
