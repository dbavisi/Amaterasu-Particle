# Amaterasu Particle
# Dwij Bavisi <dwij@dbavisi.net>

"""
Release 0, Hotfix Pack 0, Hotfix 2

This module performs the configuration for AWS Simple Storage Service (S3) for storing mailboxes.
"""

import json
import boto3

def create_mailbox(region: str, environment: str, rootDomain: str) -> str:
    """
    Configures AWS S3 bucket for storing mailboxes.

    :param region: AWS region (e.g. us-east-1).
    :param environment: Target deployment environment (e.g. delta, horizon, void).
    :param rootDomain: Root domain for the mailbox (e.g. dbavisi.net).

    :return mailbox: Bucket name for the mailbox.

    Requires following AWS permissions:
    - s3:ListBucket (required by head_bucket, for checking if bucket exists)
    - s3:CreateBucket (required by create_bucket, for creating bucket)
    """
    print(f"Using region: {region}")
    s3_client = boto3.client('s3', region_name=region)

    print(f"Setting up mailbox for {rootDomain} in {environment} environment...")
    if environment == 'void':
        mailbox = f"mailbox.{rootDomain}"
    else:
        mailbox = f"mailbox.{environment}.{rootDomain}"

    print(f"... Checking if bucket {mailbox} exists...")
    try:
        response = s3_client.head_bucket(Bucket=mailbox)
        print(json.dumps(response, indent=4))
        print(f"... ... Existing bucket {mailbox} will be reused.")
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f"... Bucket {mailbox} does not exist. Creating ...")
            response = s3_client.create_bucket(Bucket=mailbox)
            print(f"... ... Create bucket {mailbox} completed with response:")
            print(json.dumps(response, indent=4))
        else:
            print(f"... Error checking bucket {mailbox}: {e}")
            raise Exception(f"Error checking bucket {mailbox}: {e}") from e

    print("... Mailbox setup complete.")

    return mailbox
