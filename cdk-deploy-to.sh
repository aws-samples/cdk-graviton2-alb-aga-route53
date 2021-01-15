#!/usr/bin/env bash
if [[ $# -ge 4 ]]; then
    export CDK_DEPLOY_ACCOUNT=$1
    export CDK_DEPLOY_REGION=$2
    export R53_DOMAIN=$3
    export VPC_CIDR=$4
    shift; shift; shift; shift
    npx cdk bootstrap aws://$1/$2
    npx cdk deploy "$@"
    exit $?
else
    echo 1>&2 "Provide AWS account, region, root domain and VPC CIDR as first four args."
    echo 1>&2 "e.g. ./cdk-deploy-to.sh 1111111111 us-east-2 example.com 10.2.3.4/16"
    echo 1>&2 "Additional args are passed through to cdk deploy."
    exit 1
fi
