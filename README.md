## Use Case
This repo is for Appformix related automation use case based on python script.
Currently it includes the following three use cases:
1. trigger Node Maintenance in Nortstar to reroute traffic bypassing the problematic node (e.g. node running at 100% CPU)
2. trigger Link Maintenance in Northstar to reroute traffic bypassing the problematic link (e.g. link with l3 incomplete error)
3. trigger junos configuration changing to set overload bit on the problematic node 



## Requirements

1. northstar application <br>
2. appformix <br>
3. network topology <br>



## Install

git clone https://github.com/Juniper/appformix_northstargy<br>



## Configure

according to your demo needs, you can modify the listener.py script to configured the corresponding event ID that is setup in appformix<br>

e.g.<br>
AppFormixInterfaceL3IncompleteEventID='606bbc82-2fae-11e8-b38d-0242ac120003'<br>
AppFormixCPUEventID='a8783e54-2349-11e8-b3ff-0242ac120005'<br>
AppFormixRuleOverloadBitID=''<br>


modify the ulrs in user_functions.py to the correct Northstar server's ip<br>
e.g.<br>
node_url = 'http://*:8091/NorthStar/API/v1/tenant/1/topology/1/nodes'<br>
lsp_url = 'http://*:8091/NorthStar/API/v2/tenant/1/topology/1/te-lsps'<br>
maintenance_url = 'http://*:8091/NorthStar/API/v2/tenant/1/topology/1/maintenances'<br>
