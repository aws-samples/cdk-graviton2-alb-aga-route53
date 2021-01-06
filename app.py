#!/usr/bin/env python3

from aws_cdk import core

from coder_blog.coder_blog_stack import CoderBlogStack


app = core.App()
CoderBlogStack(app, "coder-blog")

app.synth()
