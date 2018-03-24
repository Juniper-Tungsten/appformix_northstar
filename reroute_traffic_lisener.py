# We need to import request to access the details of the POST request
from flask import Flask, request
from flask_restful import abort
import commands
import json
import pprint
import requests
import os
import rest_call
import user_functions

g_rule_id = os.environ.get('APPFORMIX_CONFIG_EVENT_RULE_ID')
g_cpu_rule_id = os.environ.get('APPFORMIX_CPU_EVENT_RULE_ID')
g_device_id = os.environ.get('APPFORMIX_VIOLATION_DEVICE_ID')
g_slack_notifier_url = os.environ.get('APPFORMIX_CONFIG_SLACK_URL')
# g_slack_notifier_url NOT a required parameters. However messages to slack may not be received if uninitialized
if not g_rule_id or not g_device_id:
    raise Exception('Initialize APPFORMIX_CONFIG_EVENT_RULE_ID, APPFORMIX_CONFIG_DEVICE_ID')

def do_action():
    # Notification action on the device
    rest_call.move_traffic()
    print 'provision new path succesful. traffic detoured'
    # Notification action to slack
    command = "sh ./nd_slack_notification.sh {0}".format(g_slack_notifier_url)
    #print 'Executing :: {0}'.format(command)
    commands.getoutput(command)

# Initialize the Flask application
app = Flask(__name__)

@app.route('/', methods=['POST'])
def app_message_post():
    print "########################################start"
    global g_rule_id
    global g_device_id
    global g_cpu_rule_id
    message = "No action"
    if request.headers['Content-Type'] != 'application/json':
        abort(400, message="Expected Content-Type = application/json")
    try:
        data = request.json
        #print data
        #command = "sh ./nd_slack_notification.sh {0}".format(g_slack_notifier_url)
        #commands.getoutput(command)
        #print "###################debug"
        status = data['status']
        spec = data['spec']
        state = status['state']
        device_id = status['entityId']
        event_rule_id = spec['eventRuleId']
        print "state " + state + " device id " + device_id + "  event id " + event_rule_id 
        #print "g_cpu_rule_id  " + g_cpu_rule_id 
        if spec['eventRuleId'] == g_rule_id:
            state = status['state']
            device_id = status['entityId']
            if state == "active" and device_id == g_device_id:
                print 'DATA_ACTIVE :: ', pprint.pprint(data)
                do_action()
                print 'traffic detoured and Slack was notified'
            elif state == "inactive":
                #print 'DATA_INACTIVE :: ', pprint.pprint(data)
                print 'LSP path can be changed back'
        #return json.dumps({'result': 'OK'})
        if spec['eventRuleId'] == g_cpu_rule_id:
            print "received cpu event"
            state = status['state']
            device_id = status['entityId']
            print state
            print device_id
            if state == "active" and device_id == g_device_id:
                print 'CPU HIGH UTIL DETECTED PUT NODE UNDER MAINTENANCE::', pprint.pprint(data)
                rest_node_name, rest_index_number = user_functions.get_node_info(device_id)
                #print "rest_node_name, rest_index_number" +  rest_node_name +  rest_index_number
                rest_payload = user_functions.generate_node_maitenance_json(rest_index_number, rest_node_name)
                print rest_payload
                rest_call.create_node_maintenance(rest_payload)
                print 'put router into maintenance mode and Slack was notified'
            elif state == "inactive":
                #print 'DATA_INACTIVE :: ', pprint.pprint(data)
                print 'CPU util back to normal. you can complete the maintenance mode'
        return json.dumps({'result': 'OK'})
    except Exception as e:
        abort(400, message="Exception processing request: {0}".format(e))


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("10000")
    )
