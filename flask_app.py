from flask import Flask, render_template, request

from cv_face_detector import CVFaceDetector

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            detector = CVFaceDetector(file)
            return detector.get_output_json()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

