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
    cal_proc = subprocess.Popen(["C:\\Users\\LUMICKS\\Desktop\\FlaskServer\\gppCMDversionFeb19th.exe", \
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
    # if cal_proc is not finished
    if cal_proc is None or cal_proc.poll() is None:
        return jsonify(computationStatus = False)
    else:
        # non-block method (but .stdout.read() actually block...)
        outs = cal_proc.stdout.read().decode('ascii')
        print(outs)
        finish_time = strftime("%Y-%m-%d %H:%M:%S", localtime())

        # reset global cal_proc
        cal_proc = None

        return jsonify(computationStatus = True, done_time = finish_time, result = outs)

@app.route('/jsontest/')
def jsontest():
    # first check if there is already a transmaxcal process
    global cal_proc

    if cal_proc is None:
        pass
    elif cal_proc.poll() is None:
        # the transmaxcal subprocess is alive
        return render_template('BlockFurReq.html')

    # print out the request headers like user-agent etc
    print(request.headers)
    # for user to click to see current server time
    submit_time = strftime("%Y-%m-%d %H:%M:%S", localtime())

    # process the URL input
    DNA_length = request.args.get('DNAlength')
    force = request.args.get('force')
    torque = request.args.get('torque')
    max_mode = request.args.get('maxMode')

    return render_template('TransMatCal.html',
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

