from flask import Flask, jsonify, render_template, request, session, redirect
from time import localtime, strftime
import subprocess

app = Flask(__name__)
# for request and session
app.secret_key = 'C++Bear'

# global variable to show computation status
cal_proc = None

@app.route('/transmaxcal/')
def transmaxcal():
    # process input from /jsontest as GET in the URL queries
    print(request.args)
    DNA_length = request.args.get('DNA_length')
    force = request.args.get('force')
    torque = request.args.get('torque')
    max_mode = request.args.get('max_mode')

    # call the global variable cal_proc
    global cal_proc

    # subprocess run the computation
    cal_proc = subprocess.Popen([\
        "C:\Octave\Octave-4.2.1\\bin\octave-cli.exe", "--eval", \
        "main_DNA_force_torque_spectrum_new(%s,%s,%s,%s)" % (DNA_length, force, torque, max_mode)], \
        stdout=subprocess.PIPE, \
        cwd='C:\\Users\\LUMICKS\\Desktop\\Artem')

    return jsonify(serverMsg = "Program Started")

@app.route('/kill_transmaxcal/')
def kill_transmaxcal():
    # first call the global variable
    global cal_proc
    # detect if stopCal signal is present
    print(request.args)
    stop_cal = request.args.get('stopCal')
    if stop_cal == "confirmed":
        cal_proc.kill()
        print("calculation cancelled by user")
        return jsonify(confirmedkill = True)
    return "kill the boy!"

@app.route('/check_computation_status/')
def check_computation_status():
    # first call the global variable
    global cal_proc
    # process pollServer from webpage
    # if cal_proc is not finished
    if cal_proc is None or cal_proc.poll() is None:
        return jsonify(computationStatus = False)
    else:
        # non-block method (but .stdout.read() actually block...)
        outs = cal_proc.stdout.read().decode('ascii')
        print(outs)
        finish_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        return jsonify(computationStatus = True, done_time = finish_time, result = outs)

@app.route('/jsontest/')
def jsontest():
    # print out the the request headers like user-agent etc
    print(request.headers)
    # for user to click to see current server time
    submit_time = strftime("%Y-%m-%d %H:%M:%S", localtime())

    # process the URL input
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
