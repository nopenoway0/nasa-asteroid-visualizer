import os
import sys
sys.path.append('static/')
from flask import Flask, url_for, render_template, redirect
from NASAObjects import NasaMeteor
import json

# start app
if __name__ =='__main__':
    app = Flask(__name__)
    # a simple page that says hello
    @app.route('/')
    def get_visualizer():
        texture_locations = {}
        for planet in ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']:
            texture_locations[planet] = url_for('static', filename=planet + '.jpg')
        print(url_for('static', filename='sun.jpg'))
        meteors = []
        with open('static/example_response.json', 'r') as f:
            txt = json.load(f)
            for meteor in txt['near_earth_objects']:
                try:
                    meteor = NasaMeteor(json=meteor)
                    meteors.append(meteor.serialize())
                except:
                    pass#print('error with meteor: ' + str(meteor))
        return render_template('meteor_template.html', meteors=meteors, texture_locations=texture_locations)
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))

