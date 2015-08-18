# [START app]
from flask import Flask
import MySQLdb


env = os.getenv('SERVER_SOFTWARE')
if (env and env.startswith('Google App Engine/')):
  # Connecting from App Engine
  db = MySQLdb.connect(
    unix_socket='/cloudsql/resturanthealth:food',
    user='root')
else:
  # Connecting from an external network.
  # Make sure your network is whitelisted
  db = MySQLdb.connect(
    host='173.194.232.10',
    port=3306,
    user='root',passwd='12345')

@app.route('/test')
def test():
    """Return a friendly HTTP greeting."""
    return 'test'

@app.route('/dbui',methods=['GET'])
def dbui():
    cursor = db.cursor()
    data=list(cursor.execute('SELECT 1 + 1'))

    """Return a friendly HTTP greeting."""
    return str(data)

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

if __name__ == '__main__':
    app.run(host, port)
