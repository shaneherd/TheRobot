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
  try:
    gpsp.start() # start it up
    #if it needs a couple of seconds for good data
    time.sleep(2) 
    
    #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc

    os.system('clear')
    #d = distance(gpsd.fix.latitude, gpsd.fix.longitude, sys.argv[1], sys.argv[2])
    #d = distance(43.816142300, -111.784585100, 43.816136700, -111.784569000)
    #d = distance(43.816142300, -111.784585100, float(sys.argv[1]), float(sys.argv[2]))
    #f = 'f'
    #os.system('python /home/pi/motortwo.py '+ f + ' ' + str(d) + ' &')
    #if d > 1:
    #  print 'distance ' , d
    #else:
    #  print 'in range'
  
    following = 1;
    numRecords = 0
    while (int(numRecords) == 0):
      #count num records in database
      print 'check num records'
      numRecords = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT COUNT(*) from gps";').read()  
      print 'numRecords = ' , numRecords
    
    while (int(following) == 1):
      print 'following'
      
      #destination = first record in databasedslkj
      gpsMinId = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT min(gpsID) FROM gps ";').read()
      destinationLong = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT longitude FROM gps WHERE gpsID=\'' + str(gpsMinId) + '\'";').read()
      destinationLat = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT latitude FROM gps WHERE gpsID=\'' + str(gpsMinId) + '\'";').read()
    
      #calculate direction to destination
      #turn towards destination
    
      #initialize variables
      moving = False
      destinationReached = False
    
      #get the carts position
      cartLat = '43.816142300' #gpsd.fix.latitude
      cartLong = '-111.784585100' #gpsd.fix.longitude
    
      #get the players position
      gpsMaxId = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT max(gpsID) FROM gps ";').read()
      playerLong = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT longitude FROM gps WHERE gpsID=\'' + str(gpsMaxId) + '\'";').read()
      playerLat = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT latitude FROM gps WHERE gpsID=\'' + str(gpsMaxId) + '\'";').read()
      
      distanceToPlayer = distance(float(cartLat), float(cartLong), float(playerLat), float(playerLong))
      print 'distanceToPlayer = ' , distanceToPlayer
    
      #currently facing the right direction to go forwards toward destination 
      while (distanceToPlayer > 3 and (not destinationReached) and (int(following) == 1)):
        if (not moving):
          os.system('python /home/pi/motor.py f 1 &')
          moving = True
          print 'moving'
    
        #get the players position
        gpsMaxId = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT max(gpsID) FROM gps ";').read()
        playerLong = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT longitude FROM gps WHERE gpsID=\'' + str(gpsMaxId) + '\'";').read()
        playerLat = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT latitude FROM gps WHERE gpsID=\'' + str(gpsMaxId) + '\'";').read()
    
        #get the carts position
        cartLat = '43.816142300' #gpsd.fix.latitude
        cartLong = '-111.784585100' #gpsd.fix.longitude
    
        #calculate distance to player
        distanceToPlayer = distance(float(cartLat), float(cartLong), float(playerLat), float(playerLong))
        print 'distanceToPlayer = ' , distanceToPlayer
      
        #calculate distance to destination
        distanceToDestination = distance(float(destinationLat), float(destinationLong), float(cartLat), float(cartLong))
        print 'distanceToDestination' , distanceToDestination
      
        #if within 1 meter of destination
        if (distanceToDestination < 1):
          destinationReached = True
          print 'destination reached'
      
        #update following status
        following = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT pinStatus FROM pinstatus WHERE pinNumber=''5''";').read()  
    
      os.system('python /home/pi/motor.py f 0 &')
      moving = False
      print 'stopping'
  
      if ((not destinationReached) and int(following) == 1): #within distance to the player
        print 'within distance of player'
        while ((distanceToPlayer <= 3) and int(following) == 1):
          #get the players position
          gpsMaxId = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT max(gpsID) FROM gps ";').read()
          playerLong = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT longitude FROM gps WHERE gpsID=\'' + str(gpsMaxId) + '\'";').read()
          playerLat = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT latitude FROM gps WHERE gpsID=\'' + str(gpsMaxId) + '\'";').read()
        
          #get the carts position
          cartLat = '43.816142300' #gpsd.fix.latitude
          cartLong = '-111.784585100' #gpsd.fix.longitude
        
          #calculate the distance to the player
          distanceToPlayer = distance(float(playerLat), float(playerLong), float(cartLat), float(cartLong))
          print 'distanceToPlayer = ' , distanceToPlayer
          
          #update following
          following = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT pinStatus FROM pinstatus WHERE pinNumber=''5''";').read() 
          print 'following = ' , following 
        #delete all records in database except last one
        print 'deleting all records in database except last one'
        os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "DELETE FROM gps where gpsID NOT IN ( SELECT * FROM (SELECT MAX(gpsID) FROM gps) AS X)";').read()      
    
      if (destinationReached and int(following) == 1):
        print 'destination reached'
        #delete first record in database
        print 'deleting first record'
        os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "DELETE FROM gps where gpsID IN ( SELECT * FROM (SELECT MIN(gpsID) FROM gps) AS X)";').read()  

    #delete all records in the database
    print 'deleting all records'
    os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "DELETE FROM gps";').read()
  
    #kill the thread
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c (catch statement)
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."