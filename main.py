# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
from flask import Flask


app = Flask(__name__)

@app.route('/test')
def test():
    """Return a friendly HTTP greeting."""
    return 'test'

@app.route('/getBiz',methods=['POST'])
def getBiz():
    if request.method=='POST':
        name=request.form['name']
        print 'getBiz',name
    return 'getBiz'

@app.route('/getNear',methods=['POST'])
def getNear():
    if request.method=='POST':
        name=request.form['name']
        print 'getNear',name
    return 'getNear'

@app.route('/getNearType',methods=['POST'])
def getNearType():
    if request.method=='POST':
        name=request.form['name']
        print 'getNearType',name
    return 'getNearType'

@app.route('/nameType',methods=['POST'])
def nameType():
    if request.method=='POST':
        name=request.form['name']
        print 'nameType',name
    return 'nameType'

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


# [START health]
@app.route('/_ah/health')
def health_check():
    return 'ok'
# [END health]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
# [END app]