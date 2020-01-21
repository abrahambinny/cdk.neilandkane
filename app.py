#!/usr/bin/env python3
"""AWS CDK app file to create stacks for the website

Author: Binny Abraham

"""

from aws_cdk import core
from neilandkane.hosted_zone_stack import HostedZoneStack
from neilandkane.dns_certificate_stack import DnsCertificateStack
from neilandkane.replica_bucket_stack import ReplicaBucketStack

from cdk_config import CDK_ENVIRONMENT_VARIABLES, account, region

app = core.App()

# create hosted_zone stack
hostedZoneStack = HostedZoneStack(
    app,
    CDK_ENVIRONMENT_VARIABLES['hzone']['stack_id'],
    env=core.Environment(account=account, region=region),
    # **CDK_ENVIRONMENT_VARIABLES
)

# # create acm_certificate stack
# dnsCertificateStack = DnsCertificateStack(
#     app,
#     CDK_ENVIRONMENT_VARIABLES['acm']['stack_id'],
#     env=CDK_ENVIRONMENT_VARIABLES
# )


# # create replica bucket stack
# CDK_ENVIRONMENT_VARIABLES['region'] = 'eu-west-1'

# bucketReplicaStack = ContentBucketStack(
#     app,
#     CDK_ENVIRONMENT_VARIABLES['contentbucket']['stack_id'],
#     env=CDK_ENVIRONMENT_VARIABLES
# )


app.synth()
