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
 
def getInitialBearing():
    initialBearing = 0.0
    
    #get the initial cart position
    cartLatInitial = '43.816142300' #gpsd.fix.latitude
    cartLongInitial = '-111.784585100' #gpsd.fix.longitude
    
    os.system('python /home/pi/motor.py f 1 &')
    time.sleep(2.5)  #drive forward for 1 meter
    os.system('python /home/pi/motor.py f 0 &')
    
    #get the carts position
    cartLat = '43.816142399' #gpsd.fix.latitude
    cartLong = '-111.784585100' #gpsd.fix.longitude

    # convert to radians:
    g2r = pi/180
    lat1r = float(cartLatInitial) * g2r
    lat2r = float(cartLat) * g2r
    lon1r = float(cartLongInitial) * g2r
    lon2r = float(cartLong) * g2r
    dlonr = lon2r - lon1r
    y = sin(dlonr) * cos(lat2r)
    x = cos(lat1r) * sin(lat2r) - sin(lat1r) * cos(lat2r) * cos(dlonr)

    # compute bearning and convert back to degrees:
    initialBearing = atan2(y, x) / g2r

    #if initialBearing < 0:
      #initialBearing = initialBearing + 360

    print 'Bearing: ' + str(initialBearing)
    
    return initialBearing 
 
def getCurrentBearing(latCurrent, longCurrent, latDest, longDest):
    currentBearing = 0.0
    
    # convert to radians:
    g2r = pi/180
    lat1r = float(latCurrent) * g2r
    lat2r = float(latDest) * g2r
    lon1r = float(longCurrent) * g2r
    lon2r = float(longDest) * g2r
    dlonr = lon2r - lon1r
    y = sin(dlonr) * cos(lat2r)
    x = cos(lat1r) * sin(lat2r) - sin(lat1r) * cos(lat2r) * cos(dlonr)

    # compute bearning and convert back to degrees:
    currentBearing = atan2(y, x) / g2r

    #if currentBearing < 0:
      #currentBearing = currentBearing + 360

    print 'Bearing: ' + str(currentBearing)
    
    return currentBearing
 
def turnTowardDestination(bearingToTurn):
    degreesToTurn = abs(bearingToTurn)
    if degreesToTurn > 180:
        degreesToTurn = degreesToTurn - 180
    sleeptime = degreesToTurn/280
    if ((bearingToTurn > 0 and bearingToTurn <= 180) or (bearingToTurn > -360 and bearingToTurn <= -180)):
        #turn right
        print "turn right"
        os.system('python /home/pi/motor.py r 1 &')
        time.sleep(sleeptime)
        os.system('python /home/pi/motor.py r 0 &')
    elif ((bearingToTurn < 0 and bearingToTurn > -180) or (bearingToTurn > 180 and bearingToTurn < 360)):
        #turn left
        print "turn left"
        os.system('python /home/pi/motor.py l 1 &')
        time.sleep(sleeptime)
        os.system('python /home/pi/motor.py l 0 &')
 
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
    
    #get the initial bearing by moving forward one meter
    currentBearing = getInitialBearing()
    
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
    
      #get the carts position
      cartLat = '43.816142300' #gpsd.fix.latitude
      cartLong = '-111.784585100' #gpsd.fix.longitude
    
      #calculate direction to destination
      bearingToDestination = getBearing(cartLat, cartLong, destinationLat, destinationLong)

      #determine how far to turn and in what direction
      bearingToTurn = bearingToDestination - currentBearing
      
      #turn towards destination
      turnTowardDestination(bearingToTurn)
      currentBearing = bearingToDestination
    
      #initialize variables
      moving = False
      destinationReached = False
    
      #get the players position
      gpsMaxId = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT max(gpsID) FROM gps ";').read()
      playerLong = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT longitude FROM gps WHERE gpsID=\'' + str(gpsMaxId) + '\'";').read()
      playerLat = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT latitude FROM gps WHERE gpsID=\'' + str(gpsMaxId) + '\'";').read()
      
      #get the distance to the player
      distanceToPlayer = distance(float(cartLat), float(cartLong), float(playerLat), float(playerLong))
      print 'distanceToPlayer = ' , distanceToPlayer
      
      #store previous position in order to keep track of bearing
      previousCartLat = cartLat
      previousCartLong = cartLong
    
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
        
        #update current bearing to ensure that we are still on course to destination
        if ((previousCartLat != cartLat) and (previousCartLong != cartLong)):
            currentBearing = getBearing(previousCartLat, previousCartLong, cartLat, cartLong)
        bearingToDestination = getBearing(cartLat, cartLong, destinationLat, destinationLong)
        bearingToTurn = bearingToDestination - currentBearing
        if (bearingToTurn != 0):
            #correct the direction to be heading straight for goal
            print "correcting direction"
            
            #stop moving forward so that we can perform the turn
            os.system('python /home/pi/motor.py f 0 &')
            #turn towards destination
            turnTowardDestination(bearingToDestination)
            currentBearing = bearingToDestination
            
            #update cart position
            cartLat = '43.816142300' #gpsd.fix.latitude
            cartLong = '-111.784585100' #gpsd.fix.longitude
            
            #resume moving forward
            os.system('python /home/pi/motor.py f 1 &')
            
        #update previous position to current position
        previousCartLat = cartLat
        previousCartLong = cartLong
    
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
        if (int(following) == 1):
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