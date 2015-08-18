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
from flask import Flask, render_template, request
import MySQLdb
import os
import json


env = os.getenv('SERVER_SOFTWARE')
if (env and env.startswith('Google App Engine/')):
    # Connecting from App Engine
    db = MySQLdb.connect(unix_socket='/cloudsql/resturanthealth:food',user='root')
else:
    # Connecting from an external network.
    # Make sure your network is whitelisted
    db = MySQLdb.connect(host='173.194.232.10',port=3306,user='app_client',passwd='12345',db='INSPECTIONS')


app = Flask(__name__, static_path='')

def qdb(sql):
    titles=["Name", "Program Identifier", "Inspection Date", "Description", "Address", "City", "Zip Code", "Phone", "Longitude", "Latitude", "Inspection Business Name", "Inspection Type", 0, "Inspection Result", "Inspection Closed Business", "Violation Type", "Violation Description", 0, "Business_ID", "Inspection_Serial_Num", "Violation_Record_ID"]
    cursor = db.cursor()
    cursor.execute(sql)
    tmp=list(cursor)
    data=[]
    if len(tmp)>0:
        if 'Name' in tmp[0]:
            start=tmp[1:]
        else:
            start=tmp
        for row in start:
            data.append(dict(zip(titles, row)))
    return data


@app.route('/test')
def test():
    """Return a friendly HTTP greeting."""
    return 'test'


@app.route('/dbui',methods=['GET'])
def dbui():
    cursor = db.cursor()
    cursor.execute('select * from INSPECTIONS limit 10')
    data=[]
    for row in cursor:
        data.append(row)
    # data=db.use_result()
    # for row in data:
    #     print row

    # """Return a friendly HTTP greeting."""
    # return str(data)
    return str(data)


@app.route('/getBiz',methods=['GET'])
def getBiz():
    if request.method=='GET':
        # name=request.form['name']
        name='EURASIADELIHOUSE'
        # data=qdb('select * from INSPECTIONS limit 10' )
        # print data
        print 'select * from INSPECTIONS where Name=\'%s\' ' % (name)
        data=qdb('select * from INSPECTIONS where City=\'%s\' ' % ('Kent'))
        print 'getBiz',data
    return str(data)


@app.route('/getNear', methods=['POST'])
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


@app.route('/index')
@app.route('/')
def hello():
    # jsonify results and send to template
    # getNear()
    # json_string = json.dumps(cursor.fetchall())
    cur=qdb('select * from INSPECTIONS limit 3')
    print(cur)
    # data=json.dumps(cur, sort_keys=True, indent=4, separators=(',', ': '))
    # print data
    # json_string=data

    return render_template('index.html', json_string=cur)


# [START health]
@app.route('/_ah/health')
def health_check():
    return 'ok'
# [END health]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
# [END app]
