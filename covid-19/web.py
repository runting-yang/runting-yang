from flask import Flask,request
from flask import render_template
import os
from pathlib import Path


app = Flask(__name__, static_folder='', static_url_path='')
#app = Flask(__name__)
# system_path = os.path.dirname(__file__)
system_path=os.getcwd()
#system_path="./"
@app.route('/')
def te(imgPath=None, result="None"):
    return render_template('index.html', imgPath="./templates/unit.jpg",result="./templates/unit.jpg")

@app.route('/upload', methods=['POST'])
def upload(imgPath=None, result="None"):
    file = request.files['file']
    fileName = file.filename
    filePath = "./docs/images/"+fileName
    outPath = "./docs/output/"+fileName
    imgPath=filePath
    if file:
        file.save(filePath)
        os.system("python image_demo.py --image_name %s" % (fileName))
        file = open('./docs/output/out.txt', 'r')
        CT_result= file.readline()
        CT_probability=file.readline()
        file.close()
        return render_template('index.html', imgPath=filePath,result=outPath,CT_result=CT_result,CT_probability=CT_probability)
    return render_template('index.html', imgPath="./templates/unit.jpg",result="./templates/unit.jpg")

if __name__ == '__main__': 
	app.run(host="0,0,0,0",debug=True)