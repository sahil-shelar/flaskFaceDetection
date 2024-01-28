from flask import Flask, render_template,Response
import cv2

app = Flask(__name__)
faceCascade = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

def frames():
    while True:
        ret,frame=cam.read()
        if not ret:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for x,y,w,h in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h), (255, 0, 0), 2)
                
            ret,buffer = cv2.imencode(".jpg",frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/video")
def video():
    return Response(frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)