from aws_cdk import (
    aws_ec2 as ec2,
    core
)


class NetworkingStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC - 1 AZ, 2 Subnets
        self.vpc = ec2.Vpc(
            self, "BlogVPC",
            cidr="10.70.0.0/16",
            max_azs=2
        )

        core.CfnOutput(self, "Output",
                       value=self.vpc.vpc_id)

