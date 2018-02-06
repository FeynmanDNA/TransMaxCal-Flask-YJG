from flask import Flask, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    output, rubbish = subprocess.Popen([\
        "C:\Octave\Octave-4.2.1\\bin\octave-cli.exe", "--eval", \
        "main_DNA_force_torque_spectrum_new(0,0,0,0)"], \
        stdout=subprocess.PIPE, \
        cwd='C:\\Users\\LUMICKS\\Desktop\\Artem').communicate()
    return output
    
@app.route('/jsontest/')
def jsontest():
    return jsonify(result="TEST!")
    

if __name__ == "__main__":
    app.run(host = "0.0.0.0", ssl_context=('cert.pem', 'key.pem'), port = 7717)

"""
for future reference: this actually worked
    output, rubbish = subprocess.Popen([\
        "C:\Octave\Octave-4.2.1\\bin\octave-cli.exe", "--eval", \
        "OctaveSumTest(1,2)"], \
        stdout=subprocess.PIPE, \
        cwd='C:\\Users\LUMICKS\Desktop\FlaskServer').communicate()
"""
