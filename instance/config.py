from Housemeapp import app

SECRET_KEY = 'QWERTYUIOP'
# MAIL_SERVER='smtp.gmail.com'
# MAIL_PORT=465
# MAIL_USERNAME='eventstrolley@gmail.com'
# MAIL_PASSWORD='creativityhub'
# MAIL_USE_SSL=True

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'eventstrolley@gmail.com'
app.config['MAIL_PASSWORD'] = 'creativityhub'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

