# https://stackoverflow.com/questions/25149493/how-to-call-another-webservice-api-from-flask
# https://thispointer.com/python-three-ways-to-check-if-a-file-is-empty/
# https://www.geeksforgeeks.org/how-to-create-a-pop-up-message-when-a-button-is-pressed-in-python-tkinter/
# https://stackoverflow.com/questions/23112316/using-flask-how-do-i-modify-the-cache-control-header-for-all-output
# https://dbader.org/blog/python-check-if-file-exists#:~:text=The%20most%20common%20way%20to%20check%20for%20the,search%20engine%20on%20how%20to%20solve%20this%20problem.
# fixing word cloud multi thread issues:
# https://www.shanelynn.ie/using-python-threading-for-multiple-results-queue/
# https://stackoverflow.com/questions/31264826/start-a-flask-application-in-separate-thread
# https://izziswift.com/start-a-flask-application-in-separate-thread/
# other changes
# https://stackoverflow.com/questions/29104107/upload-image-using-post-form-data-in-python-requests
# https://stackoverflow.com/questions/29104107/upload-image-using-post-form-data-in-python-requests
# https://stackoverflow.com/questions/55265779/how-to-jsonify-a-picture-in-flask


import os
import requests
import os.path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
from flask import Flask, jsonify, render_template, redirect, url_for, request, abort
import flask_restful
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from urllib.request import urlopen
from flask import flash
import threading
import base64
import io
import logging
import numpy as np
from PIL import Image
from io import BytesIO
import PIL.Image
data = 'foo'

from forms import runWordCloudForm, AddGameForm, AddGenreForm, AddCreatorForm, AddPlatformForm, \
    AddEpisodeForm, AddToM2MPlatformGame, \
    EditTheGame, SearchForm, SearchForm2, RemoveGame, RemoveGenre, RemoveCreator, \
    RemovePlatform, RemoveEpisode, RemoveGameAndPlatform, SearchPageForm

#application flask run
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300
app.config['SECRET_KEY'] = 'oTv!5ox8LB#A&@cBHpa@onsKU'

def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    h = int(360.0 * 45.0 / 255.0)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)


@app.route('/', methods=['GET', 'POST'])
def index():
    #flash('in the index')
    try:
        f = open('game.json')
        f.close()
    except IOError:
        print('File is not accessible')
    print('File is accessible')
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def cloudMake():
    print('in cloudMake')
    flash('Word Cloud successfully created')
    return redirect(url_for('index'))



@app.route('/SomeFunction', methods=['POST', 'GET'])
def SomeFunction():
    print('In SomeFunction')
    print("inside if")
    file_content = 0
    file_content2 = 0
    file_content = open("game.json").read()
    file_content2 = open("pokemonSnap_keywords.json").read()
    file_content += file_content2
    print("FileContent")
    wordcloud = WordCloud(
        stopwords=STOPWORDS,
        background_color='white',
        width=1200,
        height=1000,
        color_func=random_color_func
    ).generate(file_content)
    plt.imshow(wordcloud)
    plt.axis('off')
    # plt.show()
    # saves picture file to picture format
    plt.savefig('static/wordCloud.png')
    print("wordCloud.png created")
    flash('Success! Word Cloud has been processed and is loading')
    return redirect(url_for('wordcloud'))

#this needs to be the landing page for the word cloud- this is where the user hits the "submit" button
@app.route("/wordcloud", methods=['POST', 'GET'])
def wordcloud():
    flash('Welcome!')
    return render_template('wordcloud.html')

r = ""

@app.route("/getValerie", methods=['POST', 'GET'])
def getValerie():
    #update the following web address to whatever team members web address will be
    r = requests.get("http://127.0.0.4:80/wordcloud")
    return(r)

