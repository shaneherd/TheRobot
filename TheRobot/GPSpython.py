import os
from gps import *
from time import *
import time
import threading
import sys
from math import *
 
gpsd = None #seting the global variable

def distance(lat1, lon1, lat2, lon2):

  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * atan2(sqrt(a), sqrt(1-a))
  Base = 6371 * c

  return (Base * 1000)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
	
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  #try:
  gpsp.start() # start it up
  #if it needs a couple of seconds for good data
  time.sleep(2) 
    
  #It may take a second or two to get good data
  #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc

  os.system('clear')
  #d = distance(gpsd.fix.latitude, gpsd.fix.longitude, sys.argv[1], sys.argv[2])
  #d = distance(43.816142300, -111.784585100, 43.816136700, -111.784569000)
  d = distance(43.816142300, -111.784585100, float(sys.argv[1]), float(sys.argv[2]))
  f = 'f'
  os.system('python /home/pi/motortwo.py '+ f + ' ' + str(d) + ' &')
  if d > 1:
    print 'distance ' , d
  else:
    print 'in range'
  
  time.sleep(2) #set to whatever
  gpsp.running = False
  #gpsd.stop()
  #except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
  #  print "\nKilling Thread..."
  #  gpsp.running = False
  #  gpsp.join() # wait for the thread to finish what it's doing
  #print "Done.\nExiting."