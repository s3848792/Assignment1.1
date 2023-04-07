import datetime, json, boto3, requests
from s3_functions import show_image
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError
# Imports for website functionality

from flask import Flask, render_template, request, url_for, flash, redirect, session
#imports from flask

# Naming and setting of gloabl variables
# Explicit naming of secrets and keys is recognized as poor form
app = Flask(__name__)
app.config['SECRET_KEY'] = '3bUXIGVBPsfA3UsqbOk/E8LSazhUDAdxzWTB0c5k'
AWS_ACCESS="AKIAWG5XCPIOBQ765M43"
AWS_SECRET="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"
BUCKET_NAME='s3848792assignment1'
dynamodb=boto3.resource('dynamodb',region_name='ap-southeast-2', aws_access_key_id=AWS_ACCESS, aws_secret_access_key= AWS_SECRET)
s3 = boto3.client('s3')

MUSIC_SEARCH_URL='https://sqenqvobeb.execute-api.ap-southeast-2.amazonaws.com/test/music'
MUSIC_SUBSCRIBE_URL='https://sqenqvobeb.execute-api.ap-southeast-2.amazonaws.com/test/music'


# root method, rund on open url
#renders the home page
@app.route('/')
def root():
    return render_template('index.html')


# Method for rendering user page, and running HTTP methods for cloud interaction
# GET method retrievs user subscriptions, and renders them on their user page
# POST method is for unsubscribing from songs available on the user page
@app.route('/user', methods=('GET', 'POST'))
def user():
    if request.method==('POST'): #deletes subscription from DDBtable, then redirects to GET method for same page
        song = request.form['song']
        user = request.form['user']
        subscriptions = dynamodb.Table('Subscriptions')
        subscriptions.delete_item(Key={'User': user, 'Song': song})
        return redirect(url_for('user'))

    #GET method retrieves subscrriptions based on session user, then copies songs from Song table
    # then renders template with list of songs subscribed to
    if not session: #redirects away if user not logged in
        return redirect(url_for('login'))
    subscriptions = dynamodb.Table('Subscriptions')
    music = dynamodb.Table('Music')
    subResponse = subscriptions.query(KeyConditionExpression=Key('User').eq(session['username']))
    songList=[]
    musResponse=[]
    for item in subResponse['Items']:
        songList.append(item['Song'])
    if len(songList) > 0:
        musResponse = music.scan(
            FilterExpression=Attr('title').is_in(songList)
            )
        show_image(BUCKET_NAME, musResponse['Items'])#Helper function to get images for songs
        return render_template('user.html', music=musResponse['Items'])
    else:
        return render_template('user.html', music=[])
    


# Query/Search Page, GET method retrieves all songs not subscribed to, and narrows down if seaching using form
# Post method subscribes to a song, creates new entry in tables based on song and user
@app.route('/search', methods=('GET', 'POST'))
def search():

    if request.method==('POST'): #Uses lambda function, see searchPagePOSTlambda.py
        requests.post(MUSIC_SUBSCRIBE_URL, data = { 'user':request.form['user'], 'song': request.form['song']}, json={ 'user:':request.form['user'], 'song': request.form['user']})
        return redirect(url_for('user'))
    
    if request.method==('GET'):
        if not session: 
            return redirect(url_for('login'))
        #Uses lambda function, see searchPagePOSTlambda.py
        music = requests.get(MUSIC_SEARCH_URL, params = { 'title':request.args.get('title'), 'artist': request.args.get('artist'), 'year':request.args.get('year'), 'username': session['username']}).json()['body']
        if len(music) < 1: #if no results, inform user
            flash("No result is retrieved. You may already have subscribed to the song! Please query again.")
        show_image(BUCKET_NAME, music)
        return render_template('search.html', music=music)






# Login method, renders login page
# GET method simply renders page
# POST method checks if user exists in login table, if yes then create session and redirect to user page
# if not, then inform and run GET method

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        table = dynamodb.Table('login')
        response = table.scan(FilterExpression=Attr('username').eq(username) & Attr('password').eq(password) )
        data = response['Items']
        if len(data) == 0 or data[0]["username"] != username or data[0]["password"] != password:
            flash("Incorrect Username/Password!")
        else:
            session['username'] = username
            session['password'] = password
            session['email'] = data[0]["email"]
            return redirect(url_for('user'))
    
    if session: #redirects away if user already logged in
        return redirect(url_for('user'))
    return render_template('login.html')


#Register method, renders register page and creates new users
# GET renders page and register form
# POST method checks and validates new user, if OK then creates new entry in DDB and redirects to login
# If NO then informs user and runs GET method
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email=request.form['email']
        table = dynamodb.Table('login')
        if not username or not password or not email:
            flash("Fields are required!")
        response = table.scan(FilterExpression = Attr('email').eq(email))
        if len(response['Items']) > 0:
            flash("User email already taken!")
        else:
            table.put_item(Item={
            'lgn': '0',
            'num':str(datetime.datetime.now()),
            'username': username,
            'password': password,
            'email': email
        })
            return  redirect(url_for('root'))
        
    return render_template('register.html')

#logour page, clears session and redirects
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
