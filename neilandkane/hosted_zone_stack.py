"""Class to create a HostedZone using AWS CDK HostedZone method

Author: Binny Abraham

"""

from aws_cdk import core, aws_route53
from cdk_common import CdkCommonStack

class HostedZoneStack(CdkCommonStack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Generating cloudformation components in 3 steps below

        # GENERATE CLOUDFORMATION PARAMETERS
        cfn_params = kwargs['env']['common']['cfn_parameters']
        cfn_params.update(kwargs['env']['hzone']['cfn_parameters'])
        self.parameters = self.generate_cfn_parameters(cfn_params)

        # GENERATE CLOUDFORMATION TAGS
        cfn_tags = kwargs['env']['common']['cfn_tags']
        cfn_tags.update(kwargs['env']['hzone']['cfn_tags'])
        self.generate_cfn_tags(cfn_tags)

        # GENERATE CLOUDFORMATION RESOURCES
        self.resources = {}
        self.resources['ihzone'] = self.generate_cfn_resources(id, **kwargs['env']['hzone']['cfn_resource_variables'])

        # GENERATE CLOUDFORMATION OUTPUTS
        self.generate_cfn_outputs(**kwargs['env']['hzone']['cfn_output_variables'])


    # GENERATE CLOUDFORMATION RESOURCES STARTS HERE
    def generate_cfn_resources(self, stack_id, **kwargs):
        '''
        Generate all Cloudformation resources here
        '''
        return self.create_hosted_zone('HostedZone', stack_id, **kwargs)

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
