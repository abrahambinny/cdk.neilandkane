"""Class to create an ACM Certificate using AWS CDK DNS Validate method

Author: Binny Abraham

"""

from aws_cdk import core, aws_route53, aws_certificatemanager
from cdk_common import CdkCommonStack
from cdk_config import CFN_VARIABLES

class DnsCertificateStack(CdkCommonStack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.account_name = kwargs['env'].account
        self.region_name = kwargs['env'].region
        self.cfn_variables = CFN_VARIABLES
        self.common = self.cfn_variables['common']

        stack_key = self.generate_stack_key(id)
        dependent_stacks = self.cfn_variables['accounts'][self.account_name]['regions'][self.region_name]['stacks'][stack_key]['cfn_dependent_stacks']

        # GET CFN OUTPUTS USING SDK
        self.cfn_outputs = self.generate_outputs_from_dependent_stacks(self.common['project_code'], self.common['environment'], dependent_stacks)

        # IMPORT EXPORT VALUES FROM CFN OUTPUT
        self.parameters = self.generate_cfn_parameters_from_cfn_outputs(self.cfn_outputs)
        self.hosted_zone_id =  self.parameters['HostedZoneId']['default']
        self.hosted_zone_name =  self.parameters['HostedZoneName']['default']

        # GENERATE CLOUDFORMATION RESOURCES

        resource_variables = self.cfn_variables['accounts'][self.account_name]['regions'][self.region_name]['stacks'][stack_key]['cfn_resource_variables']
        self.resources['acm'] = self.generate_cfn_resources(stack_key, resource_variables)

        # GENERATE CLOUDFORMATION OUTPUTS
        if 'cfn_output_variables' in kwargs['env']['acm']:
            self.generate_cfn_outputs(**kwargs['env']['acm']['cfn_output_variables'])


    # GENERATE CLOUDFORMATION RESOURCES STARTS HERE
    def generate_cfn_resources(self, logical_id, **kwargs):
        '''
        Generate all Cloudformation resources here
        '''
        return self.create_dns_validated_certificate(logical_id, **kwargs)

    def create_dns_certificate(self, logical_id, **kwargs):
        '''
        Create ACM certificate using aws_certificatemanager.DnsValidatedCertificate method
        '''
        ihosted_zone = self.get_hosted_zone('IHostedZoneId')

        return aws_certificatemanager.DnsValidatedCertificate(
            self,
            logical_id,
            hosted_zone = ihosted_zone,
            domain_name = self.hosted_zone_name,
            validation_method = aws_certificatemanager.ValidationMethod.DNS
        )

    def get_hosted_zone(self, ihosted_zone_tag):
        '''
        Get IhostedZone using from_hosted_zone_attributes method
        '''
        zone = aws_route53.HostedZone.from_hosted_zone_attributes(
            self,
            ihosted_zone_tag,
            hosted_zone_id = self.hosted_zone_id,
            zone_name = self.hosted_zone_name
        )
        return zone
    # GENERATE CLOUDFORMATION RESOURCES ENDS HERE
