import os 
import sys
import psycopg2
import shutil
import logging
import subprocess

from flask import Flask, render_template, make_response, request, redirect
from flask_basicauth import BasicAuth

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from werkzeug.utils import secure_filename


sys.path.append("..")
from config import CREDENTIALS, SERVERS
from utils import my_IP, group_IP
 

# setup custom logging
log = logging.getLogger('datadrop')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler("Datadrop.log", mode="a")
fh.setFormatter(logging.Formatter("%(asctime)s : %(levelname)s : %(funcName)10s() : %(message)s"))
log.addHandler(fh)

app = Flask(__name__)
basic_auth = BasicAuth(app)

def check_credentials(user, password):
    # lookup credentials from file
    return password == CREDENTIALS[user]


basic_auth.check_credentials = check_credentials


@app.route('/', methods=['GET', 'POST'])
@basic_auth.required
def index():
    user = request.authorization.username

    # Each group is assigned to a specific server
    # So that load is eually balanced
    # and we only have to read log files present locally on disk

    if my_IP() != group_IP(user):
        return redirect("http://%s:%d" % (group_IP(user), 5000))
    
    if request.method = "GET":
        return render_template("base.html", group = user.strip().split("_")[-1])
    
    file = request.files['file']

    # keep in mind that this function is called multiple times for the same file!
    current_chunk = int(request.form['dzchunkindex'])
    student_dir = os.path.join("../uploads", user)
    if not os.path.exists(student_dir):
        os.makedirs(student_dir)



if __name__ == "__main__":
    app.run(host="localhost", port=5004)