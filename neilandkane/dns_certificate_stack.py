"""Class to create an ACM Certificate using AWS CDK DNS Validate method

Author: Binny Abraham

"""

from aws_cdk import core, aws_route53, aws_certificatemanager
from cdk_common import CdkCommonStack

class DnsCertificateStack(CdkCommonStack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Generating cloudformation components in 3 steps below

        # GET CLOUDFORMATION OUTPUTS FROM ANOTHER STACK USING CDK IMPORT
        # self.cfn_outputs = []
        # self.cfn_outputs.append(self.extract_cfn_output(kwargs['env']['hzone']['cfn_output_variables']['HostedZoneId']['export_name'], kwargs['env']['hzone']['cfn_output_variables']['HostedZoneId']['description']))
        # self.cfn_outputs.append(self.extract_cfn_output(kwargs['env']['hzone']['cfn_output_variables']['HostedZoneName']['export_name'], kwargs['env']['hzone']['cfn_output_variables']['HostedZoneName']['description']))


        # GENERATE CLOUDFORMATION PARAMETERS
        cfn_params = kwargs['env']['common']['cfn_parameters']
        cfn_params.update(kwargs['env']['acm']['cfn_parameters'])
        # cfn_params.update(self.generate_cfn_parameters_from_cfn_outputs(self.cfn_outputs))
        self.parameters = self.generate_cfn_parameters(cfn_params)

        # GENERATE CLOUDFORMATION TAGS
        cfn_tags = kwargs['env']['common']['cfn_tags']
        cfn_tags.update(kwargs['env']['acm']['cfn_tags'])
        self.generate_cfn_tags(cfn_tags)

        # GENERATE CLOUDFORMATION RESOURCES
        self.hosted_zone_id = self.get_cfn_output_using_cdk(kwargs['env']['hzone']['cfn_output_variables']['HostedZoneId']['export_name'])
        self.hosted_zone_name = self.parameters["{}/HostedZoneName".format(id)]

        self.resources = {}
        self.resources['acm'] = self.generate_cfn_resources(kwargs['env']['acm']['logical_id'], **kwargs)

        # GENERATE CLOUDFORMATION OUTPUTS
        if 'cfn_output_variables' in kwargs['env']['acm']:
            self.generate_cfn_outputs(**kwargs['env']['acm']['cfn_output_variables'])


    # GENERATE CLOUDFORMATION RESOURCES STARTS HERE
    def generate_cfn_resources(self, logical_id, **kwargs):
        '''
        Generate all Cloudformation resources here
        '''
        return self.create_dns_validated_certificate(logical_id, **kwargs)

    def create_dns_validated_certificate(self, logical_id, **kwargs):
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
