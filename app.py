#!/usr/bin/env python3
"""AWS CDK app file to create stacks for the website

Author: Binny Abraham

"""

import sys, os
from aws_cdk import core
from aws_cdk.core import Environment
from neilandkane.hosted_zone_stack import HostedZoneStack
from neilandkane.dns_certificate_stack import DnsCertificateStack
from neilandkane.content_bucket_stack import ContentBucketStack

from cdk_config import CFN_VARIABLES, account, region

app = core.App()

def generate_cfn_stack_name(project_code, environment, region_name, stack_suffix):
    return '{}-{}-{}-{}'.format(project_code, environment, region_key, stack_suffix)

def generate_cdk_class_name(stack_suffix):
    return "{}Stack".format(stack_suffix.replace('-', ' ').title().replace(' ',''))

def generate_cdk_stack_name(cdk_class_name, cfn_stack_name, cdk_env):
    return ("{}({},'{}',env={})".format(cdk_class_name, 'app', cfn_stack_name, cdk_env))


# DYNAMIC GENERATION OF STACKS USING VARIABLE FROM CDK_CONFIG FILE
for account_key, account_value in CFN_VARIABLES['accounts'].items():

    for region_key, region_value in account_value['regions'].items():

        for stack_key, stack_value in region_value['stacks'].items():
            stack_suffix = stack_value['suffix']
            cfn_stack_name = generate_cfn_stack_name(
                CFN_VARIABLES['common']['project_code'],
                CFN_VARIABLES['common']['environment'],
                region_key,
                stack_suffix
            )
            cdk_class_name =  generate_cdk_class_name(stack_suffix)
            cdk_env = Environment(account=account_key, region=region_key)
            cdk_stack_name = generate_cdk_stack_name(cdk_class_name, cfn_stack_name, cdk_env)
            stack_obj = eval(cdk_stack_name)

app.synth()
