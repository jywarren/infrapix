
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from app import app
import os
from flask import Flask, render_template, send_from_directory, send_file, request, url_for, jsonify, redirect, Request, g

from cStringIO import StringIO
from werkzeug import secure_filename

import matplotlib
matplotlib.use('Agg')
#import numpy
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as numpy

from PIL import Image
import gc

### in order to handle odd filenames
# see online material here: http://flask.pocoo.org/snippets/5/

#UPLOAD_FOLDER = '/home/asine/infrapix.pvos.org/app/uploads'
#NDVI_FOLDER = '/home/asine/infrapix.pvos.org/app/ndvi'

UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
NDVI_FOLDER = os.path.join(app.root_path, 'ndvi')


#UPLOAD_FOLDER = '/home/asine/infrapix.pvos.org/public/uploads'
#NDVI_FOLDER = '/home/asine/infrapix.pvos.org/public/ndvi'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','PNG','JPEG'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['NDVI_FOLDER'] = NDVI_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

### generating ndvi

"""
def nir(imageInPath,imageOutPath):
    img = mpimg.imread(imageInPath)
    red=img[:,:,0]
    arrR=numpy.asarray(red).astype('float64')
   
    arr_nir=arrR

    fig=plt.figure()
    fig.set_frameon(False)
    ax=fig.add_subplot(111)
    ax.set_axis_off()
    ax.patch.set_alpha(0.0)

    nir_plot = ax.imshow(arr_nir, cmap=plt.cm.gist_gray, interpolation="nearest")

    #fig.colorbar(nir_plot)
    fig.savefig(imageOutPath)
"""

def nir(imageInPath,imageOutPath):
	img=Image.open(imageInPath)
	imgR, imgG, imgB = img.split() #get channels
	arrR = numpy.asarray(imgR).astype('float64')

	arr_nir=arrR

	img_w,img_h=img.size

	dpi=600. #need this to be floating point!
	fig_w=img_w/dpi
	fig_h=img_h/dpi

	fig=plt.figure(figsize=(fig_w,fig_h),dpi=dpi)

	fig.set_frameon(False)

	ax_rect = [0.0, #left
	       0.0, #bottom
	       1.0, #width
	       1.0] #height
	ax = fig.add_axes(ax_rect)
	ax.yaxis.set_ticklabels([])
	ax.xaxis.set_ticklabels([])   
	ax.set_axis_off()
	ax.axes.get_yaxis().set_visible(False)
	ax.patch.set_alpha(0.0)

	axes_img = ax.imshow(arr_nir,
			  cmap=plt.cm.gist_gray,
			  aspect = 'equal',
			  interpolation="nearest"
			 )

	fig.savefig(imageOutPath, 
		    dpi=dpi,
		    bbox_inches='tight',
		    pad_inches=0.0, 
		   )

	#plt.show()  #show the plot after saving
	fig.clf()
	plt.close()
	gc.collect()



def ndvi(imageInPath,imageOutPath):
	img=Image.open(imageInPath)
	imgR, imgG, imgB = img.split() #get channels
	arrR = numpy.asarray(imgR).astype('float64')
	arrB = numpy.asarray(imgB).astype('float64')
	"""img = mpimg.imread(imageInPath)
	red=img[:,:,0]
	green=img[:,:,1]
	blue=img[:,:,2]

	arrR=np.asarray(red).astype('float64')
	arrG=np.asarray(green).astype('float64')
	arrB=np.asarray(blue).astype('float64')
	"""
	num=arrR - arrB
	num=(arrR - arrB)
	denom=(arrR + arrB)
	arr_ndvi=num/denom

	vmin=-1.
	vmax = 1.

	img_w,img_h=img.size

	dpi=600. #need this to be floating point!
	fig_w=img_w/dpi
	fig_h=img_h/dpi

	fig=plt.figure(figsize=(fig_w,fig_h),dpi=dpi)

	fig.set_frameon(False)

	ax_rect = [0.0, #left
	       0.0, #bottom
	       1.0, #width
	       1.0] #height
	ax = fig.add_axes(ax_rect)
	ax.yaxis.set_ticklabels([])
	ax.xaxis.set_ticklabels([])   
	ax.set_axis_off()
	ax.axes.get_yaxis().set_visible(False)
	ax.patch.set_alpha(0.0)


	"""
	axes_img = ax.imshow(arr_ndvi,
	cmap=plt.cm.spectral, 
	vmin = vmin,
	vmax = vmax,
	aspect = 'equal',
	interpolation="nearest"
	)
	"""

	axes_img = ax.imshow(arr_ndvi,
			  cmap=plt.cm.spectral, 
			  aspect = 'equal',
			  interpolation="nearest"
			 )

	# Add colorbar 
	#make an axis for colorbar
	cax = fig.add_axes([0.8,0.05,0.05,0.85]) #left, bottom, width, height
	cbar = fig.colorbar(axes_img, cax=cax)  #this resizes the axis
	cbar.ax.tick_params(labelsize=2) #this changes the font size on the axis

	#position of the colorbar
	#cbar.ax.yaxis.set_ticks_position('left')

	#color of the colorbar text
	#cbytick_obj = plt.getp(cbar.ax.axes, 'yticklabels')                #tricky
	#plt.setp(cbytick_obj, color='r')


	fig.savefig(imageOutPath, 
		    dpi=dpi,
		    bbox_inches='tight',
		    pad_inches=0.0, 
		   )

	#plt.show()  #show the plot after saving
	fig.clf()
	plt.close()
	gc.collect()



