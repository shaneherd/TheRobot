following = true;
numRecords = 0
while (numRecords == 0):
  #count num records in database
  print 'check num records'

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
  
  if ((not destinationReached) and following): #within distance to the player
    while ((distanceToPlayer <= 3) and following):
      distanceToPlayer = distance(playerLat, playerLong, cartLat, cartLong);
      following = os.popen('mysql -B --disable-column-names --user=shane --password=password webservice -e "SELECT pinStatus FROM pinstatus WHERE pinNumber=''5''";').read()  
  
#delete all records in database except last one
		
	
if (destinationReached):
  #delete first record in database
  print 'delete first record'

#delete all records in the database
