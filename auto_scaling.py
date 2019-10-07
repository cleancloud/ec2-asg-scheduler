import os
import boto3

asgs = os.environ['AUTO_SCALING_GROUPS'].split(',')

client = boto3.client('autoscaling')

def suspend_launch(asg):
  client.suspend_processes(
    AutoScalingGroupName=asg['AutoScalingGroupName'],
    ScalingProcesses=['Launch']
  )

def resume_launch(asg):
  client.resume_processes(
    AutoScalingGroupName=asg['AutoScalingGroupName'],
    ScalingProcesses=['Launch']
  )

def get_ec2_instances_ids(asg):
  ids = []
  for instance in asg['Instances']:
    ids.append(instance['InstanceId'])
  return ids

def is_active(asg):
  active = True
  for process in asg['SuspendedProcesses']:
    if process['ProcessName'] == 'Launch':
      active = False
  return active

def get(asg_name):
  return client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])['AutoScalingGroups'][0]

def get_all():
  known_asgs = []
  for asg in asgs:
    known_asgs.append(get(asg))
  return known_asgs