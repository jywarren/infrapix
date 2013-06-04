infrapix
==================

flask app for developing infragram photos!

try it out at infrapix.pvos.org (location subject to change very soon!) ...


### GNU License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

infrapix-mov
============

The included script, "processNGB.py", will take one or more NGB images from a user-specified input directory and generate NDVI imagery in the user-specified output directory.

Note, if you'd like to process NGB files instead, you can comment out the line that reads: 

```
imgR, imgB, imgG = img.split() #get channels from NGB
```

and uncomment the line that reads:

```
imgR, imgG, imgB = img.split() #get channels from NBG
```

## Usage

You can run the python script to convert NGB or NBG images in a specified input directory to NDVI in a specified output directory by invoking it on the command line. 

```
python processNGB.py inputdir outputdir vmin vmax histogramOption
```

- INPUTDIR: the input directory of images -- only the images you want to process.

- OUTPUTDIR: where you'd like the output images.

- VMIN, VMAX: the min/max values to display in the colormap of the NDVI output. 
 
- histogramOption:  1=show, 0=don't show histograms of R, B, and NDVI overlaid on the result image.  For example,

``` 
python processNGB.py ../infpx-mov/vidfolder/ ./out6/ .1 .8 1
```

has VMIN=.1, VMAX=.8, and includes the histogram option.


## Processing a video file

In order to process video files, first, extract all the video frames and place them into a folder:

``` 
ffmpeg -i inputMovie.avi  -f image2 ./vidImages/image-%04d.png
```

Then, run the python script as above to convert all of the images in the resultant output folder to NDVI.  In the above example, we might run:

```
python processNGB.py ../vidImages/ ./NDVIOut/ .1 .8 1
```

Finally, recombine the extracted frames into a movie:

``` 
ffmpeg -qscale 5 -i ./NDVIOut/ndvi_image-%04d.png movie.mp4
```
