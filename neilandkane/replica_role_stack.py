"""Class to create a HostedZone using AWS CDK HostedZone method

Author: Binny Abraham

"""

from aws_cdk import core, aws_s3, aws_iam
from cdk_common import CdkCommonStack

class ReplicaRoleStack(CdkCommonStack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        self.dest_bucket_outputs = self.get_cfn_output_using_sdk('binnywww-dev-eu-west-1-BucketReplica', 'infonas-tau-dev', 'eu-west-1')

        # Generating cloudformation components in 3 steps below

        # GENERATE CLOUDFORMATION PARAMETERS
        cfn_params = {}
        cfn_params = kwargs['env']['common']['cfn_parameters']
        cfn_params.update(kwargs['env']['replicaiamrole']['cfn_parameters'])
        cfn_params.update(self.generate_cfn_parameters_from_cfn_outputs(self.dest_bucket_outputs))
        self.parameters = self.generate_cfn_parameters(cfn_params)

        # GENERATE CLOUDFORMATION TAGS
        cfn_tags = kwargs['env']['common']['cfn_tags']
        cfn_tags.update(kwargs['env']['replicaiamrole']['cfn_tags'])
        self.generate_cfn_tags(cfn_tags)

        # GENERATE CLOUDFORMATION RESOURCES
        self.source_bucket_name = self.get_value_from_parameters('SourceBucketName', self.parameters, id)
        self.source_bucket_arn = 'arn:aws:s3:::{}'.format(self.source_bucket_name)

        self.dest_bucket_name = self.get_value_from_parameters('BucketReplicaName', self.parameters, id)
        self.dest_bucket_arn = self.get_value_from_parameters('BucketReplicaArn', self.parameters, id)

        self.resources = self.generate_cfn_resources(kwargs['env']['replicabucket']['logical_id'], id, **kwargs['env']['replicaiamrole']['cfn_resource_variables'])

        # GENERATE CLOUDFORMATION OUTPUTS
        if 'cfn_output_variables' in kwargs['env']['replicaiamrole']:
            self.generate_cfn_outputs(**kwargs['env']['replicaiamrole']['cfn_output_variables'])


    # GENERATE CLOUDFORMATION RESOURCES STARTS HERE
    def generate_cfn_resources(self, logical_id, stack_id, **kwargs):
        '''
        Generate all Cloudformation resources here
        '''
        resource_dct = {}
        resource_dct['replicarole'] = self.create_role()
        resource_dct['replicapolicy'] = self.create_policy(stack_id, resource_dct['replicarole'], **kwargs)
        return resource_dct

    def create_role(self):

        return aws_iam.Role(
            self,
            'ReplicaRole',
            assumed_by = aws_iam.ServicePrincipal(service='s3.amazonaws.com')
        )

    def create_policy(self, stack_id, replica_role, **kwargs):

        statement_dct = [
            {
                'action': ['s3:Get*', 's3:ListBucket'],
                'effect': 'ALLOW',
                'resources': [
                    self.source_bucket_arn,
                    '{}/*'.format(self.source_bucket_arn)
                ]
            },
            {
                'action': ['s3:ReplicateObject', 's3:ReplicateDelete', 's3:ReplicateTags', 's3:GetObjectVersionTagging'],
                'effect': 'ALLOW',
                'resources': [
                    '{}/*'.format(self.dest_bucket_arn)
                ]
            }
        ]

        policy_statement_lst = self.create_policy_statement(statement_dct)

        policy = aws_iam.Policy(
            self,
            'ReplicaPolicy',
            policy_name='ReplicaPolicy',
            roles=[replica_role],
            statements=policy_statement_lst
        )
        return policy

    def create_policy_statement(self, statement_dct):

        policy_statement_lst = []
        for statement in statement_dct:

            policy_statement = aws_iam.PolicyStatement(
                actions=statement['action'],
                effect=aws_iam.Effect(statement['effect']),
                resources=statement['resources']
            )
            policy_statement_lst.append(policy_statement)
        return policy_statement_lst
    # GENERATE CLOUDFORMATION RESOURCES ENDS HERE


    # GENERATE CLOUDFORMATION OUTPUTS STARTS HERE
    def generate_cfn_outputs(self, **kwargs):
        '''
        Generate all Cloudformation outputs here
        '''
        self.create_cfn_output('ReplicaRoleArn', self.resources['replicarole'].role_arn, **kwargs['ReplicaRoleArn'])
        self.create_cfn_output('ReplicaPolicyName', self.resources['replicapolicy'].policy_name, **kwargs['ReplicaPolicyName'])
    # GENERATE CLOUDFORMATION OUTPUTS ENDS HERE
