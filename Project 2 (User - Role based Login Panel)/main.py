from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

local_server=True
with open('config.json','r') as c:
    params = json.load(c)["params"]


app = Flask(__name__)
app.secret_key = 'super-secret-key'


if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
     app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

class User_table(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(50), nullable=False)
    user_phone = db.Column(db.Integer, nullable=False)
    user_about= db.Column(db.String(120), nullable=False)
    user_pass =  db.Column(db.String(120), nullable=False)
    user_role =  db.Column(db.String(120), nullable=False)
    date =  db.Column(db.String(120), nullable=True)
    

@app.route("/")
@app.route("/home")
def home():
     
            
            users = User_table.query.filter_by().all()
            return render_template("index.html",params=params,users = users)
    
@app.route("/details",methods = ['GET','POST'])
def veri():
     if request.method == "POST":
        username = request.form.get('Username')
        userpass = request.form.get('Password')
        
        users1 = User_table.query.filter_by(user_name=username).first()
        
        if username==params['user_name'] and userpass == params['user_pass']:
            session['user'] = username
            return render_template("admin_details.html",params=params,users=params)
        elif username == "" or username == None:
             return redirect("/home")
        elif users1 == None:
             return render_template("index.html",params=params)
             
        elif username == users1.user_name and userpass == users1.user_pass:
             session['user'] = username
             return render_template("details.html",params=params,users=users1)
        
@app.route("/signup",methods = ['GET','POST'])
def signup():
     if (request.method == 'POST'):
          box_user_name = request.form.get('user_name')
          box_user_pass = request.form.get('user_pass')
          box_user_role = request.form.get('user_role')
          box_user_email = request.form.get('user_email')
          box_user_about = request.form.get('user_about')
          box_user_phone = request.form.get('user_phone')
          box_user_time = datetime.now()

          users2 = User_table(user_name = box_user_name, user_pass =box_user_pass, user_phone =box_user_phone, user_email = box_user_email, user_about = box_user_about, user_role=box_user_role, date=box_user_time)
          db.session.add(users2)
          db.session.commit()
          return redirect("/home")
     return render_template("signup.html",params=params)
     
@app.route("/dash" ,methods=['GET','POST'])
def dashboard():

    if "user" in session and session['user']==params['user_name']:
        posts = User_table.query.all()
        return render_template("dashboard.html",params=params,posts=posts)
    else:
         return render_template("error.html")
@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/home')
     
@app.route("/edit/<string:sno>", methods = ['GET','POST'])
def edit(sno):
    if "user" in session and session['user']==params['user_name']:
        if request.method == 'POST':
               box_user_name = request.form.get('user_name')
               box_user_email = request.form.get('user_email')
               box_user_pass = request.form.get('user_pass')
               box_user_role = request.form.get('user_role')
               box_user_phone = request.form.get('user_phone')
               box_user_about = request.form.get('user_about')
               date = datetime.now()
               
               post = User_table.query.filter_by(sno=sno).first()
               post.user_name = box_user_name
               post.user_email = box_user_email
               post.user_about = box_user_about
               post.user_pass = box_user_pass
               post.user_role = box_user_role
               post.user_phone = box_user_phone
               post.date=date
               
               db.session.commit()
               return redirect('/dash')
        post = User_table.query.filter_by(sno=sno).first()
        return render_template('edit.html',params=params,user=post,sno=sno)
    else:
         return render_template("error.html")
    
@app.route("/delete/<string:sno>", methods = ['GET','POST'])
def delete(sno):
    if "user" in session and session['user']==params['user_name']:
        post = User_table.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        return redirect('/dash')
    else:
         return render_template("error.html")

        
app.run(debug=True,host='0.0.0.0',port=3000)