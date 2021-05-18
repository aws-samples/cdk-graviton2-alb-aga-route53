from aws_cdk import (
    aws_ec2 as ec2,
    core
)


class NetworkingStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, cidr, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC - 2 AZs, 4 subnets (2 public, 2 private with 2 NatGateways)
        self.vpc = ec2.Vpc(
            self, "BlogVPC",
            cidr=str(cidr),
            max_azs=2
        )

        core.CfnOutput(self, "Output",
                       value=self.vpc.vpc_id)
