from flask import Flask, render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, text
from sqlalchemy.sql import func

app = Flask(__name__)
app.secret_key = 'secret'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:0000@localhost:3306/blog"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

class User(db.Model):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(String(20, 'utf8mb4_unicode_ci'))
    password = Column(String(45, 'utf8mb4_unicode_ci'))
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    def __init__(self, userid, password):
        self.user_id = userid
        self.password = password

db.create_all()
@app.route('/')
def home():
    user_id=''
    if 'user_id' in session:
    	user_id = session['user_id']
    print("user_id: ",user_id)
    return render_template('home.html',user_id=user_id)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user_id = request.form["userId"]
    password =  request.form["password"]
    pre_user = User.query.filter_by(user_id=user_id).first()
    if pre_user:
        return render_template('register.html',message="이미가입됨")

    user = User(user_id,password)

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user) #Member instance도 동기화 시켜주기 위한 코드
    return render_template('register.html',message="가입완료")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    user_id = request.form["userId"]
    password =  request.form["password"]
    user = User.query.filter_by(user_id=user_id,password=password).first()
    if not user:
        return render_template('login.html',message="아이디 혹은 비밀번호를 확인해보세요.")

    session['user_id'] = user_id
    return redirect(url_for('home'))
    
@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))



@app.route("/one")
def one():
	member = User.query.first()
	return 'Hello {0}, {1}, {2}, {3}, {4}'\
		.format(member.name, member.email, member.phone, member.start.isoformat(), member.end.isoformat())
	#return render_template('home.html')
    
@app.route('/all')
def select_all():
    members = User.query.all()
    return "all"

