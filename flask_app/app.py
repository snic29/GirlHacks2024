import os
import subprocess
import platform
import json
from flask import Flask, request, render_template, render_template_string

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['UPLOAD FOLDER'] = '.'

os_type=platform.system()
if os_type == 'Linux':
    delimiter="/"
elif os_type=='Windows':
    delimiter="\\"

@app.route('/')
def home():
    return render_template('home.html', msg="Resume Remix by GenAI")

#TODO - implementing RAG
@app.route('/eval')
def eval():
    return render_template('home.html', msg="This capability is currently under development.")
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":

        if "file" not in request.files:
            upload_msg = "You must select a json file!"
        else:
            file = request.files["file"]
            if file.filename == "":
                upload_msg = "You must select a json file!"
            else:
                if file:
                    file.save(os.path.join(app.config['UPLOAD FOLDER'], request.form.get("doctype"),file.filename))
                    upload_msg = "File uploaded successfully!"
        
        # render the form when method is get
        return render_template('home.html', msg=upload_msg)
    
    return render_template('upload.html')

@app.route('/test')
def testLLM():
    result = subprocess.run(['python', 'scripts/parsing.py'], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    
    return "Error in parsing.py :" + result.stderr
    
@app.route('/playground', methods=['GET', 'POST'])
def playground():
    if request.method == "POST":
        prompt = request.form.get('prompt')
        file_name = request.form.get('file_name')
        model = request.form.get('model')

        result = subprocess.run(['python', 'scripts/evalPromptsDoc.py', '-file', app.config['UPLOAD FOLDER'] + delimiter + file_name, '-prompt', prompt, '-model', model ], capture_output=True, text=True)
        if result.returncode == 0:
            return render_template_string('<h2> Prompt Completion </h2> <br> Model: <pre>{{m}}</pre> <br> Document: <pre>{{f}}</pre> <br> Prompt: <pre>{{p}}</pre> <br> <br> Completion Results: <pre>{{r}}</pre> ', m=model, f=file_name, p=prompt, r=result.stdout)
        else:
            return render_template('home.html', msg=result.stderr)
            #msg="Error executing the script. Please reload and try again.")

    #render the form when method is get         
    else:
        fp=app.config['UPLOAD FOLDER'] + delimiter + "postings" + delimiter
        fr=app.config['UPLOAD FOLDER'] + delimiter + "resumes" + delimiter
        try:
            fp_list = [f for f in os.listdir(fp) if os.path.isfile(os.path.join(fp, f))] 
            fp_list= ["postings" + delimiter + f for f in fp_list]
        except FileNotFoundError:
            fp_list = []
        try:
            fr_list =  [f for f in os.listdir(fr) if os.path.isfile(os.path.join(fr, f))]
            fr_list= ["resumes" + delimiter + f for f in fr_list]
        except FileNotFoundError:
            fr_list = []
        file_names=fp_list + fr_list 
        fp_list=None
        fr_list=None
        
        return render_template('playground.html', file_names=file_names)

if __name__ == "__main__ ":
    app.run(debug=True, threaded=True, use_reloader=False)