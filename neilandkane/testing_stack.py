from aws_cdk import core, aws_route53, aws_certificatemanager


class BinnydemohostnetStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        if id == "BinnyHostedZone":
            self.generate_hosted_zone(id, **kwargs['env']['hosted_zone_variables'])

        if id == "BinnyCertificate":
            self.create_dns_validated_certificate(**kwargs['env']['certificate_manager_variables'])

    def generate_hosted_zone(self, id, **kwargs):

        hzone = self.create_hosted_zone(id, **kwargs)

        # Export value from the stack
        core.CfnOutput(
            self,
            "HostedZoneIdOutput",
            description="HostedZoneIdOutput",
            value=hzone.hosted_zone_id,
            export_name="HostedZoneIdOutput"
        )

        core.CfnOutput(
            self,
            "HostedZoneNameOutput",
            description="HostedZoneNameOutput",
            value=hzone.zone_name,
            export_name="HostedZoneNameOutput"
        )

    def create_hosted_zone(self, id, **kwargs):
        return aws_route53.HostedZone(self, id, **kwargs)

    def create_dns_validated_certificate(self, **kwargs):

        ihosted_zone = self.get_hosted_zone(kwargs['ihosted_zone_tag'], kwargs['hosted_zone_id'], kwargs['zone_name'])
        aws_certificatemanager.DnsValidatedCertificate(
            self,
            kwargs['certificate_tag'],
            hosted_zone = ihosted_zone,
            domain_name = kwargs['domain_name'],
            validation_method = aws_certificatemanager.ValidationMethod.DNS
        )

    def get_hosted_zone(self, ihosted_zone_tag, hosted_zone_id, zone_name):

        zone = aws_route53.HostedZone.from_hosted_zone_attributes(
            self,
            ihosted_zone_tag,
            hosted_zone_id = hosted_zone_id,
            zone_name = zone_name
        )
        return zone

    def create_certificate(self, **kwargs):

        cert = aws_certificatemanager.Certificate(
            self,
            kwargs['certificate_tag'],
            domain_name = args['domain_name'],
            validation_method =  aws_certificatemanager.ValidationMethod.DNS
        )

    def create_cname_record(self, env_variables):

        ihosted_zone = self.get_hosted_zone(env_variables)
        record_target = aws_route53.RecordTarget(values=env_variables['target'])

        cname_rec = aws_route53.RecordSet(
            self,
            env_variables['cname_tag'],
            record_type = aws_route53.RecordType.CNAME,
            target = record_target,
            zone = ihosted_zone,
            comment='cname_record',
            record_name= env_variables['record_name'],
        )

class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """

    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])
