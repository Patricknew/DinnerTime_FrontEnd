
#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import traceback
from credentials import UNI, password

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the postgresql test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/postgres
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# Swap out the URI below with the URI for the database created in part 2
DATABASEURI = "postgresql://"+UNI+":"+password+"@104.196.175.120:5432/postgres"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)

'''
try:
    conn = engine.connect()
    print "successful connection"
except:
    print "uh oh, problem connecting to database"

cursor = conn.execute("SELECT * FROM pokemon")
names = []
for result in cursor:
    names.append(result['pname'])
cursor.close()
print names
'''
#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
# 
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
# 
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
# 
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#
# engine.execute("""DROP TABLE IF EXISTS test;""")
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
#
# END SQLITE SETUP CODE
#



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


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
'''
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()
'''
  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  #return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
'''
@app.route('/another')
def another():
  return render_template("anotherfile.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  print name
  cmd = 'INSERT INTO test(name) VALUES (:name1), (:name2)';
  g.conn.execute(text(cmd), name1 = name, name2 = name);
  return redirect('/')
'''
@app.route('/')
def welcome():
	# DEBUG: this is debugging code to see what request looks like
  	return render_template('welcome.html')

@app.route('/query')
def query():
    return render_template('query.html')

@app.route('/insert')
def insert():
	return render_template('insert.html')

@app.route('/fancy')
def fancy():
    return render_template('fancy.html')
'''
@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()
'''
############insert############
@app.route('/addPokemon', methods=['POST'])
def addPokemon():
	try:
		PID = str(request.form['PID'])
		PName = str(request.form['PName'])
		PEvolutionLvl = str(request.form['PEvolutionLvl'])
		print PID, PName, PEvolutionLvl

		g.conn.execute("INSERT INTO Pokemon(PID, PName, PEvolutionLvl) VALUES (\'" + PID + "\',\'" + PName + "\',\'" + PEvolutionLvl + "\');")
		return render_template("insert.html", msg="Successful Insertion" )
	except Exception, e:
		print traceback.print_exc()
		return 'False'

@app.route('/addTrainer', methods=['POST'])
def addTrainer():
	try:
		TID = str(request.form['TID'])
		TName = str(request.form['TName'])
		TGender = str(request.form['TGender'])
		TRegion = str(request.form['TRegion'])
		print TID, TName, TGender, TRegion

		g.conn.execute("INSERT INTO Trainer(TID, TName, TGender, TRegion) VALUES (\'" + TID + "\',\'" + TName + "\',\'" + TGender + "\',\'" + TRegion + "\');")
		return render_template("insert.html", msg="Successful Insertion" )
	except Exception, e:
		# print traceback.print_exc()
		error = traceback.print_exc()
		print error
		return error

@app.route('/addBattle', methods=['POST'])
def addBattle():
	try:
		BID = str(request.form['BID'])
		BName = str(request.form['BName'])
		TyID = str(request.form['TyID'])
		print BID, BName, TyID

		g.conn.execute("INSERT INTO Battle_Belong(BID, BName, TyID) VALUES (\'" + BID + "\',\'" + BName + "\',\'" + TyID + "\');")
		return render_template("insert.html", msg="Successful Insertion" )
	except Exception, e:
		print traceback.print_exc()
		return 'False'

@app.route('/addItem', methods=['POST'])
def addItem():
	try:
		IID = str(request.form['IID'])
		IName = str(request.form['IName'])
		IType = str(request.form['IType'])
		ICost = str(request.form['ICost'])
		IEffect = str(request.form['IEffect'])
		print IID, IName, IType, ICost, IEffect

		g.conn.execute("INSERT INTO Item(IID, IName, IType, ICost, IEffect) VALUES (\'" + IID + "\',\'" + IName + "\',\'" + IType + "\',\'" + ICost + "\',\'" + IEffect + "\');")
		return render_template("insert.html", msg="Successful Insertion" )
	except Exception, e:
		print traceback.print_exc()
		return 'False'

