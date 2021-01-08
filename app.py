#!/usr/bin/env python3

from aws_cdk import core
import os

from coder_blog.network_stack import NetworkingStack
from coder_blog.aga_stack import AgaStack
from coder_blog.alb_stack import ALBStack
from coder_blog.certs_stack import CertsStack
from coder_blog.ec2_stack import EC2Stack

deploy_env = core.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"])

# These need to be injected at synth/deployment time
CIDR = os.getenv("VPC_CIDR", "10.70.0.0/20")
DOMAIN = os.getenv("R53_DOMAIN", "aws-mclean.com")
SUB_DOMAIN = os.getenv("R53_SUBDOMAIN", "code-server")

app = core.App()

net = NetworkingStack(app, "NetworkingStack", CIDR, env=deploy_env)

ec2 = EC2Stack(app, "EC2Stack", net.vpc, env=deploy_env)
ec2.add_dependency(net)

cert = CertsStack(app, "CertsStack", DOMAIN, SUB_DOMAIN, env=deploy_env)

alb = ALBStack(app, "ALBStack", net.vpc, ec2.instance,
               cert.domain_cert, env=deploy_env)
alb.add_dependency(net)
alb.add_dependency(ec2)
alb.add_dependency(cert)

aga = AgaStack(app, "AGAStack", net.vpc, alb.alb,
               cert.blog_hosted_zone, SUB_DOMAIN, env=deploy_env)
aga.add_dependency(net)
aga.add_dependency(cert)
aga.add_dependency(alb)

app.synth()
