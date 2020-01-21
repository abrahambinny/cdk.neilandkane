"""Class to create a HostedZone using AWS CDK HostedZone method

Author: Binny Abraham

"""

from aws_cdk import core
from cdk_common import CdkCommonStack

class ReplicaBucketStack(CdkCommonStack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Generating cloudformation components in 3 steps below

        # GENERATE CLOUDFORMATION PARAMETERS
        cfn_params = kwargs['env']['common']['cfn_parameters']
        cfn_params.update(kwargs['env']['replicabucket']['cfn_parameters'])
        self.parameters = self.generate_cfn_parameters(cfn_params)

        # GENERATE CLOUDFORMATION TAGS
        cfn_tags = kwargs['env']['common']['cfn_tags']
        cfn_tags.update(kwargs['env']['replicabucket']['cfn_tags'])
        self.generate_cfn_tags(cfn_tags)

        # GENERATE CLOUDFORMATION RESOURCES
        self.resources = {}
        self.resources['bucket'] = self.generate_cfn_resources(kwargs['env']['replicabucket']['logical_id'], id, **kwargs['env']['replicabucket']['cfn_resource_variables'])

        # GENERATE CLOUDFORMATION OUTPUTS
        if 'cfn_output_variables' in kwargs['env']['replicabucket']:
            self.generate_cfn_outputs(**kwargs['env']['replicabucket']['cfn_output_variables'])


    # GENERATE CLOUDFORMATION RESOURCES STARTS HERE
    def generate_cfn_resources(self, logical_id, stack_id, **kwargs):
        '''
        Generate all Cloudformation resources here
        '''
        bucket_name = self.get_value_from_parameters('BucketName', self.parameters, stack_id)
        return self.create_bucket(logical_id, bucket_name, **kwargs)
    # GENERATE CLOUDFORMATION RESOURCES ENDS HERE


    # GENERATE CLOUDFORMATION OUTPUTS STARTS HERE
    def generate_cfn_outputs(self, **kwargs):
        '''
        Generate all Cloudformation outputs here
        '''
        self.create_cfn_output('BucketReplicaName', self.resources['bucket'].bucket_name, **kwargs['BucketReplicaName'])
        self.create_cfn_output('BucketReplicaArn', self.resources['bucket'].bucket_arn, **kwargs['BucketReplicaArn'])
     # GENERATE CLOUDFORMATION OUTPUTS ENDS HERE