"""
	if histogramOption==1:

	#plot the Red histogram
	x=arrR.ravel()
	a = plt.axes([.05,.7,.18,.18], axisbg='y')
	bins=numpy.arange(0,255,8)
	n, bins, patches = plt.hist(x, bins, normed=1,linewidth=.2)
	plt.setp(patches, 'facecolor', 'r', 'alpha', 0.75)
	plt.setp(a,xticks=[0,120,255],yticks=[])
	plt.setp(a,xticks=[],yticks=[])
	plt.xticks(fontsize=2)

	#plot the Blue histogram
	x=arrB.ravel()
	a = plt.axes([.05,.4,.18,.18], axisbg='y')
	bins=numpy.arange(0,255,8)
	n, bins, patches = plt.hist(x, bins, normed=1,linewidth=.2)
	plt.setp(patches, 'facecolor', 'b', 'alpha', 0.75)
	plt.setp(a,xticks=[0,120,255],yticks=[])
	plt.setp(a,xticks=[],yticks=[])
	plt.xticks(fontsize=2)

	#plot the NDVI histogram
	x=arr_ndvi.ravel()
	a = plt.axes([.05,.1,.18,.18], axisbg='y')
	bins=numpy.arange(-1,1,.01)
	n, bins, patches = plt.hist(x, bins, normed=1,linewidth=.2)
	plt.setp(patches, 'facecolor', 'w', 'alpha', 0.75)
	plt.setp(a,xticks=[-1,0,1],yticks=[])
	plt.setp(a,xticks=[],yticks=[])
	plt.xticks(fontsize=2)
"""






"""

	fig=plt.figure()
	fig.set_frameon(False)
	ax=fig.add_subplot(111)
	ax.set_axis_off()
	ax.patch.set_alpha(0.0)

	#custom_cmap=make_cmap_gaussianHSV(bandwidth=0.01,num_segs=1024)
	ndvi_plot = ax.imshow(arr_ndvi, cmap=plt.cm.spectral, interpolation="nearest")
	#ndvi_plot = ax.imshow(arr_ndvi, cmap=custom_cmap, interpolation="nearest")

	fig.colorbar(ndvi_plot)
	fig.savefig(imageOutPath)
"""








def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method=='POST':
		file=request.files['file']
		if file and allowed_file(file.filename):
			filename=secure_filename(file.filename)
			#filename=slugify(filename)
			uploadFilePath=os.path.join(app.config['UPLOAD_FOLDER'],filename)
			file.save(uploadFilePath)
			ndviFilePath=os.path.join(app.config['UPLOAD_FOLDER'],'ndvi_'+filename)
			nirFilePath=os.path.join(app.config['UPLOAD_FOLDER'],'nir_'+filename)
			ndvi(uploadFilePath,ndviFilePath)
			nir(uploadFilePath,nirFilePath)
			return redirect(url_for('uploaded_file',filename=filename)) 
	return '''
		<!doctype html>
	<head>
	<title>infrapix!</title>
	<link type="text/css" rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap/css/bootstrap.css') }}" />
	<link type="text/css" rel="stylesheet" href="{{ url_for('static', filename='css/slider.css') }}" />
	</head>
	<body class="container">


		<img src="http://i.publiclab.org/system/images/photos/000/000/264/medium/main-image-med.jpg"><br>
		<title>Infragram Online!</title>
	<br>
	Welcome to Public Lab's online service for generating NDVI from near-infrared pictures!</br><br>

	<div class="well">
		<h2>Upload a new file</h2>

	To upload a file for processing, please click on the "Choose File" button below.  After you've selected a file, click "Upload".

		<form action="" method=post enctype=multipart/form-data>
		  <p><input type=file name=file>
		         <input type=submit value=Upload>
		</form>
	</div>
	</body>
	</html>

		'''

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)


@app.route('/show/<filename>')
def uploaded_file(filename):
    uploadFilePath=os.path.join(app.config['UPLOAD_FOLDER'],filename)
    ndviFilePath=os.path.join(app.config['NDVI_FOLDER'],filename)  
    return render_template('vanilla.html',filename='/uploads/'+filename, ndviFilename='/uploads/'+'ndvi_'+filename, nirFilename='/uploads/'+'nir_'+filename)




