import os
from flask import Flask, render_template
from os.path import join, dirname, realpath

app = Flask(__name__, instance_relative_config=True)
FOLDER_DATABASE= join(os.path.abspath(os.path.dirname(realpath(__file__))), './static/database/')
app.config.from_mapping(
    SECRET_KEY='ipul',
    DATABASE=os.path.join(FOLDER_DATABASE, 'databasenew.db'),
    # DATABASE=os.path.join(FOLDER_DATABASE, 'databaseperpustakaan.db')
)
UPLOAD_FOLDER_MEMBER = join(os.path.abspath(os.path.dirname(realpath(__file__))), './static/csvupload/member/')
UPLOAD_FOLDER_BUKU = join(os.path.abspath(os.path.dirname(realpath(__file__))), './static/csvupload/buku/')
cekfoldermember = os.path.exists(UPLOAD_FOLDER_MEMBER)
cekfolderbuku = os.path.exists(UPLOAD_FOLDER_BUKU)
if not cekfoldermember:
    os.makedirs(UPLOAD_FOLDER_MEMBER)
    print("Folder upload csv member telah dibuat")
elif not cekfolderbuku:
    os.makedirs(UPLOAD_FOLDER_BUKU)
    print("Folder upload csv buku telah dibuat")
app.config['UPLOAD_FOLDER_MEMBER'] = UPLOAD_FOLDER_MEMBER
app.config['UPLOAD_FOLDER_BUKU'] = UPLOAD_FOLDER_BUKU

try:
    # os.makedirs(app.instance_path)
    os.makedirs(FOLDER_DATABASE)
except OSError:
    pass



@app.route('/hello')
def hello():
    return "alahambra"

from . import db
db.init_app(app)
from . import auth
app.register_blueprint(auth.bp)
from . import perpus
app.register_blueprint(perpus.bp)
app.add_url_rule('/', endpoint='index')

# def create_app(test_config=None):
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='ipul',
#         DATABASE=os.path.join(app.instance_path, 'databasenew.db'),
#     )
#     UPLOAD_FOLDER = 'static/files'
#     app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#     if test_config is None:
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         app.config.from_mapping(test_config)

#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass
    
#     app.run(host='127.0.0.1', port=5000, debug=True)

#     @app.route('/hello')
#     def hello():
#         return "alahambra"

#     from . import db
#     db.init_app(app)
#     from . import auth
#     app.register_blueprint(auth.bp)
#     from . import perpus
#     app.register_blueprint(perpus.bp)
#     app.add_url_rule('/', endpoint='index')

#     return app