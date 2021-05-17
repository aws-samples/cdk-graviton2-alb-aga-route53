
# EC2 Instance fronted by Internal ALB, AGA and Custom R53 Domain + Certificate

## Stack Components 

 * __./app.py__ - This is the main entry point to the stack. This file expects to find the following environment variables set prior to stack synthesis (see blog post for details) :
   * $CDK_DEFAULT_ACCOUNT - AWS Account No.
   * $CDK_DEFAULT_REGION - AWS Region
   * $VPC_CIDR - CIDR of the VPC to create
   * $R53_DOMAIN - Custom root domain (e.g. example.com)
 * __coder_blog/networking_stack.py__ – Defines a VPC across two Availability Zones with the CIDR range of your choice. The routing and public/private subnet creation is done for us as part of the default configuration.
 * __coder_blog/certs_stack.py__ – This stack creates a certificate for the subdomain you specify as part of the stack creation and DNS validation in Route 53.
 * __coder_blog/ec2_stack.py__ – This defines both our AMI and the instance type and configuration. In this case, we’re using Amazon Linux 2 ARM64 edition. Here we also set the instance-managed roles that allow Session Manager connectivity and Secrets Manager access.
 * __coder_blog/alb_stack.py__ – Here we define the internal load balancer and specify the listener, certificate, and target configuration.
 * __coder_blog/aga_stack.py__ – The accelerator is defined here with two ports open, the ALB we defined in the ALB stack as a target, and most importantly adds in a CNAME DNS entry pointing to the DNS name of the accelerator.

## Stack Instructions 

Please see AWS Blog Post: `Building an ARM64 Rust development environment using AWS Graviton2 and AWS CDK`