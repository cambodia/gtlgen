"""
GTL-Generator
"""

#imports
#from jinja2 import Environment, FileSystemLoader
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'D:\_gtlgen\gtlgen-master\gtlgen\gtlgen\static\upload'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			filename_without_ext = filename.rsplit('.', 1)[0]
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('show', filename_without_ext=filename_without_ext))
	return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/show/<filename_without_ext>')
def show(filename_without_ext):
	csv_name = os.path.join(app.config['UPLOAD_FOLDER'], filename_without_ext) + ".csv"
	xml_name = os.path.join(app.config['UPLOAD_FOLDER'], filename_without_ext) + ".xml"
	del_notes = []
	with open(csv_name, 'r') as csv:
		for row in csv:
			values = row.split(";")
			customer_number = values[3]
			unloading_point = values[4]
			del_note_date = values[5][4:6] + "." + values[5][6:] + "." + values[5][:4]
			delivery_date = del_note_date
			pickup_date = values[100][4:6] + "." + values[100][6:] + "." + values[100][:4]
			del_notes.append([{
					'del_note'			: values[0],
					'del_note_position'	: values[1],
					'mat_number'		: values[7],
					'mat_name'			: values[8],
					'order_number'		: values[9],
					'qty'				: values[10],
					'order_position'	: values[12],
					'version'			: values[19],
					'batch'				: values[13]
				}])
	with open(xml_name, 'w') as xml:
		xml_gen = render_template('main_header.xml', del_notes=del_notes, customer_number=customer_number, unloading_point=unloading_point, del_note_date=del_note_date, delivery_date=delivery_date, pickup_date=pickup_date)
		xml.write(xml_gen.encode('utf8'))
	return render_template('show_del_notes.html', del_notes=del_notes, customer_number=customer_number, unloading_point=unloading_point, del_note_date=del_note_date, delivery_date=delivery_date, pickup_date=pickup_date)

@app.route('/xml_gen')
def xml_gen():
	return render_template('main_header.xml')
