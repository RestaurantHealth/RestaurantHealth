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
    db = MySQLdb.connect(unix_socket='/cloudsql/resturanthealth:food', user='root')
else:
    # Connecting from an external network.
    # Make sure your network is whitelisted
    db = MySQLdb.connect(host='173.194.232.10', port=3306, user='app_client', passwd='12345', db='INSPECTIONS')


app = Flask(__name__, static_path='')

loc_dict = {}


def qdb(sql):
    titles=["Name", "Program_Identifier", "Inspection_Date", "Description", "Address", "City", "Zip_Code", "Phone", "Longitude", "Latitude", "Inspection_Business_Name", "Inspection_Type", "Inspection_Score", "Inspection_Result", "Inspection_Closed_Business", "Violation_Type", "Violation_Description", "Violation_Points", "Business_ID", "Inspection_Serial_Num", "Violation_Record_ID"]
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


def org_qdb(data):
    id = 0
    json_data = {}
    for i in data:
        json_data[id] = i
        id+=1
    return json.dumps(json_data, sort_keys=False, indent=4, separators=(',', ': '))


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


@app.route('/getNear', methods=['GET'])
def getNear():
    if request.method=='GET':
        lat=47.6440788597
        lon=-122.2014702181
        # lat=request.form['lat']
        # lon=request.form['lon']
        titles=["Business_ID", "Name","Longitude", "Latitude", "Address", "City", "Inspection_Score"]
        sql='SELECT BUSINESS_ID,  NAME, LAT, LONGITUDE, ADDRESS, CITY, INSPECTION_SCORE, ( 3959 * acos( cos( radians(%s) ) * cos( radians( LAT ) ) * cos( radians( LONGITUDE ) - radians(%s) ) + sin( radians(%s) ) * sin( radians( LAT ) ) ) ) AS distance FROM INSPECTIONS GROUP BY BUSINESS_ID HAVING distance < 25 ORDER BY distance LIMIT 0 , 20;' % (lat,lon,lat)
        cur = db.cursor()
        cur.execute(sql)
        data=[]
        seen=[]
        for row in cur:
            if row[1] not in seen:
                seen.append(row[1])
                data.append(dict(zip(titles,row)))
        # data=list(cursor)
        # print data
        # cur=qdb(sql)
        # print cur
        return render_template('index.html', json_string=data)
    return ''


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

@app.route('/location', methods = ['POST'])
def location():
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    global loc_dict
    loc_dict={'latitude': latitude, 'longitude': longitude}
    return str(latitude) + ', ' + str(longitude)


def getBusiness_JSON(data):
    json_string = {}
    print(org_qdb(data))
    if len(data)>0:
        for i in data:
            json_string['Name'] = i.get('Name', {})
            json_string['Address'] = i.get('Address', {})
            json_string['City'] = i.get('City', {})
            json_string['Zip_Code'] = i.get('Zip_Code', {})
            json_string['Latitude'] = i.get('Latitude', {})
            json_string['Longitude'] = i.get('Longitude', {})
            json_string['Phone'] = i.get('Phone', {})
    print json_string
    return json_string


@app.route('/getBiz/<Business_ID>', methods=['GET', 'POST'])
def getBiz(Business_ID):
    print(Business_ID)
    if request.method=='POST' or Business_ID or request.method=='GET':
        data = qdb('select * from INSPECTIONS where BUSINESS_ID=\'%s\' ' % (str(Business_ID)))
        business_data = getBusiness_JSON(data)
    return render_template('ew-listing.html', json_string=data, business_data=business_data)
    # return str(data)


@app.route('/')
def hello():
    # jsonify results and send to template
    # getNear()
    # json_string = json.dumps(cursor.fetchall())
    data=qdb('select * from INSPECTIONS group by Name limit 5  ')
    return render_template('index.html', json_string=data)


# [START health]
@app.route('/_ah/health')
def health_check():
    return 'ok'
# [END health]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
# [END app]

