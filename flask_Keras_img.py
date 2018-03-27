#$ export(set in  Win) FLASK_APP=my_application  
#$ export(set in  Win) FLASK_DEBUG=1
#$ flask run
#set FLASK_APP=flask_Keras_img.py && set FLASK_DEBUG=1 && flask run

import kfunctions as kf
from flask import Flask, render_template
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])

dane_odpowiedz = []
lista_zdjec = []  

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('my_form.html')

@app.route('/onas.html')
def onas():
    return render_template('onas.html')

@app.route('/api', methods = ['POST'])
def dane():
    dane_xor = request.form['xor']
    print('dane wejściowe: ',dane_xor)
    dane_odpowiedz.append(dane_xor)
    a = kf.przygotowanie_danych(dane_xor)
    model = kf.upload_model()
    odpowiedz = model.predict(a)
    if odpowiedz < 0.1:
        dane_odpowiedz.append(0)
        print('xor od ',dane_xor,' to 0')
    else:
        print('xor od ',dane_xor,' to 1')
        dane_odpowiedz.append(1)
    return redirect('/odpowiedz.html')

@app.route('/odpowiedz.html')
def odpowiedz():
    return render_template('odpowiedz.html',dane_odpowiedz=dane_odpowiedz)

@app.route('/upload.html', methods = ['GET', 'POST'])
def upload_file():
    picture_path = request.args.get('filename')
    picture_path = 'static/uploads/'+str(picture_path)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no image')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('no image selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            lista_zdjec.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', filename=filename)) 
    return render_template('upload.html', picture_path=picture_path)

@app.route('/jakatocyfra.html')
def jaka_to_cyfra():
    global lista_zdjec
    picture = lista_zdjec[-1]
    picture_path = 'static/uploads/'+str(picture)
    img = kf.prepare_img(picture_path)
    model = kf.upload_model_MNIST()
    prediction = kf.odp_sieci(model.predict(img))
    return render_template('jakatocyfra.html', prediction=prediction, picture=picture)

@app.route('/draw.html')
def draw():
    return render_template('draw.html')

if __name__ == '__main__':
    app.run()