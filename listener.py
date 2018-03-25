# We need to import request to access the details of the POST request
from flask import Flask, request
from flask_restful import abort
import commands
import json
import pprint
import requests
import os
import user_functions


AppFormixInterfaceL3IncompleteEventID='606bbc82-2fae-11e8-b38d-0242ac120003'
AppFormixCPUEventID='a8783e54-2349-11e8-b3ff-0242ac120005'


# Initialize the Flask application
app = Flask(__name__)

@app.route('/', methods=['POST'])
def app_message_post():
    print "########################################start"
    global AppFormixInterfaceL3IncompleteEventID
    global AppFormixCPUEventID
    if request.headers['Content-Type'] != 'application/json':
        abort(400, message="Expected Content-Type = application/json")
    try:
        data = request.json
        status = data['status']
        spec = data['spec']
        state = status['state']
        device_id = status['entityId']
        event_rule_id = spec['eventRuleId']
        print "state " + state + " device id " + device_id + "  event id " + event_rule_id
        #if spec['eventRuleId'] == g_rule_id:
        #    state = status['state']
        #    device_id = status['entityId']
        #    if state == "active" and device_id == g_device_id:
        #        print 'DATA_ACTIVE :: ', pprint.pprint(data)
        #        user_functions.move_traffic()
        #        print 'traffic detoured and Slack was notified'
        #    elif state == "inactive":
        #        #print 'DATA_INACTIVE :: ', pprint.pprint(data)
        #        print 'LSP path can be changed back'
        #return json.dumps({'result': 'OK'})
        if event_rule_id == AppFormixCPUEventID:
            print "received cpu high alert"
            print state
            print device_id
            if state == "active":
                print 'CPU HIGH UTIL DETECTED PUT NODE UNDER MAINTENANCE::', pprint.pprint(data)
                rest_index_number = user_functions.get_node_info(device_id)
                #print "rest_node_name, rest_index_number" +  rest_node_name +  rest_index_number
                rest_payload = user_functions.generate_node_maitenance_json(rest_index_number)
                print rest_payload
                user_functions.create_maintenance(rest_payload)
                print 'put router into maintenance mode'
            elif state == "inactive":
                #print 'DATA_INACTIVE :: ', pprint.pprint(data)
                print 'CPU util back to normal. you can complete the maintenance event'
        if event_rule_id == AppFormixInterfaceL3IncompleteEventID:
            print "received interface l3 incomplete alert"
            if state == "active":
                rest_payload = user_functions.generate_link_maitenance_json()
                print rest_payload
                user_functions.create_maintenance(rest_payload)
                print 'put problematic link into maintenance mode'
            elif state == "inactive":
            # print 'DATA_INACTIVE :: ', pprint.pprint(data)
                print 'link back to normal. you can complete the maintenance event'
        return json.dumps({'result': 'OK'})
    except Exception as e:
        abort(400, message="Exception processing request: {0}".format(e))


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("10000")
    )
