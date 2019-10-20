from flask import Flask, request, render_template, redirect, url_for, flash
from google.cloud import datastore

app = Flask(__name__)
app.secret_key = 'super secret kitty'
datastore_client = datastore.Client()


def add_star(star_data):

    star_key = datastore_client.key('STAR')

    star = datastore.Entity(key=star_key)
    star.update({
        'question': star_data['question'],
        'situation': star_data['situation'],
        'task': star_data['task'],
        'action': star_data['action'],
        'result': star_data['result'],
        'module': star_data['module']
    })

    datastore_client.put(star)

    # print(datastore_client.get(star_key))



@app.route('/', methods=['get'])
def intro_page():
    return render_template('page1.html')

@app.route('/formpage', methods=['get', 'post'])
def get_stardata():

    if request.method == 'POST':
        star_data = {}
        star_data['question'] = request.form.get('question')
        star_data['situation'] = request.form.get('situation')
        star_data['task'] = request.form.get('task')
        star_data['action'] = request.form.get('action')
        star_data['result'] = request.form.get('result')
        star_data['module'] = request.form.get('module')

        add_star(star_data)
        return render_template('page1.html')

    return render_template('getstar.html')

@app.route('/starinfo', methods=['get', 'post'])
def star_info():
    stars = []
    details = {}
    query = datastore_client.query(kind="STAR")
    stars_entities=list(query.fetch())

    for s in stars_entities:
        stars.append(s['question'])

    if request.method == 'POST':
        q = request.form['details']
        print("the quetion is:{}".format(q))
        for s in stars_entities:
            if str(s['question']) == str(q):
                details['question'] = s['question']
                details['situation'] = s['situation']
                details['task'] = s['task']
                details['action'] = s['action']
                details['result'] = s['result']
                details['module'] = s['module']

        return render_template('star_details.html', details=details)

    return render_template('starsinfo.html', stars=stars)



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=9090, debug=True)

