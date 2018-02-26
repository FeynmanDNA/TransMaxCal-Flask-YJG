from flask import Flask, jsonify, render_template, request
from time import localtime, strftime
import subprocess
import sys

# replace sys.stdout with some other stream like wrapper
# which does a flush after every call.
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

app = Flask(__name__)

<<<<<<< HEAD
=======
# global variable to show computation status
cal_proc = None

@app.route('/transmaxcal/')
def transmaxcal():
    # process input from /jsontest as GET in the URL queries
    print("page now redirect to /transmaxcal and request.args is: ", request.args)
    DNA_length = request.args.get('DNA_length')
    force = request.args.get('force')
    torque = request.args.get('torque')
    max_mode = request.args.get('max_mode')

    # call the global variable cal_proc
    global cal_proc

    # subprocess run the computation
    cal_proc = subprocess.Popen(["C:\\Users\\LUMICKS\\Desktop\\FlaskServer\\gppCMDversionFeb23rd.exe", \
            "%s" % (DNA_length), "%s" % (force), "%s" % (torque), "%s" % (max_mode)], \
        stdout=subprocess.PIPE)

    return jsonify(serverMsg = "Program Started", computationStarted = True)

@app.route('/kill_transmaxcal/')
def kill_transmaxcal():
    # first call the global variable
    global cal_proc
    # detect if stopCal signal is present
    print(request.args)
    stop_cal = request.args.get('stopCal')
    if stop_cal == "confirmed":
        #if cal_proc: cal_proc.kill()
        try:
            cal_proc.kill()
        except AttributeError:
            # if connection between popup and server resumes
            pass
        finish_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        print("calculation cancelled by user @ ", finish_time)

        # reset global cal_proc
        cal_proc = None

        return jsonify(confirmedkill = True, done_time = finish_time)

    return "kill the boy!"

@app.route('/check_computation_status/')
def check_computation_status():
    # first call the global variable
    global cal_proc
    # process pollServer from webpage
    if cal_proc is None:
        # calculator.exe stopped prematurely
        outs = ""
        finish_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        return jsonify(computationStatus = True, done_time = finish_time, result = outs)
    elif cal_proc.poll() is None:
        # if cal_proc is not finished
        return jsonify(computationStatus = False)
    else:
        # non-block method (but .stdout.read() actually block...)
        outs = cal_proc.stdout.read().decode('ascii')
        print(outs)
        finish_time = strftime("%Y-%m-%d %H:%M:%S", localtime())

        # reset global cal_proc
        # only after computation status is checked is cal_proc resetted
        cal_proc = None

        return jsonify(computationStatus = True, done_time = finish_time, result = outs)

>>>>>>> master
@app.route('/jsontest/')
def jsontest():
    # record the request submit time
    submit_time = strftime("%Y-%m-%d %H:%M:%S", localtime())

<<<<<<< HEAD
    # show submit time to stdout
    print("@", submit_time)

    # print out the request headers like user-agent etc
    print("==========request.headers received by Flask is:=========")
    print(request.headers)
=======
    # cal_proc is None when Flask first start
    # or previous calculations are finished (reset by check_computation_status)
    # only proceed to send transmaxcal route if cal_proc is None
    if cal_proc is None:
        pass
    else:
        # the transmaxcal subprocess is alive
        # OR this request is sent before
        # check_computation_status has reset the cal_proc
        return render_template('BlockFurReq.html')

    # print out the request headers like user-agent etc
    print("request.headers received by Flask is: ", request.headers)
    # for user to click to see current server time
    submit_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
>>>>>>> master

    # process the URL input
    DNA_length = request.args.get('DNAlength')
    force_str = request.args.get('force').split(",")
    torque = request.args.get('torque')
    max_mode = request.args.get('maxMode')

    # to prevent empty url queries
    try:
        int(DNA_length)
<<<<<<< HEAD
        for i in force_str:
            float(i)
=======
        float(force)
>>>>>>> master
        float(torque)
        int(max_mode)
    except (TypeError, ValueError):
        print("empty or invalid  url queries detected")
        return "please input valid parameters"

<<<<<<< HEAD
    # force_str is now list like ['1', '20', '199', '0.1']
    force = [float(i) for i in force_str]
    # force is an array [1.0, 20.0, 199.0, 0.1]

    # server-side url queries validation
    # first validate force array
    for item in force:
        if item <=0 or item>=200:
            print("user is entering force values in url...")
            return "please submit valid force values"

    if (int(DNA_length) <= 0 or
=======
    # server-side url queries validation
    if (int(DNA_length) <= 0 or
        float(force) <= 0 or
        float(force) >= 200 or
>>>>>>> master
        float(torque) < -30 or
        float(torque) > 50 or
        int(max_mode) < 10 or
        int(max_mode) >20):
        print("user is entering the url queries in the pop up...")
<<<<<<< HEAD
        return "please submit valid parameters"
=======
        return "please submit valid  parameters"
>>>>>>> master

    return render_template('TransMatCal.html',
                           submit_time = submit_time,
                           DNA_length = DNA_length,
                           force = force,
                           torque = torque,
                           max_mode = max_mode
                           )

@app.route('/transmaxcal/')
def transmaxcal():
    # process input from /jsontest as GET in the URL queries
    print(">>>>>>>>>Page now redirect to /transmaxcal")
    print("request.args is:")
    print(request.args)
    DNA_length = request.args.get('DNA_length')
    force = request.args.get('force').split(",")
    torque = request.args.get('torque')
    max_mode = request.args.get('max_mode')

    # initiate outs as empty list
    outs = []
    # force is a list like ['1', '3.3', '5']
    for i in force:
        cal_proc = subprocess.Popen(["./artem_update.out", \
                   "%s" % (DNA_length), "%s" % (i), "%s" % (torque), "%s" % (max_mode)], \
                   stdout=subprocess.PIPE)
        outs.append(cal_proc.stdout.read().decode('ascii'))
        print("cal_proc now is ", cal_proc)

    finish_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print("Now /transmaxcal/ returns the json back to page")
    return jsonify(done_time = finish_time, result = outs)

@app.route('/jsonshowtime/')
def jsonshowtime():
    time_json = strftime("%Y-%m-%d %H:%M:%S", localtime())
    return jsonify(result = time_json)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 7717, threaded=True)

