#!/usr/bin/env python3
"""AWS CDK app file to create stacks for the website

Author: Binny Abraham

"""

from aws_cdk import core
from binnydemohostnet.hosted_zone_stack import HostedZoneStack
from binnydemohostnet.dns_certificate_stack import DnsCertificateStack
from binnydemohostnet.replica_bucket_stack import ReplicaBucketStack
from binnydemohostnet.replica_role_stack import ReplicaRoleStack
from binnydemohostnet.source_bucket_stack import SourceBucketStack

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

# bucketReplicaStack = ReplicaBucketStack(
#     app,
#     CDK_ENVIRONMENT_VARIABLES['replicabucket']['stack_id'],
#     env=CDK_ENVIRONMENT_VARIABLES
# )


# # create replica role stack
# CDK_ENVIRONMENT_VARIABLES['region'] = 'us-east-1'
# ReplicaRoleStack = ReplicaRoleStack(
#     app,
#     CDK_ENVIRONMENT_VARIABLES['replicaiamrole']['stack_id'],
#     env=CDK_ENVIRONMENT_VARIABLES
# )


# # create bucket stack
# CDK_ENVIRONMENT_VARIABLES['region'] = 'us-east-1'

# bucketStack = SourceBucketStack(
#     app,
#     CDK_ENVIRONMENT_VARIABLES['sourcebucket']['stack_id'],
#     env=CDK_ENVIRONMENT_VARIABLES
# )


app.synth()
