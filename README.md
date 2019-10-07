# EC2 Auto Scaling Group Scheduler
Lambda script to automatically turn on/off EC2 Auto Scaling Groups based on week days and working hours

## How it works?

This script basically terminate instances attached to ASGs and pause the ASG's Launch process, disabling it to launch new EC2 instances when you get out of the work hour/day and resume the ASG's Launch process when you get back into work hour/day.

## Configuration

### Variables

Before running, you need to set these variables:

- `AUTO_SCALING_GROUPS`: names of the Auto Scaling Groups to be scheduled separated by comma
- `TIMEZONE`: the timezone following the pattern `America/Sao_Paulo`
- `PERIOD`: the start and end times, in the format: `08:00-17:00`
- `WORK_DAYS`: the work days abbreviated separated by comma. Example: `mon,tue,wed,thu,fri`

If you want to test it before deploying to Lambda, you can run locally: `python3 main.py`

### IAM

Make sure the Lambda function have the right permissions to manage EC2 instances and Auto Scaling Groups:

    "Action": [
      "autoscaling:ResumeProcesses",
      "autoscaling:SuspendProcesses",
      "ec2:StopInstances"
    ]

### CloudWatch Events

Setup a CloudWatch Event to trigger the Lambda function periodically as your needed.

## Running

After configuration the function is ready to be deployed.  
The handler function is `main.lambda_handler`.

> **Important**: the script will only print logs when it make some change (on/off) to EC2 instances and ASGs and in case of a fail or misconfiguration. It will not log everytime it runs.