from flask import Flask, request, render_template, render_template_string
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

@app.route('/test')
def testLLM():
    result = subprocess.run(['python', 'scripts/parsing.py'], capture_output=True, text=True)
    return result

#TODO: will update with proper code