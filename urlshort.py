from flask import Flask,render_template,request,redirect,url_for,flash,abort,session,jsonify,Blueprint
import json
import os.path
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'vbbvjbfjvbjgbsjbgfj24'
bp = Blueprint('urlshort',__name__)
@bp.route('/')

def home():
    return render_template('home.html',codes=session.keys())

@bp.route('/your-url',methods=['GET','POST'])

def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('That short name has already been taken')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            file_name = request.form['code'] + secure_filename(f.filename)
            f.save('/Users/anike/Desktop/url-shortener-project/urlshort/static/userfiles/' + file_name)
            urls[request.form['code']] = {'file':file_name}


        with open('urls.json','w') as url_files:
            json.dump(urls,url_files)
            session[request.form['code']] = True
        return render_template('your_url.html',code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))


@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as u_f:
            urls = json.load(u_f)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static',filename='userfiles/' + urls[code]['file']))
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))

@bp.route('/del1')
def del1():
    if 'ut' in session:
        session.pop('ut',None)
    return redirect(url_for('urlshort.home'))
