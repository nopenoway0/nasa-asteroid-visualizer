import os
import sys
sys.path.append('static/')
from flask import Flask, url_for, render_template, redirect
from NASAObjects import NasaMeteor
import json

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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

    return app