from flask import Flask, render_template, request
import argparse

import socket

app = Flask(__name__)
# add socket connection to simPat

# 


s = socket.socket()
s.connect(('127.0.0.1',12345))

@app.route("/", methods=['GET', 'POST'])


def index():
    print(request.method)
  
    if request.method == 'POST':
        if request.form.get('Forward') == 'Forward':
                # pass
            # add bittarray to send
            print("Forward")
        elif  request.form.get('Reverse') == 'Reverse':
            # pass # do something else
           print("Reverse")
        elif  request.form.get('Left') == 'Left':
            # pass # do something else
           print("Left")

        elif  request.form.get('Right') == 'Right':
            # pass # do something else
           print("Right")
        elif  request.form.get('Stop') == 'Stop':
            # pass # do something else
           print("Stop")
        elif  request.form.get('CounterClock') == 'CounterClock':
            # pass # do something else
           print("CounterClock")
        elif  request.form.get('ClockWise') == 'ClockWise':
            # pass # do something else
           print("ClockWise")
        elif  request.form.get('StartDetectionTrack') == 'StartDetectionTrack':
            # pass # do something else
           print("StartDetectionTrack")
        else:
                # pass # unknown
            return render_template("index.html")
    elif request.method == 'GET':
            # return render_template("index.html")
        print("No Post Back Call")
    return render_template("index.html")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")

    args = vars(ap.parse_args())

    app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)
    s.send(str.encode());
    str = input("S: ")