#!/usr/bin/env python3

from aws_cdk import core

from coder_blog.network_stack import NetworkingStack
from coder_blog.aga_stack import AgaStack
from coder_blog.alb_stack import ALBStack
from coder_blog.certs_stack import CertsStack
from coder_blog.ec2_stack import EC2Stack

app = core.App()

net = NetworkingStack(app, "NetworkingStack")
ec2 = EC2Stack(app, "EC2Stack", net.vpc)
ec2.add_dependency(net)

cert = CertsStack(app, "CertsStack")

alb = ALBStack(app, "ALBStack", net.vpc, ec2.instance, cert.domain_cert)
alb.add_dependency(net)
alb.add_dependency(ec2)
alb.add_dependency(cert)

aga = AgaStack(app, "AGAStack", alb.alb)
aga.add_dependency(alb)

app.synth()
