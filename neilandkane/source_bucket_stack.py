"""Class to create a HostedZone using AWS CDK HostedZone method

Author: Binny Abraham

"""

from aws_cdk import core, aws_s3, aws_iam
from cdk_common import CdkCommonStack

class SourceBucketStack(CdkCommonStack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.dest_bucket_outputs = self.get_cfn_output_using_sdk('binnywww-dev-eu-west-1-BucketReplica', 'infonas-tau-dev', 'eu-west-1')
        self.replicarole_outputs = self.get_cfn_output_using_sdk('binnywww-dev-us-east-1-ReplicaRole', 'infonas-tau-dev', 'us-east-1')

        # Generating cloudformation components in 3 steps below
        cfn_params = {}
        cfn_params = kwargs['env']['common']['cfn_parameters']
        cfn_params.update(kwargs['env']['sourcebucket']['cfn_parameters'])
        cfn_params.update(self.generate_cfn_parameters_from_cfn_outputs(self.dest_bucket_outputs))
        cfn_params.update(self.generate_cfn_parameters_from_cfn_outputs(self.replicarole_outputs))
        self.parameters = self.generate_cfn_parameters(cfn_params)

        cfn_tags = kwargs['env']['common']['cfn_tags']
        cfn_tags.update(kwargs['env']['sourcebucket']['cfn_tags'])
        self.generate_cfn_tags(cfn_tags)

        self.source_bucket_name = self.get_value_from_parameters('SourceBucketName', self.parameters, id)
        self.dest_bucket_arn = self.get_value_from_parameters('BucketReplicaArn', self.parameters, id)

        self.resources = self.generate_cfn_resources(kwargs['env']['sourcebucket']['logical_id'], id, **kwargs['env']['sourcebucket']['cfn_resource_variables'])

        self.generate_cfn_outputs(**kwargs['env']['sourcebucket']['cfn_output_variables'])

    # Generate cloudformation resources starts here
    def generate_cfn_resources(self, logical_id, stack_id, **kwargs):
        '''
        Generate all Cloudformation resources here
        '''
        resource_dct = {}
        resource_dct['sourcebucket'] = self.create_cfn_bucket(logical_id, stack_id, **kwargs)
        return resource_dct

    def create_cfn_bucket(self, logical_id, stack_id, **kwargs):

        replication_configuration = {
            'role': self.get_value_from_parameters('ReplicaRoleArn', self.parameters, stack_id),
            'rules': [
                {
                    'destination':{
                        'bucket': self.dest_bucket_arn,
                        'storageclass': 'STANDARD'
                    },
                    'id': 'Backup',
                    'prefix': '',
                    'status': 'Enabled'
                }
            ]
        }

        versioning_configuration = {
            'status': 'Enabled'
        }

        s3_bucket = aws_s3.CfnBucket(
            self,
            logical_id,
            bucket_name=self.source_bucket_name,
            replication_configuration=replication_configuration,
            versioning_configuration=versioning_configuration,
        )
        s3_bucket.apply_removal_policy(policy=core.RemovalPolicy.DESTROY)
        return s3_bucket


    # Generate cloudformation outputs starts here
    def generate_cfn_outputs(self, **kwargs):
        '''
        Generate all Cloudformation outputs here
        '''
        self.create_cfn_output('SourceBucketNameOut', self.resources['sourcebucket'].bucket_name, **kwargs['SourceBucketName'])
        self.create_cfn_output('SourceBucketArnOut', self.resources['sourcebucket'].attr_arn, **kwargs['SourceBucketArn'])
