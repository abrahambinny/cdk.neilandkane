#!/usr/bin/env python3
"""AWS CDK config file to store cfn static variables

Author: Binny Abraham

"""

import os
from aws_cdk import core

account = '369920941779'
account_alias = 'binnyabraham'
region = 'eu-west-1'
owner = "binnyabraham"
project_code = 'nkwww'
environment = 'dev'
root_domain = 'neilandkane.com'
delegated_hosted_zone_name = 'www.neilandkane.com'
content_bucket_name = 'neilandkane.com'

COMMON_VARIABLES = {
    'project_code': project_code,
    'environment': environment,
}

HOSTED_ZONE_VARIABLES = {
    'sequence': 1,
    'suffix': 'hosted-zone',
    'cfn_resource_variables':{
        'hosted_zone':{
            'suffix': 'hzone',
            'zone_name': root_domain,
            'outputs': {
                'zoneid': {
                    'id': 'HostedZoneId',
                    'description': 'HostedZoneIdOutput',
                    'field_name': 'hosted_zone_id',
                    'export_name': ''
                },
                'zonename': {
                    'id': 'HostedZoneName',
                    'description': 'HostedZoneNameOutput',
                    'field_name': 'zone_name',
                    'export_name': ''
                },
            },
        },
    },
}

DNS_CERTIFICATE_VARIABLES = {
    'sequence': 2,
    'suffix': 'dns-certificate',
    'cfn_resource_variables': {
        'dns_certificate':{
            'suffix': 'certificate',
            'zone_name': root_domain,
            'CDK_DEFAULT_ACCOUNT': account,
            'CDK_DEFAULT_REGION': region,
        },
    },
    'cfn_dependent_stacks': [
        {
            'suffix': 'hosted-zone',
            'account': account_alias,
            'region': 'eu-west-1'
        },
    ]
}

CONTENT_BUCKET_VARIABLES = {
    'sequence': 2,
    'suffix': 'content-bucket',
    'cfn_resource_variables':{
        'bucket':{
            'suffix': 'bucket',
            'versioned': True,
            'removal_policy': 'destroy',
            'outputs': {
                'bucketarn': {
                    'id': 'ContentBucketArn',
                    'description': 'Bucket Arn Output',
                    'field_name': 'bucket_arn',
                    'export_name': ''
                },
                'bucketname': {
                    'id': 'ContentBucketName',
                    'description': 'Bucket Name Output',
                    'field_name': 'bucket_name',
                    'export_name': ''
                },
            },
        },
    },
    'cfn_dependent_stacks': [
        {
            'suffix': 'hosted-zone',
            'account': account_alias,
            'region': 'eu-west-1'
        },
        {
            'suffix': 'dns-certificate',
            'account': account_alias,
            'region': 'eu-west-1'
        },
    ]
}


CFN_VARIABLES = {
    'common': COMMON_VARIABLES,
    'accounts': {
        account:{
            'common': {
                'alias': account_alias,
                'sequence': 1
            },
            'regions': {
                'eu-west-1': {
                    'common': {
                        'sequence': 1
                    },
                    'stacks': {
                        'zone': HOSTED_ZONE_VARIABLES,
                        'certificate': DNS_CERTIFICATE_VARIABLES,
                    },
                },
                'us-east-1': {
                    'common': {
                        'sequence': 1
                    },
                    'stacks': {
                        'certificate': DNS_CERTIFICATE_VARIABLES,
                    },
                },
            },
        },
    },
}
