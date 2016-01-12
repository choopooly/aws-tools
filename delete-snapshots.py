#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import boto.ec2

from boto.exception import EC2ResponseError
from datetime import datetime, timedelta

try:
    days = int(sys.argv[1])
except IndexError:
    days = 30

delete_time = datetime.utcnow() - timedelta(days=days)

filters = {
    'owner_id': '<INSERT_AWS_ID>'
}

print 'Deleting any snapshots older than {days} days'.format(days=days)

ec2 = boto.ec2.connect_to_region('us-west-2')
snapshots = ec2.get_all_snapshots(filters=filters)

deletion_counter = 0
size_counter = 0

for snapshot in snapshots:
    start_time = datetime.strptime(
        snapshot.start_time,
        '%Y-%m-%dT%H:%M:%S.000Z'
    )

    if start_time < delete_time:
        print 'Deleting {id}'.format(id=snapshot.id)
        deletion_counter = deletion_counter + 1
        size_counter = size_counter + snapshot.volume_size
        try:
            snapshot.delete()
        except EC2ResponseError as error:
            print ('Could not remove snapshot: {}'.format(
                error.reason))


print 'Deleted {number} snapshots totalling {size} GB'.format(
    number=deletion_counter,
    size=size_counter
)
