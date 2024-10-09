# Amaterasu Particle
# Dwij Bavisi <dwij@dbavisi.net>

"""
Release 0, Hotfix Pack 0, Hotfix 1

This module serves as the entry point for setting up the infrastructure for the project.
"""

import os
import dotenv
import boto3

from s3.mailbox import create_mailbox
from ses.identities import configure_identities
from sns.inboundMail import create_inboundMail

if __name__ == '__main__':
    dotenv.load_dotenv()

    access_key = os.getenv('AWS_access_key')
    secret_access_key = os.getenv('AWS_secret_access_key')
    boto3.setup_default_session(aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

    region = os.getenv('AWS_region', 'us-east-1')
    environment = os.getenv('AWS_environment', 'delta')
    rootDomain = os.getenv('AWS_rootDomain', 'dbavisi.net')

    mailbox = create_mailbox(region, environment, rootDomain)
    domain = configure_identities(region, environment, rootDomain)

    inboundMail = create_inboundMail(region, domain)