@app.route("/wordcloud2", methods=['POST', 'GET'])
def wordcloud2():
    #need to update the code below to something along the lines of the web address access
    #perhaps something of "did beavis work"
    try:
        f = open('game.json')
        f.close()
    #when error happens then flashing this error will be helpful
    except IOError:
        print('File is not accessible')
        flash('Files not found or readable. One or more required scraper files (game.json as example) not available - please fix')
        return render_template('wordcloud.html')
    print('File is accessible')
    flash('You created a word cloud')
    #Need to update this to the proper web address for the word cloud
    beavis = requests.get('http://127.0.0.4/wordcloud')
    print("out of beavis")
    #Discovered this after way too long - this forces the text out of beavis and into
    #a format that the cloud generator can run
    file_content = beavis.text
    # literally exists out of total paranoia - shows the text
    print(file_content)
    print('out of file_content')
    print("FileContent")
    #this section generates the word cloud
    wordcloud = WordCloud(
        stopwords=STOPWORDS,
        background_color='white',
        width=1200,
        height=1000,
        color_func=random_color_func
    ).generate(file_content)
    plt.imshow(wordcloud)
    plt.axis('off')
    # plt.show()
    # saves picture file to picture format
    plt.savefig('static/wordCloud.png')
    print("wordCloud.png created")
    flash('Success! Word Cloud has been processed and is loading')
    return render_template('wordcloud2.html')



#
@app.route("/uploadImage", methods=["POST", "GET"])
def upload_image():
    print('in upload image')
    file = request.files['static/wordCloud']
    print('after file')
    # Read the image via file.stream
    img = Image.open(file.stream)
    print(img)
    return jsonify({'msg': 'success', 'size': [img.width, img.height]})


# this never worked - probably should consider deleting this.
@app.route("/test", methods=['POST', 'GET'])
def test_method():
    # print(request.json)
    print('in test')
    if not request.json or 'static/wordCloud.png' not in request.json:
        print('it blew up')
        abort(400)
    print('avoided if not')
    # get the base64 encoded string
    im_b64 = request.json['static/wordCloud.png']

    # convert it into bytes
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))

    # PIL image object to numpy array
    img_arr = np.asarray(img)
    print('img shape', img_arr.shape)

    # process your img_arr here

    # access other keys of json
    # print(request.json['other_key'])

    result_dict = {'output': 'output_key'}
    return result_dict

# this is the only word cloud get method that works
@app.route('/wordcloud66', methods=['POST', 'GET'])
def wordcloudGet66():
    try:
        #f = open('game.json')
        #webbrowser.get('http://127.0.0.4/wordcloud')
        requests.get('http://127.0.0.4/wordcloud')
        #f.close()
    #when error happens then flashing this error will be helpful
    except IOError:
        print('File is not accessible')
        flash('picture file not found')
        return ('File is not accessible')
    print('pre file content opening of word cloud')
    file_content = open("static/wordCloud.png", 'rb')
    with open('static/wordCloud.png', 'rb') as image_file:
        print('file_content')
        encoded_string = base64.b64encode(image_file.read())

        print('file content created')

        print('checking if file can be written')
        #image decoding from recent encoding - this is to prove that
        #encoded string will actually return back to the original picture
        newImage = Image.open(BytesIO(base64.b64decode(encoded_string)))
        print('decode workie?')

        print("test")
        #image is successfully printed to static folder proving that data can be decoded
        newImage.save('static/noob.png', 'PNG')
        print('possible print')

        return (encoded_string)

#this doesn't work probably delete
@app.route('/sendWordCloud', methods=['POST', 'GET'])
def sendWordCloud():
    print("inside sendWordCloud")
    beavis = requests.post('http://127.0.0.1:5000/static/wordCloud.png')
    print(beavis)
    file_content = beavis.request
    print(file_content)
    return render_template(file_content)

#this doesn't work probably delete
@app.route('/sendWordCloud2', methods=['POST', 'GET'])
def sendWordCloud2():
    print("inside sendWordCloud")

    image_file_descriptor = open('static/wordCloud.png', 'rb')
    # Requests makes it simple to upload Multipart-encoded files
    files = {'media': image_file_descriptor}
    url = 'http://127.0.0.1:5000/static/wordCloud.png'
    beavis = requests.post(url, files=files)
    image_file_descriptor.close()
    return (beavis)

#old app run - doesn't work now- need to base it on threading environment
#if __name__ == '__main__':
#   app.run()

@app.route("/")
def main():
    return data

if __name__ == "__main__":
    threading.Thread(target=app.run).start()