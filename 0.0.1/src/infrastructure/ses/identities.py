# Amaterasu Particle
# Dwij Bavisi <dwij@dbavisi.net>

"""
Release 0, Hotfix Pack 0, Hotfix 1

This module performs the configuration for AWS Simple Email Service (SES) identities.
"""

import json
import boto3

def configure_identities(region: str, environment: str, rootDomain: str) -> str:
    """
    Configures Email and Domain identities to be used with AWS SES.

    :param region: AWS region (e.g. us-east-1).
    :param environment: Target deployment environment (e.g. delta, horizon, void).
    :param rootDomain: Root domain for the mailbox (e.g. dbavisi.net).

    :return domain: Domain identity for the mailbox.

    Requires following AWS permissions:
    - ses:GetIdentityVerificationAttributes (required by get_identity_verification_attributes, for checking if identity is registered)
    - ses:VerifyEmailIdentity (required by verify_email_identity, for verifying email identity)
    - ses:VerifyDomainIdentity (required by verify_domain_identity, for verifying domain identity)
    """
    print(f"Using region: {region}")
    ses_client = boto3.client('ses', region_name=region)

    print(f"Setting up email and domain identities for {rootDomain} in {environment} environment...")
    if environment == 'void':
        domain = rootDomain
    else:
        domain = f"{environment}.{rootDomain}"
    postman = f"postman@{domain}"

    print(f"... Checking if email address {postman} is registered...")
    try:
        response = ses_client.get_identity_verification_attributes(Identities=[postman])
        print(json.dumps(response, indent=4))
        if postman in response['VerificationAttributes']:
            print(f"... ... Email address {postman} is registered.")
        else:
            print(f"... Email address {postman} is not registered. Registering ...")
            response = ses_client.verify_email_identity(EmailAddress=postman)
            print(f"... ... Verify email identity for {postman} completed with response:")
            print(json.dumps(response, indent=4))
    except ses_client.exceptions.ClientError as e:
        print(f"... Error checking email address {postman}: {e}")
        raise Exception(f"Error checking email address {postman}: {e}") from e

    print(f"... Checking if domain {domain} is registered...")
    try:
        response = ses_client.get_identity_verification_attributes(Identities=[domain])
        print(json.dumps(response, indent=4))
        if domain in response['VerificationAttributes']:
            print(f"... ... Domain {domain} is registered.")
        else:
            print(f"... Domain {domain} is not registered. Registering ...")
            response = ses_client.verify_domain_identity(Domain=domain)
            print(f"... ... Verify domain identity for {domain} completed with response:")
            print(json.dumps(response, indent=4))
    except ses_client.exceptions.ClientError as e:
        print(f"... Error checking domain {domain}: {e}")
        raise Exception(f"Error checking domain {domain}: {e}") from e

    print(f"... Identity setup complete.")

    return domain
