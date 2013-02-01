from flask import Flask, request, redirect, render_template
import twilio.twiml
from werkzeug.contrib.fixers import ProxyFix
import MySQLdb 
import MySQLdb.cursors
 
app = Flask(__name__)
app.config.from_object('config')

myDb = MySQLdb.connect(host=app.config['MYSQL_DATABASE_HOST'], user=app.config['MYSQL_DATABASE_USER'], passwd=app.config['MYSQL_DATABASE_PASSWORD'], db=app.config['MYSQL_DATABASE_DB'], cursorclass=MySQLdb.cursors.DictCursor)

@app.route("/", methods=['GET'])
def index():
    cursor = myDb.cursor()
    cursor.execute('select * from teams13')
    for team in cursor:
        print team
        print team['vote_id'], team['team_name'], team['votes']
    
    return render_template('index.html', teams=cursor)

@app.route("/vote", methods=['GET'])
def vote():
    cursor = myDb.cursor()

    #prevent from voting twice
    from_number = request.values.get('From', None)
    cursor.execute('select * from phone_numbers13 where phone_number=' + from_number)
    number = cursor.fetchone()
    if number:
        return "You already voted." #don't waste a text here

    #cast vote
    vote_id = request.values.get('Body', None)
    cursor.execute('select * from teams13 where vote_id=' + vote_id)
    team = cursor.fetchone()

    if team:
        message = "Your vote for " + team['team_name'] + " has been tallied!"
        cursor.execute( 'update teams13 set votes=' + str((team['votes']+1)) + ' where vote_id=' + str(team['vote_id']) )
        query = 'insert into phone_numbers13 values(' + "\'" + from_number + "\'" + ')' 
        print query
        cursor.execute(query)
    else:
        message = "Not a valid vote."
 
    resp = twilio.twiml.Response()
    resp.sms(message)

    return message


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == "__main__":
    app.run(debug=False)