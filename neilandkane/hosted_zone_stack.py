"""Class to create a HostedZone using AWS CDK HostedZone method

Author: Binny Abraham

"""

from aws_cdk import core, aws_route53
from cdk_common import CdkCommonStack
from cdk_config import CFN_VARIABLES

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


    def create_hosted_zone(self, logical_id, resource_name, **kwargs):
        '''
        Create Hosted Zone using aws_cdk aws_route53.HostedZone method
        '''
        return aws_route53.HostedZone(
            self,
            logical_id,
            zone_name=kwargs['kwargs']['zone_name']
        )
    # GENERATE CLOUDFORMATION RESOURCES ENDS HERE
