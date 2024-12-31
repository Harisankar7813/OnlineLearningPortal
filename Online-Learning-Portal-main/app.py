from flask import Flask, render_template,session, redirect, url_for, flash, request,jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Email,EqualTo
import bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB'] ='mydatabase'
app.secret_key='your-secret-key-123456'
mysql = MySQL(app)


class RegistrationForm(FlaskForm):
    name = StringField("Username",validators=[DataRequired()],render_kw={"class": "input-container", "id": "name", "type": "text"})
    email = StringField("Email",validators=[DataRequired(),Email()],render_kw={"class": "input-container", "id": "email","type":"email"})
    password = PasswordField("Password",validators=[DataRequired()],render_kw={"class": "input-container", "id": "password","type":"password"})
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ],
        render_kw={"placeholder": "Re-enter your password"}
    )
    submit = SubmitField("signup",render_kw={"class": "button"})


class LoginForm(FlaskForm):
    name = StringField("Username",validators=[DataRequired()],render_kw={"class": "input-container", "id": "name", "type": "text"})
    password = PasswordField("Password",validators=[DataRequired()],render_kw={"class": "input-container", "id": "password","type":"password"})
    submit = SubmitField("Login",render_kw={"class": "button"})

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField
from wtforms.validators import DataRequired

class BookingForm(FlaskForm):
    course = SelectField('', choices=[('select course','Select Course'),('course1', 'Course 1'), ('course2', 'Course 2')], validators=[DataRequired()],render_kw={"class": "input-container", "id": "course"})
    trainee = SelectField('', choices=[('select trainee','Select Trainee'),('trainee1', 'Trainee 1'), ('trainee2', 'Trainee 2')], validators=[DataRequired()],render_kw={"class": "input-container", "id":"trainee"})
    date = DateField('', format='%Y-%m-%d', validators=[DataRequired()],render_kw={"class": "input-container", "id": "dob"})
    slot = SelectField('', choices=[('select slot timing','Select Slot Timing'),('slot1', 'Slot 1'), ('slot2', 'Slot 2')], validators=[DataRequired()],render_kw={"class": "input-container", "id": "slot"})
    submit = SubmitField("Save",render_kw={"class":"button"})


@app.route('/login',methods=['GET', 'POST'])
def login():
        form = LoginForm()
        if form.validate_on_submit():
            name = form.name.data
            password = form.password.data  

            cursor = mysql.connection.cursor()
            cursor.execute(
                        "SELECT * FROM users WHERE name=%s",(name,)
                 )
            user = cursor.fetchone()
            cursor.close()
            if user and bcrypt.checkpw(password.encode('utf-8'),user[3].encode('utf-8')):
                 session['user_id'] = user[0]
                 return redirect(url_for('dashboard'))
            else:
                flash("Login failed. Please check your email and password")
                return redirect(url_for('login'))
        return render_template("login.html",form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
        form = RegistrationForm()
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            confirm_password = form.confirm_password.data  

            print("Form validation passed")  

            if password == confirm_password:
                print("Passwords match")  

                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                try:
                    print(f"Inserting into database: Name={name}, Email={email}")
                    cursor = mysql.connection.cursor()
                    cursor.execute(
                        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                        (name, email, hashed_password)
                 )
                    mysql.connection.commit()
                    cursor.close()

                    print("User registered successfully, redirecting to login")  
                    return redirect(url_for('login'))
                except Exception as e:
                    print(f"Database error: {e}")  
                    flash(f"An error occurred: {e}", "danger")
            else:
                print("Passwords do not match")  
                flash("Passwords do not match. Please try again.", "danger")

        return render_template("signup.html", form=form)
    
            
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' in session:  
        user_id = session['user_id']
        
        cursor = mysql.connect.cursor()
        cursor.execute("SELECT name FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            username = user[0]  
        else:
            username = "Guest"  

        form = BookingForm()  

        return render_template("dashboard.html", username=username, form=form)
    else:
        flash("Please log in to access the dashboard.", "danger")
        return redirect(url_for('login'))

@app.route('/book', methods=['GET', 'POST'])
def book():
    form = BookingForm()

    if form.validate_on_submit():

        course = form.course.data
        trainee = form.trainee.data
        date = form.date.data
        slot = form.slot.data

        user_id = session.get('user_id')
        
        if user_id:
            try:
                cursor = mysql.connection.cursor()
                cursor.execute("""
                    INSERT INTO booking (user_id, course, trainee, booking_date, slot)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, course, trainee, date, slot))
                mysql.connection.commit()
                cursor.close()

                flash('Booking successfully saved!', 'success')
            except Exception as e:
                flash(f'Error saving booking: {e}', 'danger')
        else:
            flash('Please log in to book a class.', 'danger')

        return redirect(url_for('dashboard'))
        

    return render_template('dashboard.html', form=form)

@app.route('/get_bookings', methods=['GET'])
def get_bookings():
    if 'user_id' not in session:
        return {"error": "Unauthorized"}, 401

    user_id = session['user_id']

    try:
        cursor = mysql.connect.cursor()
        cursor.execute("""
            SELECT id, course, trainee, booking_date, slot 
            FROM booking 
            WHERE user_id = %s
        """, (user_id,))
        bookings = cursor.fetchall()
        cursor.close()

        bookings_data = [
            {
                "id": booking[0],
                "course": booking[1],
                "trainee": booking[2],
                "booking_date": booking[3].strftime("%d-%m-%Y"), 
                "slot": booking[4]
            }
            for booking in bookings
        ]
        return {"bookings": bookings_data}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/base')
def base():
    return render_template("base.html")

if __name__ == "__main__": 
    app.run(debug=True)
