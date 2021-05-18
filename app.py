#!/usr/bin/env python3

from aws_cdk import core
import os

from ec2_ialb_aga_custom_r53.network_stack import NetworkingStack
from ec2_ialb_aga_custom_r53.aga_stack import AgaStack
from ec2_ialb_aga_custom_r53.alb_stack import ALBStack
from ec2_ialb_aga_custom_r53.certs_stack import CertsStack
from ec2_ialb_aga_custom_r53.ec2_stack import EC2Stack

deploy_env = core.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"])

# These need to be injected at synth/deployment time
CIDR = os.getenv("VPC_CIDR", "")
DOMAIN = os.getenv("R53_DOMAIN", "")
SUB_DOMAIN = "code-server"

app = core.App()

net = NetworkingStack(app, "CoderBlog-NetworkingStack", CIDR, env=deploy_env)

ec2 = EC2Stack(app, "CoderBlog-EC2Stack", net.vpc, env=deploy_env)
ec2.add_dependency(net)

cert = CertsStack(app, "CoderBlog-CertsStack",
                  DOMAIN, SUB_DOMAIN, env=deploy_env)

alb = ALBStack(app, "CoderBlog-ALBStack", net.vpc, ec2.instance,
               cert.domain_cert, env=deploy_env)
alb.add_dependency(net)
alb.add_dependency(ec2)
alb.add_dependency(cert)

aga = AgaStack(app, "CoderBlog-AGAStack", net.vpc, alb.alb,
               cert.blog_hosted_zone, SUB_DOMAIN, env=deploy_env)
aga.add_dependency(net)
aga.add_dependency(cert)
aga.add_dependency(alb)

app.synth()
