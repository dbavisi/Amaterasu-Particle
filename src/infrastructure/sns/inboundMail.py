# Amaterasu Particle
# Dwij Bavisi <dwij@dbavisi.net>

"""
Release 0, Hotfix Pack 0, Hotfix 2

This module performs the configuration for AWS Simple Notification Service (SNS) for handling inbound emails.
"""

import os
import json
import boto3

def create_inboundMail(region: str, domain: str) -> str:
    """
    Configures AWS SNS queue for handling inbound emails.

    :param region: AWS region (e.g. us-east-1).
    :param domain: Domain for the mailbox (e.g. dbavisi.net).

    :return inboundMail: Topic name for the inbound mailbox.

    Requires following AWS permissions:
    - sns:GetTopicAttributes (required by get_topic_attributes, for checking if topic exists)
    - sns:CreateTopic (required by create_topic, for creating topic)
    - sns:SetTopicAttributes (required by set_topic_attributes, for applying access policy)
    """
    print(f"Using region: {region}")
    sns_client = boto3.client('sns', region_name=region)

    inboundMail = f"inboundMail_{domain.replace('.', '-')}"
    AWS_acc_id = boto3.client('sts').get_caller_identity().get('Account')
    inboundMailArn = f"arn:aws:sns:{region}:{AWS_acc_id}:{inboundMail}"

    print(f"Checking if topic {inboundMail} exists...")
    try:
        response = sns_client.get_topic_attributes(TopicArn=inboundMailArn)
        print(json.dumps(response, indent=4))
        print(f"... Existing topic {inboundMail} will be reused.")
    except sns_client.exceptions.NotFoundException as e:
        print(f"... Topic {inboundMail} does not exist. Creating ...")
        response = sns_client.create_topic(Name=inboundMail)
        print(f"... ... Create topic {inboundMail} completed with response:")
        print(json.dumps(response, indent=4))
    except sns_client.exceptions.ClientError as e:
        print(f"... Error checking topic {inboundMail}: {e}")
        raise Exception(f"Error checking topic {inboundMail}: {e}") from e

    inboundMail_AccessPolicy = os.path.join(os.path.dirname(__file__), 'inboundMail_AccessPolicy.json')
    print(f"... Loading access policy to be applied to topic {inboundMail}...")
    with open(inboundMail_AccessPolicy, 'r') as policy:
        policyDocumentTemplate = policy.read()
        policyDocument = policyDocumentTemplate % {
            'region': region,
            'domain': domain,
            'inboundMail': inboundMail,
            'AWS_acc_id': AWS_acc_id,
            'inboundMailArn': inboundMailArn
        }
    print(f"... ... Access policy loaded.")
    print(policyDocument)

    print(f"... Applying access policy to topic {inboundMail}...")
    response = sns_client.set_topic_attributes(
        TopicArn=inboundMailArn,
        AttributeName='Policy',
        AttributeValue=policyDocument
    )
    print(f"... ... Access policy applied to topic {inboundMail} with response:")

    print("... Inbound topic setup complete.")

    return inboundMail
