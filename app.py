#!/usr/bin/env python3

from aws_cdk import core

from coder_blog.coder_blog_stack import CoderBlogStack


app = core.App()
ohio_env =core.Environment(region="us-east-2")
CoderBlogStack(app, "coder-blog", env=ohio_env)

app.synth()
