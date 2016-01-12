#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto
import boto.ec2

from boto.vpc import VPCConnection


class ListVPC:
    """
    List us-west-2 VPC environments
    """
    def __init__(self):
        self.region = 'us-west-2'
        self.vpc_env = self.list_env()

    def __str__(self):
        return self.vpc_env

    def vpc_api_call(self):
        """
        AWS VPC api call
        """
        region = boto.ec2.get_region(self.region)
        vpc_conn = VPCConnection(region=region)
        return vpc_conn

    def list_env(self):
        """
        Return VPC env tags
        """
        vpc_conn = self.vpc_api_call()
        # get VPC id
        vpc_env = []
        for vpc in vpc_conn.get_all_vpcs():
            print vpc.tags.get('Env')
            vpc_env.append(vpc.tags.get('Env'))

        return vpc_env
        # print vpc_env


if __name__ == "__main__":
    ListVPC()
