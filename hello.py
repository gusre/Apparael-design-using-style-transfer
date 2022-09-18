# Shamelessly copied from http://flask.pocoo.org/docs/quickstart/

from tkinter import N
from turtle import color
from flask import Flask, render_template, request
from flask import jsonify
import json
import io, base64,os
from PIL import Image
from usermask  import *
from colorpalette import *
from IFT import *
import shutil  


app = Flask(__name__,template_folder='template')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER']='./figures'


number_of_areas=1
number_of_styles=1


def remfiles(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

@app.route('/areas', methods = ['GET'])
def get_Areas():
    return jsonify({'number':number_of_areas})

@app.route('/styles', methods = ['GET'])
def get_stylenum():
    return jsonify({'number':number_of_styles})

@app.route('/getresult', methods = ['GET','POST'])
def get_Result():
    print(request)
    data=request.data.decode('UTF-8')
    data=json.loads(data)
    print(data)
    mode=data["mode"]
    if mode =="1":
        blendormix=data["blend"]
    else:
        blendormix=data["mix"]
    color=data["color"]
    style_scale=data["stylescale"]
    style_transfer(mode,color,blendormix,number_of_areas,number_of_styles,style_scale)
    with open("./figures/tmp/result.png", "rb") as image_file:
        dataimg = base64.b64encode(image_file.read())
    #print(dataimg)
    return jsonify({'number':str(dataimg)})

@app.route('/colors', methods = ['POST','GET'])
def get_Colors():
    file=request.files['file']
    num_colors=request.form['num']
    style_num=request.form['stylenum']
    
    print(file,num_colors,style_num)
    if file :
        file.save(os.path.join(app.config['UPLOAD_FOLDER']+'/tmp','color.png'))
    colors=get_colors(num_colors,style_num)
    return jsonify({'colors':colors})

@app.route('/content', methods = ['POST','GET'])
def get_Contentimage():
    print(request)
    data=request.data.decode('UTF-8')
    data=json.loads(data)
    image_string=data['image']
    base64_str =image_string.replace('data:image/jpeg;base64,', '')
    # Assuming base64_str is the string value without 'data:image/jpeg;base64,'
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(base64_str, "utf-8"))))
    img.save('./figures/content/content.png')
    process_content(data['points'])
    global number_of_areas
    number_of_areas=len(data['points'])
    print(number_of_areas)
    return jsonify({'Status':'OK'})


@app.route('/style', methods = ['POST'])
def get_styleimages():
    print(request)
    print(request.files)
    '''for y in request.files:
        print(request.files[y].read())'''
    for i in range(len(request.files)):
        filename='file'+str(i+1)
        filename2='style'+str(i+1)
        file=request.files[filename]
        if file :
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+'/style',filename+'.png'))
            shutil.copyfile(app.config['UPLOAD_FOLDER']+'/style/'+filename+'.png', app.config['UPLOAD_FOLDER']+'/style/'+filename2+'.png')  

    global number_of_styles
    number_of_styles=len(request.files)
    return jsonify({'Status':'OK'})


@app.route('/clrchange',methods=['POST'])
def style_color():
    data=request.data.decode('utf-8')
    data=json.loads(data)
    swap_colors(data['color'])

    with open("./figures/style/style{}.png".format(data['color'][0][0]), "rb") as image_file:
        dataimg = base64.b64encode(image_file.read())
    #print(dataimg)
    return jsonify({'number':str(dataimg)})


@app.route('/style1', methods = ['POST'])
def get_style():
    print(request)
    data=request.data.decode('utf-8')
    print(type(data),data)
    data=json.loads(data)
    swap_colors(data['color'])
    print(data['position'])
    return jsonify({'Status':'OK'})
    #return Response(json.dumps({'Status': 'Version mismatch,try again'}), status=422, mimetype="application/json")

@app.route('/colorchange')
def styleup():
    return render_template('colorchange.html')



@app.route('/draw')
def draw():
    return render_template('draw.html')

@app.route('/')
def hello_world():
    return render_template('home.html')

if __name__ == '__main__':
    remfiles('C:/Users/gunas/Music/Flask/figures/style')
    remfiles('C:/Users/gunas/Music/Flask/figures/tmp')
    remfiles('C:/Users/gunas/Music/Flask/figures/colored')
    app.run(debug=True)

