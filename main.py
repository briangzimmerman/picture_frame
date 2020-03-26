import yaml
import sys
import os
sys.path.append(os.path.dirname('.'))

from components.jobs.job_manager import JobManager
from components.utils.utils import create_object

config = yaml.load(open('./config.yaml'), Loader=yaml.UnsafeLoader)
jobs   = []

for job in config['jobs']:
    info = job['class_info']
    jobs.append(create_object(info['module'], info['class'], info['params']))

jobManager = JobManager(jobs)
jobManager.run()