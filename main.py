from flask import Flask, request
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))


app = Flask(__name__)

app.config['DEBUG'] = True     # Display errors in the browser too

@app.route("/", methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    check_password = request.form['check_password']
    email = request.form['email']

    username_status = ""
    password_status = ""
    verified_status = ""
    email_status = ""
    activate = True
    email_activate = True

    if len(username) < 3 or len(username) > 20 or username.isalnum() != True:
        username_status = "Username must be between 3 and 20 alphanumeric characters. No spaces allowed. "
        activate = False

    if len(password) < 3 or len(password) > 20 or password.isalnum() != True :
        password_status = "Password must be between 3 and 20 alphanumeric characters. No spaces allowed. "
        activate = False

    if len(check_password) < 3 or len(check_password) > 20 or check_password.isalnum() != True or check_password != password:
        verified_status = "Both passwords must match and meet the same requirements to verify."
        activate = False

    if len(email) < 3 or len(email) > 20 or email.find("@") < 0 or email.find(".") < 0 or email.find(" ") > -1 :
        email_status = "It is optional, but we recommend that you submit a valid email for your account."
        email_activate = False

        if len(email) > 0 and email_activate == False:
            email_status = "The email you supplied is not valid."
            activate = False
    
    if activate == False:
        message = "Your registration could not be processed.<br />" + username_status + "<br />" + password_status + "<br />" + verified_status
        template = jinja_env.get_template('index.html')
        return template.render(username_alert=username_status,password_alert=password_status,verifypw_alert=verified_status,email_alert=email_status,username=username,email=email)

    if activate != False and email_activate == False:
        template = jinja_env.get_template('welcome.html')
        return template.render(username=username,email_status=email_status)

    if activate != False and email_activate != False:
        message = "Welcome to MiniBook! " + "<br />Your username is: " + username
        email_message = "Your account confirmation link was sent to:<br /> " + '<span class="email">' + email + "</span>"

        template = jinja_env.get_template('welcome.html')
        return template.render(username=username,email_status=email_message)

@app.route("/", methods=['GET','POST'])
def index():
    template = jinja_env.get_template('index.html')
    return template.render()

    


app.run()