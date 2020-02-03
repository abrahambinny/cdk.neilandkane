"""Class to create a HostedZone using AWS CDK HostedZone method

Author: Binny Abraham

"""

from aws_cdk import core, aws_route53
from cdk_common import CdkCommonStack

class HostedZoneStack(CdkCommonStack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.account_name = kwargs['env'].account
        self.region_name = kwargs['env'].region
        self.cfn_variables = CFN_VARIABLES
        self.common = self.cfn_variables['common']

        # GENERATE CLOUDFORMATION RESOURCES
        stack_key = self.generate_stack_key(id)
        resource_variables = self.cfn_variables['accounts'][self.account_name]['regions'][self.region_name]['stacks'][stack_key]['cfn_resource_variables']
        self.resources = self.generate_cfn_resources(stack_key, resource_variables)


    def create_hosted_zone(self, logical_id, stack_id, **kwargs):
        '''
        Create Hosted Zone using aws_cdk aws_route53.HostedZone method
        '''
        return aws_route53.HostedZone(
            self,
            logical_id,
            zone_name=self.get_value_from_parameters('DelegatedHostedZoneName', self.parameters, stack_id)
        )
    # GENERATE CLOUDFORMATION RESOURCES ENDS HERE


    # GENERATE CLOUDFORMATION OUTPUTS STARTS HERE
    def generate_cfn_outputs(self, **kwargs):
        '''
        Generate all Cloudformation outputs here
        '''
        self.create_cfn_output('HostedZoneId', self.resources['ihzone'].hosted_zone_id, **kwargs['HostedZoneId'])
        self.create_cfn_output('HostedZoneName', self.resources['ihzone'].zone_name, **kwargs['HostedZoneName'])
    # GENERATE CLOUDFORMATION OUTPUTS ENDS HERE
