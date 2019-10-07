# The MIT License (MIT)
#
# Copyright (c) 2019 CleanCloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import boto3
import auto_scaling

from pytz import timezone
from datetime import datetime
from validator import validate_vars

UTC = 'UTC'
TIMEZONE = os.environ['TIMEZONE']

def lambda_handler(event, context):
  validate_vars()

  asgs = auto_scaling.get_all()
  period = os.environ['PERIOD'].split('-')

  current = datetime.now(timezone(UTC)).astimezone(timezone(TIMEZONE)).time()
  start = datetime.strptime(period[0], '%H:%M').time()
  end = datetime.strptime(period[1], '%H:%M').time()

  for asg in asgs:
    if current < start or current > end:
      if auto_scaling.is_active(asg):
        pause(asg)
    if current >= start and current <= end:
      if not auto_scaling.is_active(asg):
        resume(asg)

def pause(asg):
  print('Suspending Launch process of the Auto Scaling Group \'{}\''.format(asg['AutoScalingGroupName']))
  auto_scaling.suspend_launch(asg)

  ids = auto_scaling.get_ec2_instances_ids(asg)
  print('Terminating EC2 instances IDs: {}'.format(ids))
  boto3.client('ec2').terminate_instances(InstanceIds=ids)

def resume(asg):
  print('Resuming Launch process of the Auto Scaling Group \'{}\''.format(asg['AutoScalingGroupName']))
  auto_scaling.resume_launch(asg)

if __name__ == "__main__":
    lambda_handler(None, None)
