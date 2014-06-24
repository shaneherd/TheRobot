following = true;
numRecords = 0
while (numRecords == 0):
  #count num records in database
  print 'check num records'
  numRecords = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT COUNT(*) from gps";').read()  
  
while (following):
  #destination = first record in databasedslkj
  gpsMinId = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT min(gpsID) FROM gps ";').read()
  destinationLong = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT longitude FROM gps WHERE gpsID=\'' + str(gpsMinId) + '\'";').read()
  destinationLat = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT latitude FROM gps WHERE gpsID=\'' + str(gpsMinId) + '\'";').read()
  
  #calculate direction to destination
  #turn towards destination
  
  #initialize variables
  moving = false
  destinationReached = false
  distanceToPlayer = distance(43.816142300, -111.784585100, float(sys.argv[1]), float(sys.argv[2]))
  
  #currently facing the right direction to go forwards toward destination 
  while (distanceToPlayer > 3 and (not destinationReached) and following):
    if (not moving):
      os.system('python /home/pi/motor.py f 1 &')
      moving = true
    
	#get the players position
    gpsMaxId = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT max(gpsID) FROM gps ";').read()
    playerLong = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT longitude FROM gps WHERE gpsID=\'' + str(gpsMaxId) + '\'";').read()
    playerLat = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT latitude FROM gps WHERE gpsID=\'' + str(gpsMaxId) + '\'";').read()
    
	#get the carts position
    cartLat = '43.816142300'
    cartLong = '-111.784585100'
	
	#calculate distance to player
    distanceToPlayer = distance(cartLat, cartLong, playerLat, playerLong)
	
	#calculate distance to destination
    distanceToDestination = distance(destinationLat, destinationLong, cartLat, cartLong)
	
	#if within 1 meter of destination
    if (distanceToDestination < 1):
      destinationReached = true
	  
	#update following status
    following = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT pinStatus FROM pinstatus WHERE pinNumber=''5''";').read()  
  
  os.system('python /home/pi/motor.py f 0 &')
  moving = false
  
  if ((not destinationReached) and following): #within distance to the player
    while ((distanceToPlayer <= 3) and following):
      #get the players position
      gpsMaxId = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT max(gpsID) FROM gps ";').read()
      playerLong = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT longitude FROM gps WHERE gpsID=\'' + str(gpsMaxId) + '\'";').read()
      playerLat = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e \"SELECT latitude FROM gps WHERE gpsID=\'' + str(gpsMaxId) + '\'";').read()
      distanceToPlayer = distance(playerLat, playerLong, cartLat, cartLong);
      
      #update following
      following = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT pinStatus FROM pinstatus WHERE pinNumber=''5''";').read()  
    #delete all records in database except last one
    os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "DELETE FROM gps where gpsID NOT IN ( SELECT * FROM (SELECT MAX(gpsID) FROM gps) AS X)";').read()  	
	
  if (destinationReached and following):
    #delete first record in database
    print 'delete first record'
    os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "DELETE FROM gps where gpsID IN ( SELECT * FROM (SELECT MIN(gpsID) FROM gps) AS X)";').read()  

#delete all records in the database
os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "DELETE FROM gps";').read()