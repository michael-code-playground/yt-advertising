#!/bin/bash

# Start EC2 instance
aws ec2 start-instances --instance-ids #instance_id

# Wait for the instance to be running
aws ec2 wait instance-running --instance-ids #instance_id

echo "Instance is running."

# Fetch public dns
public_dns=$(aws ec2 describe-instances --instance-ids #instance_id --query 'Reservations[0].Instances[0].PublicDnsName')

# Remove double quotes
clear_dns=$(sed -e 's/^"//' -e 's/"$//' <<<"$public_dns")

# Replaced DNS in the RDP file
sed -i "2s/.*/full address:s:$clear_dns/" #RDP_file

echo "RDP file updated successfully."