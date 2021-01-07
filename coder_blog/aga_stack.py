from aws_cdk import (
    aws_globalaccelerator as ga,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as elbv2_targets,
    core
)


class AgaStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, vpc, alb, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.accelerator = ga.Accelerator(self, "Accelerator")
        ga_listener = ga.Listener(
            self, "Listener",
            accelerator=self.accelerator,
            port_ranges=[ga.PortRange(
                from_port=443, to_port=443)]
        )
        endpoint_group = ga.EndpointGroup(
            self, "MainGroup", listener=ga_listener)
        endpoint_group.add_load_balancer("AlbEndpoint", alb)
        aga_sg = ga.AcceleratorSecurityGroup.from_vpc(
            self, "GlobalAcceleratorSG", vpc, endpoint_group)

        core.CfnOutput(self, "Output",
                       value=self.accelerator.accelerator_arn)
