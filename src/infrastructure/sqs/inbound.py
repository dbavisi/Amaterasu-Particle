# Amaterasu Particle
# Dwij Bavisi <dwij@dbavisi.net>

"""
Release 0, Hotfix Pack 0, Hotfix 2

This module performs the configuration for AWS Simple Queue Service (SQS) for handling inbound emails.
"""

import json
import boto3

def create_inbound(region: str, domain: str) -> str:
    """
    Configures AWS SQS queue for handling inbound emails.

    :param region: Queue region (e.g. us-east-1).
    :param domain: Domain for the mailbox (e.g. dbavisi.net).

    :return inboundMail: Queue name for the inbound mailbox.

    Requires following AWS permissions:
    - sqs:GetQueueUrl (required by get_queue_url, for checking if queue exists)
    - sqs:CreateQueue (required by create_queue, for creating queue)
    """
    print(f"Using region: {region}")
    sqs_client = boto3.client('sqs', region_name=region)

    inboundMail = f"inboundMail_{domain.replace('.', '-')}"
    print(f"Checking if queue {inboundMail} exists...")
    try:
        response = sqs_client.get_queue_url(QueueName=inboundMail)
        print(json.dumps(response, indent=4))
        print(f"... Existing queue {inboundMail} will be reused.")
    except sqs_client.exceptions.QueueDoesNotExist as e:
        print(f"... Queue {inboundMail} does not exist. Creating ...")
        response = sqs_client.create_queue(QueueName=inboundMail)
        print(f"... ... Create queue {inboundMail} completed with response:")
        print(json.dumps(response, indent=4))
    except sqs_client.exceptions.ClientError as e:
        print(f"... Error checking queue {inboundMail}: {e}")
        raise Exception(f"Error checking queue {inboundMail}: {e}") from e

    print("... Inbound queue setup complete.")

    return inboundMail
