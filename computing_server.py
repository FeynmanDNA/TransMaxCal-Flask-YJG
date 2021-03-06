from flask import Flask, jsonify, render_template, request
from time import localtime, strftime, time
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

@app.route('/Bare_DNA_Cal/')
def Bare_DNA_Cal():
    # record the request submit time
    submit_time = strftime("%Y-%m-%d %H:%M:%S", localtime())

    # show submit time to stdout
    print("@", submit_time)

    # print out the request headers like user-agent etc
    print("==========request.headers for Bare_DNA_Cal received by Flask is:=========")
    print(request.headers)

    # process the URL input
    DNA_length = request.args.get('DNAlength')
    force_str = request.args.get('force').split(",")
    torque = request.args.get('torque')
    max_mode = request.args.get('maxMode')

    # to prevent empty url queries
    try:
        int(DNA_length)
        for i in force_str:
            float(i)
        float(torque)
        int(max_mode)
    except (TypeError, ValueError):
        print("empty or invalid  url queries detected")
        return "please input valid parameters"

    # force_str is now list like ['1', '20', '199', '0.1']
    if len(force_str)>20:
       return "user manually key in more than 20 force for Bare_DNA_Cal"

    force = [float(i) for i in force_str]
    # force is an array [1.0, 20.0, 199.0, 0.1]

    # server-side url queries validation
    # first validate force array
    for item in force:
        if item <=0 or item>=200:
            print("user is entering force values in url...")
            return "please submit valid force values"

    if (int(DNA_length) <= 0 or
        float(torque) < -30 or
        float(torque) > 50 or
        int(max_mode) < 10 or
        int(max_mode) >20):
        print("user is entering the url queries in the pop up...")
        return "please submit valid parameters"

    return render_template('TransMatCalBareDNA.html',
                           submit_time = submit_time,
                           DNA_length = DNA_length,
                           force = force,
                           torque = torque,
                           max_mode = max_mode
                           )

@app.route('/With_Nul_Cal/')
def With_Nul_Cal():
    # record the request submit time
    submit_time = strftime("%Y-%m-%d %H:%M:%S", localtime())

    # show submit time to stdout
    print("@", submit_time)

    # print out the request headers like user-agent etc
    print("==========request.headers for With_Nul_Cal received by Flask is:=========")
    print(request.headers)

    # process the URL input
    DNA_length = request.args.get('DNAlength')
    force_str = request.args.get('force').split(",")
    torque = request.args.get('torque')
    protein_E = request.args.get('proteinEnergy')
    max_mode = request.args.get('maxMode')

    # to prevent empty url queries
    try:
        int(DNA_length)
        for i in force_str:
            float(i)
        float(torque)
        float(protein_E)
        int(max_mode)
    except (TypeError, ValueError):
        print("empty or invalid  url queries detected")
        return "please input valid parameters"

    # force_str is now list like ['1', '20', '199', '0.1']
    if len(force_str)>5:
       return "user manually key in more than 5 force for With_Nul_Cal"

    force = [float(i) for i in force_str]
    # force is an array [1.0, 20.0, 199.0, 0.1]

    # server-side url queries validation
    # first validate force array
    for item in force:
        if item <=0 or item>=31:
            print("user is entering force values in url...")
            return "please submit valid force values"

    if (int(DNA_length) <= 0 or
        float(torque) < -30 or
        float(torque) > 50 or
        float(protein_E) > 100 or
        float(protein_E) < -100 or
        int(max_mode) < 10 or
        int(max_mode) >20):
        print("user is entering the url queries in the pop up...")
        return "please submit valid parameters"

    return render_template('TransMatCalWithNul.html',
                           submit_time = submit_time,
                           DNA_length = DNA_length,
                           force = force,
                           torque = torque,
                           protein_E = protein_E,
                           max_mode = max_mode
                           )

@app.route('/transmaxcal_BareDNA/')
def transmaxcal_BareDNA():
    # process input from /Bare_DNA_Cal as GET in the URL queries
    print(">>>>>>>>>Page now redirect to /transmaxcal_BareDNA")
    print("request.args is:")
    print(request.args)
    DNA_length = request.args.get('DNA_length')
    force = request.args.get('force').split(",")
    torque = request.args.get('torque')
    max_mode = request.args.get('max_mode')

    # initiate outs as empty list
    outs = []
    cal_procs = []

    # record the time taken for calculation
    cal_start = int(round(time() * 1000))

    # force is a list like ['1', '3.3', '5']
    for i in force:
        cal_proc = subprocess.Popen(["./Bare-DNA.out", \
                   "%s" % (DNA_length), "%s" % (i), "%s" % (torque), "%s" % (max_mode)], \
                   stdout=subprocess.PIPE)
        cal_procs.append(cal_proc)
    for cal_proc in cal_procs:
        outs.append(cal_proc.stdout.read().decode('ascii'))
        print("cal_proc now is ", cal_proc)

    # elapsed time is in sec
    cal_end = int(round(time() * 1000))
    cal_elapsed = (cal_end-cal_start)/1000

    finish_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print("Now /transmaxcal_BareDNA returns the json back to page")
    return jsonify(done_time = finish_time, elapsed_time = cal_elapsed, result = outs)

@app.route('/transmaxcal_WithNul/')
def transmaxcal_WithNul():
    # process input from /With_Nul_Cal as GET in the URL queries
    print(">>>>>>>>>Page now redirect to /transmaxcal_WithNul")
    print("request.args is:")
    print(request.args)
    DNA_length = request.args.get('DNA_length')
    force = request.args.get('force').split(",")
    torque = request.args.get('torque')
    protein_E = request.args.get('protein_E')
    max_mode = request.args.get('max_mode')

    # initiate outs as empty list
    outs = []
    cal_procs = []

    # record the time taken for calculation
    cal_start = int(round(time() * 1000))

    # force is a list like ['1', '3.3', '5']
    for i in force:
        cal_proc = subprocess.Popen(["./artem_nucleosome_update_Apr.out", \
                   "%s" % (DNA_length), "%s" % (i), "%s" % (torque), "%s" % (protein_E), "%s" % (max_mode)], \
                   stdout=subprocess.PIPE)
        cal_procs.append(cal_proc)
    for cal_proc in cal_procs:
        outs.append(cal_proc.stdout.read().decode('ascii'))
        print("cal_proc now is ", cal_proc)

    # elapsed time is in sec
    cal_end = int(round(time() * 1000))
    cal_elapsed = (cal_end-cal_start)/1000

    finish_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print("Now /transmaxcal_WithNul returns the json back to page")
    return jsonify(done_time = finish_time, elapsed_time = cal_elapsed, result = outs)

@app.route('/jsonshowtime/')
def jsonshowtime():
    time_json = strftime("%Y-%m-%d %H:%M:%S", localtime())
    return jsonify(result = time_json)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 7717, threaded=True)

