from flask import Flask, render_template, request, send_file, abort
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

USE_REMBG = False
try:
    from rembg import remove
    USE_REMBG = True
except Exception:
    USE_REMBG = False

try:
    import cv2
    import numpy as np
    USE_CV2 = True
except Exception:
    USE_CV2 = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        abort(400, 'no file')
    f = request.files['image']
    if f.filename == '':
        abort(400, 'empty filename')

    img_bytes = f.read()

    if USE_REMBG:
        try:
            out_bytes = remove(img_bytes)
            return send_file(BytesIO(out_bytes), mimetype='image/png')
        except Exception as e:
            print('rembg failed', e)

    if USE_CV2:
        try:
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            blur = cv2.GaussianBlur(img, (21,21), 0)
            gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
            mask = cv2.medianBlur(mask, 5)
            b,g,r = cv2.split(img)
            rgba = cv2.merge([b,g,r,mask])
            _, buf = cv2.imencode('.png', rgba)
            return send_file(BytesIO(buf.tobytes()), mimetype='image/png')
        except Exception as e:
            print('cv2 fallback failed', e)

    try:
        im = Image.open(BytesIO(img_bytes)).convert('RGBA')
        buf = BytesIO()
        im.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        abort(500, str(e))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)