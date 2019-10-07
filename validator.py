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
import sys
import boto3
import auto_scaling

from pytz import timezone
from datetime import datetime
from pytz import all_timezones

UTC = 'UTC'
PERIODS = os.environ['PERIOD']
TIMEZONE = os.environ['TIMEZONE']
WORK_DAYS = os.environ['WORK_DAYS']

asgs = os.environ['AUTO_SCALING_GROUPS'].split(',')

def validate_vars():
  validate_timezone()
  validate_periods()

def validate_work_days():
  current = datetime.now(timezone(UTC)).astimezone(timezone(TIMEZONE)).strftime('%a')
  if current.lower() not in WORK_DAYS.lower():
    sys.exit()

def validate_timezone():
  if TIMEZONE not in all_timezones:
    finish('Unknown timezone \'{}\''.format(TIMEZONE))

def validate_periods():
  if len(PERIODS.split('-')) == 1:
    finish('PERIOD variable should be in the format: 08:00-17:00')

  period = PERIODS.split('-')
  validate_period(period[0])
  validate_period(period[1])

def validate_period(period):
  if len(period.split(':')) == 1:
    finish('The value \'{}\' is in wrong format. Should be 00:00'.format(period))

def finish(msg):
  print(msg)
  print('Stopping execution')
  sys.exit(2)