from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_mysqldb import MySQL
import hashlib
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('login_page/login.html')


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'abhi4089'

mysql = MySQL(app)

prototype = 0
waterfall = 0
rad = 0
iterative = 0
evolutionary = 0
spiral = 0


@app.route('/results')
def results():
    p=[('prototype',prototype),('waterfall',waterfall),('rad',rad),('iterative',iterative),('evolutionary',evolutionary),('spiral',spiral)]
    x=0
    ans=max(p)
    print(ans[0])
    for i in p:
        print(i)
    return render_template('results/output.html', res=ans[0])


@app.route('/login', methods=['POST', 'GET'])
def do_admin_login():
    requests = request.form
    usern = requests['username']
    password = requests['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM  sdlcwebapp")
    for row in cur.fetchall():
        if usern == row[0] and hashlib.md5(password.encode()).hexdigest()== row[1]:
            session['logged_in'] = True
            return render_template('index.html', user=requests)
    return home()


@app.route('/register', methods=['POST', 'GET'])
def register():
    requests = request.form
    if request.method == "POST":
        details = request.form
        username = details['username']
        password = details['password']
        password_hash = hashlib.md5(password.encode())
        email = details['email']
        contact = details['contact']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sdlcwebapp(username, password, email, contact) VALUES (%s, %s,%s,%s)", (username, password_hash.hexdigest(), email, contact))
        mysql.connection.commit()
        cur.close()
        return render_template('index.html')
    return render_template('register_page/register.html')


@app.route('/selection', methods=['POST'])
def selection():
    global prototype
    global iterative
    global evolutionary
    global spiral
    global waterfall
    global rad
    requests=request.form
    val = requests['key']
    if val == '1':
        return render_template('selection/selection1.html')
    elif val == '2':
        if requests['question1']=='yes':
            waterfall+=1
            rad+=1
        else:
            prototype+=1
            iterative+=1
            evolutionary+=1
            spiral+=1
        if requests['question2']=='yes':
            prototype+=1
            spiral+=1
        else:
            waterfall+=1
            iterative+=1
            evolutionary+=1
            rad+=1
        if requests['question3']=='yes':
            waterfall+=1
            rad+=1
            iterative += 1
            evolutionary += 1
        else:
            prototype+=1
            spiral+=1
        if requests['question4']=='yes':
            prototype += 1
            iterative += 1
            evolutionary += 1
            spiral += 1
        else:
            waterfall +=1
            rad +=1
        return render_template('selection/selection2.html')
    elif val == '3':
        if requests['question1']=='yes':

            prototype+=1
            spiral+=1
        else:
            waterfall+=1
            iterative+=1
            evolutionary+=1
            rad+=1
        if requests['question2']=='yes':
            waterfall += 1
            iterative += 1
            evolutionary += 1
            spiral+=1
        else:
            prototype += 1
            rad+=1
        if requests['question3']=='yes':
            waterfall += 1
            spiral += 1
        else:
            iterative += 1
            evolutionary += 1
            prototype+=1
            rad+=1
        if requests['question4']=='yes':
            iterative += 1
            evolutionary += 1
            rad += 1
        else:
            waterfall += 1
            prototype += 1
            spiral += 1
        return render_template('selection/selection3.html')
    elif val == '4':
        if requests['question1']=='yes':
            prototype += 1
            rad+=1
        else:
            iterative += 1
            evolutionary += 1
            waterfall += 1
            spiral+=1
        if requests['question2']=='yes':
            waterfall += 1
            iterative += 1
            evolutionary += 1
            spiral+=1
        else:
            prototype += 1
            rad+=1
        if requests['question3']=='yes':
            prototype += 1
            spiral += 1
            iterative += 1
            evolutionary += 1
        else:
            waterfall += 1
            rad += 1
        if requests['question4']=='yes':
            prototype += 1
            iterative += 1
            evolutionary += 1
            rad += 1
        else:
            waterfall += 1
            spiral += 1
        return render_template('selection/selection4.html')
    else:
        if requests['question1']=='yes':
            iterative += 1
            evolutionary += 1
            rad+=1
        else:
            prototype += 1
            waterfall += 1
            spiral += 1
        if requests['question2']=='yes':
            prototype += 1
            waterfall += 1
            rad += 1
        else:
            iterative+=1
            evolutionary+=1
            spiral+=1
        if requests['question3']=='yes':
            spiral+= 1
            iterative += 1
            evolutionary += 1
        else:
            waterfall += 1
            prototype += 1
            rad += 1
        if requests['question4']=='yes':
            spiral += 1
            iterative += 1
            evolutionary += 1
            prototype += 1
            rad += 1
        else:
            waterfall += 1
    return results()


@app.route('/logout')
def logout():
    # session['logged_in'] = False
    return home()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
