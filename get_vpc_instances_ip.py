#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import boto
import boto.ec2
import argparse

from boto.vpc import VPCConnection


class GetVPCInstances:
    """
    Get VPC Instances
    """
    def __init__(self, env):
        self._env = env
        self.instances_dict = self.list_ip()

    def __str__(self):
        return self.instances_dict

    def api_call(self):
        """
        AWS api call
        """
        region = 'us-west-2'
        conn = boto.ec2.connect_to_region(region)
        return conn

    def get_vpc_id(self, env):
        """
        Return VPC ID from Stack Name
        """
        # VPC connection
        self.api_call()
        region = boto.ec2.get_region('us-west-2')
        vpc_conn = VPCConnection(region=region)

        # get dict of VPC
        vpc_dict = {}
        for vpc in vpc_conn.get_all_vpcs():
            vpc_dict[vpc.tags.get('Env')] = vpc.id

        # search Env in VPC tag name
        if env not in vpc_dict:
            print "VPC name not found."
            sys.exit(1)
        else:
            return vpc_dict[env]

    def list_ip(self):
        """
        List private IP from a VPC
        """
        conn = self.api_call()
        vpc_id = self.get_vpc_id(self._env)
        instances_dict = {}
        reservations = conn.get_all_instances()

        instances = [i for r in reservations for i in r.instances]
        for i in instances:
            if i.vpc_id == vpc_id:
                print i.tags.get('Name'), i.private_ip_address
                instances_dict[i.tags.get('Name')] = i.private_ip_address

        return instances_dict


def options():
    """
    options parser
    """
    parser = argparse.ArgumentParser(description="Get private IP")
    parser.add_argument('env', help='Stack Name')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    opts = options()
    GetVPCInstances(opts.env)
