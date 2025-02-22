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
        # return redirect("http://%s:%d" % ("0.0.0.0", 5000))

    if request.method == "GET":
        return render_template("base.html", group = user.strip().split("_")[-1])

    file = request.files['file']

    # keep in mind that this function is called multiple times for the same file!
    current_chunk = int(request.form['dzchunkindex'])
    student_dir = os.path.join("../uploads", user)
    if not os.path.exists(student_dir):
        os.makedirs(student_dir)

    file_path = os.path.join(student_dir, secure_filename(file.filename))

    if os.path.exists(student_dir) and current_chunk == 0:
        try:
            # Delete entire student folder
            # Solves the problem of student uploading file with different name
            shutil.rmtree(student_dir)
            os.makedirs(student_dir)
        except OSError:
            return make_response(("Unable to delete old uploads.", 400))

    # Write chunk to file
    try:
        with open(file_path, 'ab') as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            f.write(file.stream.read())
    except OSError:
        err = "Couldn't write to file"
        log.exception(err)
        return make_response((err, 500))

    # Finished writing chunks
    total_chunks = int(request.form['dztotalchunkcount'])
    if current_chunk + 1 == total_chunks:
        msg = pg_load(user, request.authorization.password, file_path)

        # Crude way of detecting that an error has occured
        if b"ERROR:" in msg:
            log.error("%s - PG SQL returned : %s", user, msg.decode("ascii", "ignore"))
            return make_response((msg, 400))
        else:
            log.debug("%s - Data upload successful", user)
            return make_response((msg, 200))
    return make_response(("Chunk upload successful", 200))

def connect(ip, user, pswd, dbname="postgres"):
    log.debug("%s - Connecting to %s:5432" % (user, ip))
    try:
        conn = psycopg2.connect(
            user = user,
            host = ip,
            port = "5432",
            password = pswd,
            dbname = dbname
        )
        return conn
    except psycopg2.Error as e:
        log.debug("%s - Error connecting to postgres server \n %s" % (user, str(e)))
        return None

def cleanup(conn, group):
    q1 = "DROP DATABASE IF EXISTS {};".format(group)
    q2 = "CREATE DATABASE {};".format(group)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(q1)
    log.debug("%s - query - %s, status - %s", group, q1, cur.statusmessage)
    cur.execute(q2)
    log.debug("%s - query - %s, status - %s", group, q2, cur.statusmessage)
    conn.commit()

def pg_load(user, pswd, dump_path):
    ip = group_IP(user)
    log.debug("%s - Performing cleanup before loading", user)
    conn = connect(ip, "postgres", "vpl-362")

    cleanup(conn, user)
    conn.close()
    log.debug("%s - Cleanup complete", user)

    # Load Databases
    print("\n\n\n\n")
    print(dump_path)
    print("\n\n\n\n")
    cmd = 'PGPASSWORD="vpl-362" psql -h {ip} -d {db} -U postgres < "{dump}"'.format(pswd=pswd, ip=ip,
    db=user, user=user, dump=dump_path)
    log.debug("%s - Running command : %s", user, cmd)
    msg = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    log.debug("%s - Database Loading Complete", user)

    # Revoke Privileges
    conn = connect(ip, "postgres", "vpl-362", dbname=user)
    log.debug("%s- Revoking Privileges", user)
    # query = """
    # REVOKE CREATE ON SCHEMA public FROM public;
    # GRANT ALL ON schema public TO postgres;
    # GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {user};
    # GRANT SELECT ON ALL TABLES IN SCHEMA public TO {user};
    # """

    query = """
    GRANT CONNECT ON DATABASE {group} TO {user};
    GRANT ALL PRIVILEGES ON DATABASE {group} TO {user};
    GRANT USAGE ON SCHEMA public TO {user};
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {user};
    """
    conn.cursor().execute(query.format(user=user,group=user))
    conn.commit()
    conn.close()
    return msg

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
