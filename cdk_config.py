#!/usr/bin/env python3
"""AWS CDK config file to store cfn static variables

Author: Binny Abraham

"""

import os
from aws_cdk import core

account = 'binnyabraham'
region = 'us-east-1'
owner = "binnyabraham"
project_code = 'nkwww'
environment = 'dev'
root_domain = 'neilandkane.com'
delegated_hosted_zone_name = 'www.neilandkane.com'
content_bucket_name = 'neilandkane.com'

COMMON_VARIABLES = {
    'project_code': project_code,
    'environment': environment,
    'cfn_parameters': {
        'ProjectCode': {
            'type': 'String',
            'default': project_code,
            'description' : 'Project Code'
        },
        'Environment': {
            'type': 'String',
            'default': environment,
            'description': 'Environment'
        },
    },
    'cfn_tags': {
        'ProjectCode': project_code,
        'Environment': environment,
        'Owner': owner
    }
}

HOSTED_ZONE_VARIABLES = {
    'stack_id': '{}-{}-{}-HostedZone'.format(project_code, environment, region),
    'logical_id': 'HostedZone',
    'cfn_parameters': {
        'DelegatedHostedZoneName': {
            'type': 'String',
            'default': delegated_hosted_zone_name,
            'description': 'Delegated Hosted Zone'
        },
    },
    'cfn_tags': {
        'Name': 'NeilAndKaneHostedZone'
    },
    'cfn_resource_variables':{
        'HostedZone':{
            'zone_name': delegated_hosted_zone_name
        },
    },
    'cfn_output_variables': {
        'HostedZoneId': {
            'export_name': 'HostedZoneId',
            'description': 'HostedZoneIdOutput'
        },
        'HostedZoneName': {
            'export_name': 'HostedZoneName',
            'description': 'HostedZoneName'
        },
    },
}

DNS_CERTIFICATE_VARIABLES = {
    'stack_id': '{}-{}-{}-DnsCertificate'.format(project_code, environment, region),
    'logical_id': 'DnsCertificate',
    'cfn_parameters': {
        'HostedZoneName': {
            'type': 'String',
            'default': delegated_hosted_zone_name,
            'description': 'Delegated Hosted Zone'
        },
        'RootDomain': {
            'type': 'String',
            'default': root_domain,
            'description': 'Root Domain'
        },
    },
    'cfn_tags': {
        'Name': 'NeilAndKaneCertificate'
    },
    'cfn_resource_variables': {
        'DnsCertificate':{
            'zone_name': delegated_hosted_zone_name,
            'CDK_DEFAULT_ACCOUNT': account,
            'CDK_DEFAULT_REGION': region,
        },
    },
}

CONTENT_BUCKET_VARIABLES = {
    'stack_id': '{}-{}-{}-BucketReplica'.format(project_code, environment, 'eu-west-1'),
    'logical_id': 'WebsiteContentBucket',
    'cfn_parameters': {
        'BucketName': {
            'type': 'String',
            'default': content_bucket_name,
            'description': 'Bucket Name'
        },
    },
    'cfn_tags': {
        'Name': 'NeilAndKaneContentBucket'
    },
    'cfn_resource_variables':{
        'versioned': True,
        'removal_policy':core.RemovalPolicy.DESTROY
    },
    'cfn_output_variables': {
        'BucketReplicaArn': {
            'export_name': 'ContentBucketArn',
            'description': 'Bucket Arn Output'
        },
        'BucketReplicaName': {
            'export_name': 'ContentBucketName',
            'description': 'Bucket Name Ouput'
        },
    }
}


CDK_ENVIRONMENT_VARIABLES = {
    # 'account': os.environ['CDK_DEFAULT_ACCOUNT'],
    # 'region': os.environ['CDK_DEFAULT_REGION'],
    'common': COMMON_VARIABLES,
    'hzone': HOSTED_ZONE_VARIABLES,
    'acm': DNS_CERTIFICATE_VARIABLES,
    'contentbucket': CONTENT_BUCKET_VARIABLES,
}
