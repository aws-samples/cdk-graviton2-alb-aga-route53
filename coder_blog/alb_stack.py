from aws_cdk import (
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
        alb_listener = alb.add_listener(
            "ALBListener",
            port=443,
            certificates=[domain_cert],
            open=True
        )

        # Don't forget to add the ALB to the list of things the instance will talk to
        alb_listener.add_targets(
            "CodeServerInstance",
            port=8080, targets=[elbv2_targets.InstanceTarget(instance=host)])

        core.CfnOutput(self, "Output",
                       value=self.alb.id)
