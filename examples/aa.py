# Copyright 2011-2014 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Retrieves a list of installed apps from Splunk using the client module."""
import sys, os
from splunklib.binding import HTTPError

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import splunklib.client as client

HOST = "localhost"
PORT = 8089
USERNAME = "admin"
PASSWORD = "changed"
owner = USERNAME
app = "search"

service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD,
    owner=owner,
    app=app)

collection = "test"
urlConf = "storage/collections-conf"
urlCommon = "storage/collections"
urlConfItem = urlConf + "/" + collection
urlData = urlCommon + "/" + collection + "/data"
urlIndex = urlCommon + "/" + collection + "/indexes"

try:
    service.delete(urlConfItem)
except HTTPError, e:
    if e.status != 404:
        raise

service.post(urlConf, name = collection)
print service.get(urlConfItem).body.read()

import json

data = { '_id': "33", 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'es' : "5" }
service.post(urlData, body=json.dumps(data))
urlDataItem = urlData + "/33"
print service.get(urlDataItem).body.read()
service.delete(urlDataItem)

index = { 'name': 'index', 'key':{'a' : 1, 'b' : 1, 'c' : 1} }
service.post(urlIndex, body=json.dumps(index))
urlIndexItem = urlIndex + "/index"
print service.get(urlIndexItem).body.read()
service.delete(urlIndexItem)