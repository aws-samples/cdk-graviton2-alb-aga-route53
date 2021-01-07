from aws_cdk import (
    aws_certificatemanager as acm,
    aws_route53 as route53,
    core
)


class CertsStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Certs Manager
        self.blog_hosted_zone = route53.HostedZone.from_hosted_zone_id(
            self, "AlMclean Domain", hosted_zone_id="Z09031023UJOL68N69L6")

        self.domain_cert = acm.Certificate(
            self, "DomainCert",
            domain_name="code-server.aws-mclean.com",
            validation=acm.CertificateValidation.from_dns(self.blog_hosted_zone))

        ## TODO
        # Add in an alias record once the AGA is completed 
        # Add injectable zoneID and domain name
