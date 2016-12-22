
import os, json, io, StringIO
import requests
from flask import Flask, request, render_template, g, redirect, Response, url_for, send_from_directory, jsonify
import traceback
from werkzeug import secure_filename
from sqlalchemy import *
#ry:
#  import sys
#  reload(sys)
#  sys.setdefaultencoding('UTF-8')
#except:
#  pass
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
DBURI = 'postgresql://Patrick:hiddenpassword@cloudproject.cty82ugj6lwz.us-east-1.rds.amazonaws.com:5432/TripAdvisor'

engine = create_engine(DBURI)

try:
    conn = engine.connect()
    print "successful connection"
except:
  traceback.print_exc()
  conn = None
  print "uh oh, problem connecting to database"

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads/')
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def welcome():
  	return render_template('welcome.html')

@app.route('/basic')
def basic():
    return render_template('basic.html')

@app.route('/fancy')
def fancy():
    return render_template('fancy.html')

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    img = request.files['file']
    # img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    size = str(request.form['size'])
    [width, height] = size.split(',')

    #print type(file)
    # Check if the file is one of the allowed types/extensions
    
    if img and allowed_file(img.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(img.filename)
        data = img.read().encode('base64')

        body={"size": [int(height), int(width)],"image": data}
        print body
        url = "http://nn-flask-env.vm8fiwyr7p.us-east-1.elasticbeanstalk.com"
        response = requests.post(url, data = json.dumps(body, ensure_ascii=False))
        print response.text
        # r = json.loads(response.text)
        # print r['Casual Dining'],r['Casual Elegant'],r['Fine Dining']
        # m = 'Casual Dining' + str(r['Casual Dining']) + '\n' + 'Casual Elegant' + str(r['Casual Elegant']) + 'Fine Dining' + str(r['Fine Dining'])
        
        return render_template('basic.html', msg=response.text)
    else:
        return render_template('basic.html', msg="Please try again!")


############Advanced############
@app.route('/add', methods=['POST'])
def add():
  # try:
    img = request.files['file']
    # img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    imgData = img.read()
    reviews = str(request.form['reviews'])
    print img, reviews
    if len(reviews) == 0:
      return render_template('fancy.html', msgU="Please tell me what you think!")
    
    Query = "INSERT INTO userReviews (reviews) VALUES (\'" + reviews + "\');"
    print Query
    #Result = g.conn.execute(Query)
    
    return render_template('fancy.html', msgU="Successful Update")
  # except Exception, e:
    # print traceback.print_exc()
    # return 'Invalid Input'


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=True, threaded=threaded)


  run()