@app.route('/addType', methods=['POST'])
def addType():
	try:
		TyID = str(request.form['TyID'])
		TyName = str(request.form['TyName'])
		TyWeakness = str(request.form['TyWeakness'])
		TyStrength = str(request.form['TyStrength'])
		print TyID, TyName, TyWeakness, TyStrength

		g.conn.execute("INSERT INTO Type(TyID, TyName, TyWeakness, TyStrength) VALUES (\'" + TyID + "\',\'" + TyName + "\',\'" + TyWeakness + "\',\'" + TyStrength + "\');")
		return render_template("insert.html", msg="Successful Insertion" )
	except Exception, e:
		print traceback.print_exc()
		return 'False'

@app.route('/addMove', methods=['POST'])
def addMove():
	try:
		MID = str(request.form['MID'])
		MName = str(request.form['MName'])
		MDps = str(request.form['MDps'])
		MPower = str(request.form['MPower'])
		MSecond = str(request.form['MSecond'])
		TyID = str(request.form['TyID'])
		print MID, MName, MDps, MPower, MSecond, TyID

		g.conn.execute("INSERT INTO Move_Classify(MID, MName, MDps, MPower, MSecond, TyID) VALUES (\'" + MID + "\',\'" + MName + "\',\'" + MDps + "\',\'" + MPower + "\',\'" + MSecond + "\',\'" + TyID + "\');")
		return render_template("insert.html", msg="Successful Insertion" )
	except Exception, e:
		print traceback.print_exc()
		return 'False'

@app.route('/addStats', methods=['POST'])
def addStats():
	try:
		PID = str(request.form['PID'])
		SHP = str(request.form['SHP'])
		SAttack = str(request.form['SAttack'])
		SDefense = str(request.form['SDefense'])
		SSpeed = str(request.form['SSpeed'])
		print PID, SHP, SAttack, SDefense, SSpeed

		g.conn.execute("INSERT INTO Posses_Stats(SID, SHP, SAttack, SDefense, SSpeed, PID) VALUES (\'" + PID + "\',\'" + SHP + "\',\'" + SAttack + "\',\'" + SDefense + "\',\'" + SSpeed + "\',\'" + PID + "\');")
		return render_template("insert.html", msg="Successful Insertion" )
	except Exception, e:
		print traceback.print_exc()
		return 'False'
############query############
@app.route('/recommendation', methods=['POST'])
def recommendation():
  try:
    opponentName = str(request.form['PName'])
    if len(opponentName) == 0:
      return render_template('fancy.html', msg="Please tell me which Pokemon you want to battle with!")

    queryID = "SELECT P.PID FROM Pokemon P WHERE P.PName=\'" + opponentName + "\'"
    queryResult = g.conn.execute(queryID)
    for row in queryResult:
      opponentID = row[0]

    queryType = "SELECT C.TyID FROM Categorize C WHERE C.PID=\'" + str(opponentID) + "\'"
    typeResult = g.conn.execute(queryType)
    opponentType = []
    for row in typeResult:
      opponentType.append(row[0])

    weakness = ''
    for TyID in opponentType:
      queryWeakness = "SELECT T.TyWeakness FROM Type T WHERE T.TyID=\'" + str(TyID) + "\'"
      weaknessResult = g.conn.execute(queryWeakness)
      for row in weaknessResult:
        weakness += row[0] + ", "
    weak = str(weakness).split(", ")
    weakset = list(set(weak[:-1]))

    weakID = []
    for w in weakset:
      queryTypeID = "SELECT T.TyID FROM Type T WHERE T.TyName=\'" + w + "\'"
      weaknessID = g.conn.execute(queryTypeID)
      for row in weaknessID:
        weakID.append(row[0])

    recommend = []
    for i in weakID:
      queryPokemon = "SELECT C.PID FROM Categorize C WHERE C.TyID=\'" + str(i) + "\'"
      pokemonResult = g.conn.execute(queryPokemon)
      for row in pokemonResult:
        recommend.append(row[0])
    recommendPoke = list(set(recommend))

    recommendPokeName = []
    for p in recommendPoke:
      queryPokeName = "SELECT P.PName FROM Pokemon P WHERE P.PID=\'" + str(p) + "\'"
      nameResult = g.conn.execute(queryPokeName)
      for row in nameResult:
        recommendPokeName.append(str(row[0]))
    print recommendPokeName

    message = ''
    for n in recommendPokeName:
      message += n + ", "
    return render_template('fancy.html', msg=message[:-2])
  except Exception, e:
    print traceback.print_exc()
    return 'Invalid Input'

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
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
