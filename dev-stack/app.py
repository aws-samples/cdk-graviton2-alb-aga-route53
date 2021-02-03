#!/usr/bin/env python3

from aws_cdk import core

from dev_stack.dev_stack_stack import DevStackStack


app = core.App()

props = {
    "vpc-ref": "vpc-0b4bec20afcad3759",
}

DevStackStack(app, "dev-stack", props, env=core.Environment(account="432762038596", region="us-east-2"))

app.synth()
