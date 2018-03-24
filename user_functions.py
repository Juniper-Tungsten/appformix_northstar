import json
from pprint import pprint
import os
from jinja2 import Environment, FileSystemLoader
import rest_call
import datetime
import time

def get_node_info(hostname):
  network_info = rest_call.get_node()

  for i in network_info.json():
    #pprint(i['hostName'])
    if i['hostName'] == hostname:
      name = i['name']
      index_number = i['nodeIndex']
  return name, index_number

def generate_node_maitenance_json(index_number, name):
  THIS_DIR = os.path.dirname(os.path.abspath(__file__))

  j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)

  payload = j2_env.get_template('maintenance.j2').render(
        index_number=index_number,
        name=name
    )

  return(payload)  


def getTimeSeq(num):
    # tz = pytz.timezone('America/New_York')
    # a = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    a = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    b_start = time.mktime(time.strptime(a, '%Y-%m-%d %H:%M:%S')) + int(num) * 60
    dateA = str(time.strftime("%Y%m%d", time.localtime(b_start)))
    timeA = str(time.strftime("%H%M", time.localtime(b_start)))
    juniorTime = 'T'.join([dateA, timeA])
    endstr = "00"
    finalTime = ''.join([juniorTime, endstr])
    return finalTime


