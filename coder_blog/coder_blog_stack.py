from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_globalaccelerator as ga,
    aws_elasticloadbalancingv2 as elbv2,
    core
)


class CoderBlogStack(core.Stack):

    def availability_zones(self):
        return ['us-east-2b']

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC - 1 AZ, 2 Subnets
        vpc = ec2.Vpc(
            self, "BlogVPC",
            cidr="10.70.0.0/16",
            max_azs=1,
        )

        # AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            cpu_type=ec2.AmazonLinuxCpuType.ARM_64)

        # IAM Stuff
        role = iam.Role(self, "InstanceSSM",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(
            "service-role/AmazonEC2RoleforSSM"))
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite"))

        # Instance Type
        host = ec2.Instance(self, "Workstation",
                            instance_type=ec2.InstanceType("t4g.large"),
                            machine_image=amzn_linux,
                            block_devices=[ec2.BlockDevice(
                                device_name="/dev/xvda",
                                volume=ec2.BlockDeviceVolume.ebs(
                                    volume_size=128)
                            )],
                            vpc=vpc,
                            role=role
                            )

        host.connections.allow_internally

        print(f"Created new EC2 Instance {host.instance_id}")
        # Certs Manager
        # TODO

        # ALB Configuration
        alb = elbv2.ApplicationLoadBalancer(
            self, "ALB", vpc=vpc, internet_facing=False)
        alb_listener = alb.add_listener(
            port=443,
            open=true
        )

        alb_listener.add_targets("CodeServerInstance",
                                 port=5555, targets=[host])
        # TODO - add certificate

        # AGA Configuration

        accelerator = ga.Accelerator(self, "Accelerator")
        ga_listener = ga.Listener(self, "Listener",
                                  accelerator=accelerator,
                                  port_ranges=[ga.PortRange(
                                      from_port=443, to_port=443)]
                                  )
        endpoint_group = ga.EndpointGroup(
            self, "MainGroup", listener=ga_listener)
        endpoint_group.add_load_balancer("AlbEndpoint", alb)
        aga_sg = ga.AcceleratorSecurityGroup.from_vpc(
            self, "GlobalAcceleratorSG", vpc, endpoint_group)
        alb.connections.allow_from(aga_sg, ec2.Port.tcp(443))
