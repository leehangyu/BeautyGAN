import tensorflow.compat.v1 as tf
import requests
from flask import request
import hashlib
import os
import numpy as np
import cv2
from beautygan import BeautyGan
import base64
from flask import Flask, request, render_template


ALLOWED_EXTENSIONS = set(['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG'])
app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app._static_folder = UPLOAD_FOLDER
import json
from flask import make_response

beautygan = BeautyGan()

@app.route("/beautygan", methods=['GET', 'POST'])
def beauty_gan():
    if request.method == 'POST':

        file_binary = requests.get(request.form["base64"], verify=False).content if (
            request.form["base64"].startswith("http")) else base64.b64decode(request.form["base64"].split(",")[1])
        name = hashlib.md5(file_binary).hexdigest()
        file_name = 'static/tmpimg/' + name + "_beautygan.png"
        nparr = np.fromstring(file_binary, dtype=np.uint8)
        img = cv2.imdecode(nparr, 1)
        ref_img = cv2.imread(os.path.join("static/makeup", os.path.basename(request.form["imgsrc"])))
        print(ref_img)
        cv2.imwrite(file_name, img)

        res_img = beautygan.predict(cv2.resize(img, (256, 256))[:, :, ::-1],
                                      cv2.resize(ref_img[:, :, ::-1], (256, 256)))[0]
        res_img = res_img * 255


        if os.path.exists(file_name):
            res = {"res": "실행", "name": name + os.path.basename(request.form["imgsrc"]), "status": True}
        else:
            res = {"res": "감지안됨", "status": False}
        resp = make_response()
        resp.status_code = 200
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Content-Type"] = "application/json"
        resp.response = json.dumps(res)
        return resp
    return render_template('beautygan.html')



if __name__ == "__main__":
    #https is not necessary,but web camera only work in https mode
    if os.path.exists("./ssl/cert"):
        app.run(host='0.0.0.0', port=5000, debug=True,
                ssl_context=('./ssl/cert', './ssl/key'))
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
