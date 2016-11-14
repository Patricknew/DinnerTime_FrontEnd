
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
############search############
@app.route('/searchpokemon')
def searchpokemon():
    try:
        PID = str(request.args.get('PID'))
        PName = str(request.args.get('PName'))
        result=''
        if len(PID) == 0 and len(PName) == 0:
            return 'Please input PID or PName!'
        if len(PID) == 0:
            sexecute = "SELECT P.PID FROM Pokemon P WHERE P.PName=\'" + PName + "\'"
            profiles = g.conn.execute(sexecute)
            for profile in profiles:
                PID=str(profile)[1]
            if not PID:
                return 'PName not in table!'
        #profile
        sexecute = "SELECT P.PID, P.PName, P.Pevolutionlvl FROM Pokemon P WHERE P.PID=\'" + PID + "\'"
        profiles = g.conn.execute(sexecute)
        for s in profiles:
            if s[1]!=PName and len(PName)!= 0:
                return 'PID and PName do not match!'
            PName=s[1]
            st = 'Pokemon ['+PName+"] Profile: <br>PID: "+PID +' Pevolutionlvl: '+str(s[2])+'<br>'
            result +=st
        result+=" --------------------------------------------- <br>"

        #perform relationship
        sexecute = "SELECT P.PID,P.MID FROM Perform P WHERE P.PID=\'" + PID + "\'"
        owns = g.conn.execute(sexecute)
        result = result + "Move performed by Pokemon: <br>"
        for own in owns:
            st='MID: '+str(own[1])+"<br>"
            result = result + st
        result+=" --------------------------------------------- <br>"

        #categorize relationship
        sexecute = "SELECT P.PID,P.TyID FROM categorize P WHERE P.PID=\'" + PID + "\'"
        owns = g.conn.execute(sexecute)
        result = result + "Categorize as Type: <br>"
        for own in owns:
            st='Type ID = '+str(own[1])+"<br>"
            result = result + st
        result+=" --------------------------------------------- <br>"

        #posses relationship
        sexecute = "SELECT P.PID,P.sattack,P.sspeed, P.shp, P.sdefense FROM posses_stats P WHERE P.PID=\'" + PID + "\'"
        owns = g.conn.execute(sexecute)
        result = result + "Possed status: <br>"
        for own in owns:
            st='Attack = '+str(own[1])+' Speed = '+str(own[2])+"<br>"
            st+='HP = '+str(own[3])+' Defense = '+str(own[4])+"<br>"
            result = result + st
        return result

    except Exception:
        print traceback.print_exc()
        return 'Oops something goes wrong!'

@app.route('/searchtrainer')
def searchtrainer():
    try:
        TID = str(request.args.get('TID'))
        TName = str(request.args.get('TName'))
        if len(TID) == 0 and len(TName) == 0:
            return 'Please input PID or PName!'
        result=''
        if len(TID) == 0:
            sexecute = "SELECT T.TID FROM Trainer T WHERE T.TName=\'" + TName + "\'"
            profiles = g.conn.execute(sexecute)
            for profile in profiles:
                TID=str(profile)[1]
            if not TID:
                return 'TName not in table!'
        #profile
        sexecute = "SELECT T.TID, T.TName, T.Tgender, T.Tregion FROM Trainer T WHERE T.TID=\'" + TID + "\'"
        profiles = g.conn.execute(sexecute)
        for s in profiles:
            if s[1]!=TName and len(TName)!= 0:
                return 'TID and TName do not match!'
            TName=s[1]
            st = 'Trainer ['+TName+"] Profile: <br>TID: "+TID +' Tgender: '+s[2]+' Tregion: '+s[3]+"<br>"
            result += st
        result+=" --------------------------------------------- <br>"

        #own relationship
        sexecute = "SELECT O.PID,O.since,O.episode FROM Own O WHERE O.TID=\'" + TID + "\'"
        owns = g.conn.execute(sexecute)
        result = result + "Pokemon Ownership: <br>"
        for own in owns:
            st='PID: '+str(own[0])+' Since episode '+str(own[1])+" : "+own[2]+"<br>"
            result = result + st
        result+=" --------------------------------------------- <br>"

        #ISA
        sexecute = "SELECT O.TID,O.hleague FROM hero O WHERE O.TID=\'" + TID + "\'"
        hh = g.conn.execute(sexecute)
        v,h=[],[]
        for i in hh:
            h=i
        sexecute = "SELECT O.TID,O.vteam FROM villain O WHERE O.TID=\'" + TID + "\'"
        vv = g.conn.execute(sexecute)
        for i in vv:
            v=i
        result = result + "ISA: <br>"
        st=''
        if not h and not v:
            st='Neither a hero nor a villain. <br>'
        elif not v:
            st='Is a Hero.<br>Belong to league: '+h[1]+"<br>"
        elif not h:
            st='Is a Villain.<br>Belong to team: '+v[1]+"<br>"
        result = result + st
        result+=" --------------------------------------------- <br>"

        #participate relationship
        sexecute = "SELECT O.TID,O.BID FROM participate O WHERE O.TID=\'" + TID + "\'"
        owns = g.conn.execute(sexecute)
        result = result + "Participate in Battle: <br>"
        for own in owns:
            st='Battle ID = '+str(own[1])+"<br>"
            result = result + st
        result+=" --------------------------------------------- <br>"

        return result
    except Exception, e:
        print traceback.print_exc()
        return 'Oops something goes wrong!'

