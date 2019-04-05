from flask import Flask, request

app = Flask(__name__)

app.config['DEBUG'] = True     # Display errors in the browser too

page_header = """
<!DOCTYPE HTML>
<html>
<head>
 <title>MiniBook</title>

 <style>
 input[type=text], select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 18px;
}

input[type=password], select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 18px;
}

input[type=submit] {
  width: 100%;
  background-color: #3b5998;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 18px;
}

input[type=submit]:hover {
  background-color: #8b9dc3;
}

div {
  width: 65%;
  margin-left: auto;
  margin-right: auto;
  margin-top: 35px;
  margin-bottom: 35px;
  border-radius: 5px;
  background-color: #f2f2f2;
  padding: 20px;
}

.email {
  color: blue;
}

.alert {
  color: red;
}
</style>

</head>

<body>
<div>
<h1>Sign Up for MiniBook</h1>
</div>
"""

form = """
<div>
<form method='POST'>
 <span class="alert">{0}</span><input type="text" name="username" value="{4}" placeholder="Username">
 <span class="alert">{1}</span><input type="password" name="password" placeholder="Password">
 <span class="alert">{2}</span><input type="password" name="check_password" placeholder="Verify Password">
 <span class="alert">{3}</span><input type="text" name="email" value="{5}" placeholder="Email (Optional)">
 <input type="submit" value="Register">
</form>
</div>
"""

page_footer = """
</body>
</html>
"""

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
        return page_header + form.format(username_status,password_status,verified_status,email_status,username,email) + page_footer

    if activate != False and email_activate == False:
        message = "Welcome to MiniBook! " + "<br />Your username is: " + username 
        return page_header + "<div>" + "<h2>" + message + "<br />" + email_status + "</h2>" + "</div>" + page_footer
    
    if activate != False and email_activate != False:
        message = "Welcome to MiniBook! " + "<br />Your username is: " + username
        email_message = "Your account confirmation link was sent to:<br /> " + '<span class="email">' + email + "</span>" 
        return page_header + "<div>" + "<h2>" + message + "<br />" + email_message + "</h2>" + "</div>" + page_footer

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == "GET":
        content = page_header + form.format("","","","","","") + page_footer
    elif request.method == "POST":
        content = page_header + form.format("","","","",{4},{5}) + page_footer
    return content


app.run()