#!/bin/bash
yum update -y
yum install jq -y
amazon-linux-extras install docker -y
systemctl enable docker
systemctl start docker
