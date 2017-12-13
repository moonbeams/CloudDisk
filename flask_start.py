# -*- coding: utf-8 -*-
import os

from flask import Flask, render_template

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class, ALL
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'


#app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()
Dest = '/Users/zhaoleiwang/PycharmProjects/CloudDisk/myfile'
#app.config['UPLOADED_PHOTOS_DEST'] = Dest
app.config['UPLOADS_DEFAULT_DEST'] = Dest

#photos = UploadSet('photos', IMAGES)
files = UploadSet('files',ALL)
configure_uploads(app, files)
patch_request_class(app,100 *1024 * 1024)  # set maximum file size, default is 16MB


class UploadForm(FlaskForm):
    file = FileField(validators=[
        FileAllowed(files, u'！'),
        FileRequired(u'文件未选择！')])
    submit = SubmitField(u'上传')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = files.save(form.file.data)
        file_url = files.url(filename)
    else:
        file_url = None
    return render_template('upload.html', form=form, file_url=file_url)


if __name__ == '__main__':
    app.run()