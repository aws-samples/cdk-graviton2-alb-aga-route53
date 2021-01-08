from aws_cdk import (
    aws_globalaccelerator as ga,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as elbv2_targets,
    core
)


class AgaStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, vpc, alb, hosted_zone, subdomain, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the Accelerator and add two listeners on ports 80 and 443 for http/https respectivley
        # The ALB already has a redirect in place to redirect to https.
        self.accelerator = ga.Accelerator(self, "Accelerator")
        ga_listener = ga.Listener(
            self, "Listener",
            accelerator=self.accelerator,
            port_ranges=[
                ga.PortRange(
                    from_port=443, to_port=443),
                ga.PortRange(
                    from_port=80, to_port=80)]
        )
        endpoint_group = ga.EndpointGroup(
            self, "MainGroup", listener=ga_listener)
        endpoint_group.add_load_balancer("AlbEndpoint", alb)
        aga_sg = ga.AcceleratorSecurityGroup.from_vpc(
            self, "GlobalAcceleratorSG", vpc, endpoint_group)

        # Add in a CNAME Record to our new LB based on the subdomain we created before.
        route53.CnameRecord(self, "AGA Subdomain", domain_name=self.accelerator.dns_name,
                            zone=hosted_zone, record_name=f"{subdomain}.{hosted_zone.zone_name}")

        core.CfnOutput(self, "Output",
                       value=self.accelerator.accelerator_arn)
