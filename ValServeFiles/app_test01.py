#Test code online - using to server up json information
import os
import requests
import os.path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, jsonify, render_template, redirect, url_for, request, make_response
from restparse.parser import Parser
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from urllib.request import urlopen
from flask import flash
import threading
data = 'foo'


app = Flask(__name__)

"""
@app.route("/employees/info", methods=['GET', 'POST'])
def employees():
    emp_id = request.args["employee_id"]
    print(emp_id)
    return "Hello " + emp_id
"""

@app.route("/employees/info", methods=['GET', 'POST'])
def employees():
    if request.method == "GET":
        emp_id = request.args["employee_id"]
        print(emp_id)
        return "Hello " + emp_id
    elif request.method == "POST":
        if not request.is_json:
            print("Invalid json")
            return "invalid json"

        content = request.get_json()
        emp_id = content["employee_id"]
        emp_name = content["employee_name"]
        emp_phone = content["employee_phone"]

        print(emp_id, emp_name, emp_phone)

        return "Information added!"

@app.route('/wordcloud', methods=['POST', 'GET'])
def wordcloudGet():
    try:
        f = open('game.json')
        f.close()
    except IOError:
        print('File is not accessible')
        flash('Files not found or readable. One or more required scraper files (game.json as example) not available - please fix')
        return render_template('wordcloud.html')
    file_content = open("game.json").read()
    #r = requests.get('https://api.github.com/users/runnable')
    return jsonify(file_content)

if __name__ == "__main__":
    app.run(host='127.0.0.4', port=80, threaded=True, debug=True)