from flask import Flask,render_template,url_for,flash,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from forms import RegistrationForm,LoginForm,UpdateAccountForm,AddMeetForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user
import secrets,os
import smtplib

import pdfkit

from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 



from send_mail import send_mail
from attach_mail import attach_mail
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY']='7e4f75670462c4506dc181474b1e2bda'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    meetings = db.relationship('Meet', backref='author', lazy=True)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_required = db.Column(db.String,nullable=False)
    time = db.Column(db.String,nullable=False)
    content = db.Column(db.Text,nullable=False)
    meet_person_email = db.Column(db.String(100))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    

    def __repr__(self):
        return f"Post('{self.title}','{self.date_required}','{self.content}','{self.time}')"


class Meet(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_required = db.Column(db.String(10),nullable=False)
    time = db.Column(db.String(10),nullable=False)
    content = db.Column(db.Text,nullable=False)
    meet_person_email = db.Column(db.String(100))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Meet('{self.title}','{self.time}',{self.meet_person_email})"

    


    
    
    

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/meetings",methods=['GET', 'POST'])
def meetings():
    meets = Meet.query.filter_by(user_id=current_user.id).all()
    return render_template('meetings.html',meets=meets)

@app.route("/emailmeetings",methods=['GET','POST'])
def emailmeetings():
  rendered = render_template('meetings.html')
  pdf = pdfkit.from_string(rendered,False)
  response = make_response(pdf)
  response.headers['Content-type']='application/pdf'
  response.headers['Content-Disposition']='inline;filename=output.pdf'



# if __name__=="__main__":
#     app.run(debug=True)
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
      return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! plz login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
          login_user(user,remember=form.remember.data)
          next_page = request.args.get('next')
          flash('Welcome to EasyMeet', 'success')
          return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))

def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  _,f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
  

  output_size = (125,125)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(picture_path)

  return picture_fn


@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Account Updated','success')
    return redirect(url_for('account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email

  image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
  return render_template('account.html', title='Account',image_file=image_file,form=form)


@app.route("/addmeet",methods=['GET','POST'])
@login_required
def addmeet():
  form = AddMeetForm()
  if form.validate_on_submit():
      posts = Meet(title=form.title.data,date_required=form.date.data,time=form.time.data,content=form.content.data,meet_person_email=form.meet_person.data,author=current_user)
      db.session.add(posts)
      attach_mail(posts.meet_person_email,current_user.username,posts.date_required,posts.time)
      db.session.commit()
      flash('Your new meeting has been created!', 'success')

      return redirect(url_for('home'))

  return render_template('addmeet.html',title='Add Meet',form=form)

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    manager.run()