@app.route('/searchmove')
def searchmove():
    try:
        MID = str(request.args.get('MID'))
        MName = str(request.args.get('MName'))
        result=''
        if len(MID) == 0 and len(MName) == 0:
            return 'Please input MID or MName!'
        if len(MID) == 0:
            sexecute = "SELECT M.MID FROM move_classify M WHERE M.MName=\'" + MName + "\'"
            profiles = g.conn.execute(sexecute)
            for profile in profiles:
                MID=str(profile)[1]
            if not MID:
                return 'MName not in table!'
        #profile
        sexecute = "SELECT M.MID, M.MName, M.mdps, M.mpower, M.msecond, M.tyid FROM move_classify M WHERE M.MID=\'" + MID + "\'"
        profiles = g.conn.execute(sexecute)
        for s in profiles:
            if s[1]!=MName and len(MName)!= 0:
                return 'MID and MName do not match!'
            st = 'Move ['+s[1]+"] Profile: <br>MID: "+MID +'<br>'+'Damage per second: '+str(s[2])+'<br>'
            st+='Power: '+str(s[3])+' Second: '+str(s[4])+' Type: '+str(s[5])+'<br>'
            result +=st
        return result
    except Exception:
        print traceback.print_exc()
        return 'Oops something goes wrong!'

@app.route('/searchtype')
def searchtype():
    try:
        TyID = str(request.args.get('TyID'))
        TyName = str(request.args.get('TyName'))
        result=''
        if len(TyID) == 0 and len(TyName) == 0:
            return 'Please input Type ID or Name!'
        if len(TyID) == 0:
            sexecute = "SELECT T.TyID FROM type T WHERE T.TyName=\'" + TyName + "\'"
            profiles = g.conn.execute(sexecute)
            for profile in profiles:
                TyID=str(profile)[1]
            if not TyID:
                return 'Type Name not in table!'
        #profile
        sexecute = "SELECT T.TyID, T.TyName, T.tyweakness, T.tystrength  FROM Type T WHERE T.TyID=\'" + TyID + "\'"
        profiles = g.conn.execute(sexecute)
        for s in profiles:
            if s[1]!=TyName and len(TyName)!= 0:
                return 'Type ID and Name do not match!'
            st = 'Type ['+s[1]+"] Profile: <br>Type ID: "+TyID +'<br>'
            st+='Weakness: '+s[2]+'<br>'+'Strength: '+s[3]
            result +=st
        return result
    except Exception:
        print traceback.print_exc()
        return 'Oops something goes wrong!'

@app.route('/searchitem')
def searchitem():
    try:
        IID = str(request.args.get('IID'))
        IName = str(request.args.get('IName'))
        result=''
        if len(IID) == 0 and len(IName) == 0:
            return 'Please input Item ID or Name!'
        if len(IID) == 0:
            sexecute = "SELECT I.IID FROM item I WHERE I.IName=\'" + IName + "\'"
            profiles = g.conn.execute(sexecute)
            for profile in profiles:
                IID=str(profile)[1]
            if not IID:
                return 'Item Name not in table!'
        #profile
        sexecute = "SELECT I.IID, I.IName, I.itype, I.icost, I.ieffect  FROM item I WHERE I.IID=\'" + IID + "\'"
        profiles = g.conn.execute(sexecute)
        for s in profiles:
            if s[1]!=IName and len(IName)!= 0:
                return 'Item ID and Name do not match!'
            IName=s[1]
            st = 'Item ['+s[1]+"] Profile: <br>Item ID: "+IID +'<br>Type: '+s[2]+'<br>'
            st+='Cost: '+str(s[3])+'<br>'+'Effect: '+s[4]+'<br>'
            result +=st
        result+=" -------------------------------------------------------------------------------- <br>"

        ##Use relationship
        sexecute = "SELECT I.IID, I.TID, I.PID, I.qty FROM use I WHERE I.IID=\'" + IID + "\'"
        profiles = g.conn.execute(sexecute)
        result+='Item ['+IName+'] <br>'
        for s in profiles:
            st = 'Used '+str(s[3])+'times by Trainer with TID = '+str(s[1]) +' on Pokemon with PID = '+str(s[2])+'<br>'
            result +=st

        return result
    except Exception:
        print traceback.print_exc()
        return 'Oops something goes wrong!'

@app.route('/searchbattle')
def searchbattle():
    try:
        BName = str(request.args.get('BName'))
        result=''
        if len(BName) == 0:
            return 'Please input Battle Name!'
        #profile
        sexecute = "SELECT I.BName, I.BID, I.tyid FROM Battle_belong I WHERE I.BName=\'" + BName + "\'"
        profiles = g.conn.execute(sexecute)
        tmp=[]
        for s in profiles:
            tmp=s
            BID=s[1]
            result+='Battle ['+BName+"] Profile: <br>BID: "+str(BID) +'<br>Battle Type: '+str(s[2])+'<br>'
        if not tmp:
            result='Battle name not in table!'
        return result
    except Exception:
        print traceback.print_exc()
        return 'Oops something goes wrong!'

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
############Advanced############
@app.route('/update', methods=['POST'])
def update():
  try:
    TID = str(request.form['TID'])
    Field = str(request.form['Field'])
    New = str(request.form['New'])
    if len(TID) == 0:
      return render_template('fancy.html', msgU="You can find your ID in the search page.")
    if len(Field) == 0 or len(New) == 0:
      return render_template('fancy.html', msgU="Please tell me what you want to update!")
    
    updateQuery = "UPDATE Trainer SET " + Field + " = \'" + New + "\' WHERE TID = " + str(TID)
    updateResult = g.conn.execute(updateQuery)
    
    return render_template('fancy.html', msgU="Successful Update")
  except Exception, e:
    print traceback.print_exc()
    return 'Invalid Input'


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
