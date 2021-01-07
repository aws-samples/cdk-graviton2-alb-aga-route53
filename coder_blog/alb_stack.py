from aws_cdk import (
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as elbv2_targets,
    core
)


class ALBStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, vpc, instance, domain_cert, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ALB Configuration
        self.alb = elbv2.ApplicationLoadBalancer(
            self, "ALB", vpc=vpc, internet_facing=False)
        self.alb_listener = self.alb.add_listener(
            "ALBListener",
            port=443,
            certificates=[domain_cert],
            open=True
        )

        self.alb_listener.add_targets(
            "CodeServerInstance",
            port=8080, targets=[elbv2_targets.InstanceTarget(instance=instance, port=8080)])

        self.alb.connections.allow_to(instance, ec2.Port.tcp(8080))

        self.alb.add_redirect(source_port=80, source_protocol=elbv2.Protocol.HTTP,
                              target_port=443, target_protocol=elbv2.Protocol.HTTPS)

        self.alb.connections.allow_from_any_ipv4(ec2.Port.tcp(80))

        core.CfnOutput(self, "Output",
                       value=self.alb.load_balancer_arn)
