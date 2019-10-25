# aws-acg-py-automate

Demo project to manage aws ec2 instances snapshot

## About

This project is a demo and uses boto3 
to manage aws ec2 instances snapshots.

## Configuring

paco uses the configuration file created by 
the AWS Cli. e.g.

`aws configure --profile paco`

## Running

`pipenv run python snapshotty/ec2-list.py <command> <subcommand> <--project=PROJECT>`

*command* are snapshot, instances, volumes 
*subcommand* depends on command
*project* is optional 
 



