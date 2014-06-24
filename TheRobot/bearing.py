import os
import sys
from math import *

if argv[5]:
   currentBearing = float(sys.argv[5])

# bearings
lat1 = float(sys.argv[1])
lat2 = float(sys.argv[3])
lon1 = float(sys.argv[2])
lon2 = float(sys.argv[4])

# convert to radians:
g2r = pi/180
lat1r = lat1 * g2r
lat2r = lat2 * g2r
lon1r = lon1 * g2r
lon2r = lon2 * g2r
dlonr = lon2r - lon1r
y = sin(dlonr) * cos(lat2r)
x = cos(lat1r) * sin(lat2r) - sin(lat1r) * cos(lat2r) * cos(dlonr)

# compute bearning and convert back to degrees:
bearing = atan2(y, x) / g2r

if bearing < 0:
   bearing = bearing + 360

print 'Bearing: ' + str(bearing)

# fprintf(1,'x: %+.3e\ny: %+.3e\nbearing: %.3f\n', x, y, bearing)

if sys.argv[5]:
   if not (currentBearing == bearing):
      currentBearing = bearing   
else:
   currentBearing = bearing

# os.system('blah ' + currentBearing.toString())