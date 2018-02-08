from flask import Flask, jsonify, render_template, request
from time import localtime, strftime
import subprocess

app = Flask(__name__)

@app.route('/')
def hello():
    outs, errs = subprocess.Popen([\
        "C:\Octave\Octave-4.2.1\\bin\octave-cli.exe", "--eval", \
        "main_DNA_force_torque_spectrum_new(0,0,0,0)"], \
        stdout=subprocess.PIPE, \
        cwd='C:\\Users\\LUMICKS\\Desktop\\Artem').communicate()
    return outs

@app.route('/jsontest/')
def jsontest():
    print(request.headers)
    submit_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    DNA_length = request.args.get('DNAlength')
    force = request.args.get('force')
    torque = request.args.get('torque')
    max_mode = request.args.get('maxMode')
    return render_template('TransMaxCal.html', 
                           submit_time = submit_time,
                           DNA_length = DNA_length,
                           force = force,
                           torque = torque,
                           max_mode = max_mode
                           )

@app.route('/jsonshowtime/')
def jsonshowtime():
    time_json = strftime("%Y-%m-%d %H:%M:%S", localtime())
    return jsonify(result = time_json)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 7717)

"""
for future reference: this actually worked
    output, rubbish = subprocess.Popen([\
        "C:\Octave\Octave-4.2.1\\bin\octave-cli.exe", "--eval", \
        "OctaveSumTest(1,2)"], \
        stdout=subprocess.PIPE, \
        cwd='C:\\Users\LUMICKS\Desktop\FlaskServer').communicate()
"""
