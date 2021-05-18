from aws_cdk import (
    aws_certificatemanager as acm,
    aws_route53 as route53,
    core
)


class CertsStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, domain, subdomain, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lookup the existing public hosted zone
        self.blog_hosted_zone = route53.HostedZone.from_lookup(
            self, "Domain", domain_name=domain)

        # Request and DNS Validate a certificate for the new subdomain
        self.domain_cert = acm.Certificate(
            self, "DomainCert",
            domain_name=f"{subdomain}.{domain}",
            validation=acm.CertificateValidation.from_dns(self.blog_hosted_zone))
