import json
from pprint import pprint
import os
from jinja2 import Environment, FileSystemLoader
import datetime
import time
import requests

node_url = 'http://10.10.2.54:8091/NorthStar/API/v1/tenant/1/topology/1/nodes'
lsp_url = 'http://10.10.2.54:8091/NorthStar/API/v2/tenant/1/topology/1/te-lsps'
maintenance_url = 'http://10.10.2.54:8091/NorthStar/API/v2/tenant/1/topology/1/maintenances'
headers = {'Authorization': 'Bearer Z28XMqGf4EPJvfDjGbAWRFp7LPXGJZzHO33mFbcJO6I=', 'Content-Type': 'application/json'}


def get_node_info(hostname):
    network_info = get_node()
    for i in network_info.json():
        if i['hostName'] == hostname:
            index_number = i['nodeIndex']
    return index_number


def move_traffic():
    contents = open('new_path.json', 'rb').read()
    print(contents)
    r = requests.post(lsp_url, data=contents, headers=headers, verify=False)
    # print(r)


def move_traffic2():
    contents = open('new_path.json', 'rb').read()
    print(contents)
    r = requests.put(lsp_url, data=contents, headers=headers, verify=False)
    # print(r)


def move_traffic_back():
    contents = open('original_path.json', 'rb').read()
    print(contents)
    r = requests.post(lsp_url, data=contents, headers=headers, verify=False)


def get_node():
    r = requests.get(node_url, headers=headers, verify=False)
    return (r)


def create_maintenance(payload):
    print(payload)
    r = requests.post(maintenance_url, data=payload, headers=headers, verify=False)
    return r


def generate_node_maitenance_json(index_number):
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)

    payload = j2_env.get_template('node_maintenance.j2').render(
        index_number=index_number,
        current_time=datetime.datetime.utcnow().strftime("%Y%m%d%H%M"),
        start_time=getTimeSeqUTC(1),
        end_time=getTimeSeqUTC(6000)
    )
    return (payload)


def generate_link_maitenance_json():
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)

    payload = j2_env.get_template('link_maintenance.j2').render(
        index_number=6,
        current_time=datetime.datetime.utcnow().strftime("%Y%m%d%H%M"),
        start_time=getTimeSeqUTC(1),
        end_time=getTimeSeqUTC(6000)
    )
    return payload


def getTimeSeqUTC(num):
    # tz = pytz.timezone('America/New_York')
    # a = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    a = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    b_start = time.mktime(time.strptime(a, '%Y-%m-%d %H:%M:%S')) + int(num) * 60
    dateA = str(time.strftime("%Y%m%d", time.localtime(b_start)))
    timeA = str(time.strftime("%H%M", time.localtime(b_start)))
    juniorTime = 'T'.join([dateA, timeA])
    endstr = "00"
    finalTime = ''.join([juniorTime, endstr])
    return finalTime + 'Z'
