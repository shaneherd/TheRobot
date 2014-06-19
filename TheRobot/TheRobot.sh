mysqlusername="shane"
mysqlpassword="password"

#Set  Refresh
#echo "How long do you want the wait time to be?          "
#read waitTime
waitTime="1"

#Invoke GPIO
echo "1" > /sys/class/gpio/export
echo "2" > /sys/class/gpio/export
echo "3" > /sys/class/gpio/export
echo "4" > /sys/class/gpio/export
echo "5" > /sys/class/gpio/export

#Start Loop
while :
do
#Read MySQL Data
#Direction
direction1="out"
direction2="out"
direction3="out"
direction4="out"
directionFollow="out"

#Status
status1=$(mysql -B --disable-column-names --user=$mysqlusername --password=$mysqlpassword webservice -e "SELECT pinStatus FROM pinstatus WHERE pinNumber='1'";)
status2=$(mysql -B --disable-column-names --user=$mysqlusername --password=$mysqlpassword webservice -e "SELECT pinStatus FROM pinstatus WHERE pinNumber='2'";)
status3=$(mysql -B --disable-column-names --user=$mysqlusername --password=$mysqlpassword webservice -e "SELECT pinStatus FROM pinstatus WHERE pinNumber='3'";)
status4=$(mysql -B --disable-column-names --user=$mysqlusername --password=$mysqlpassword webservice -e "SELECT pinStatus FROM pinstatus WHERE pinNumber='4'";)
statusFollow=$(mysql -B --disable-column-names --user=$mysqlusername --password=$mysqlpassword webservice -e "SELECT pinStatus FROM pinstatus WHERE pinNumber='5'";)

gpsMaxId=$(mysql -B --disable-column-names --user=$mysqlusername --password=$mysqlpassword webservice -e "SELECT max(gpsID) FROM gps ";)
gpsLong=$(mysql -B --disable-column-names --user=$mysqlusername --password=$mysqlpassword webservice -e "SELECT longitude FROM gps WHERE gpsID='$gpsMaxId'";)
gpsLat=$(mysql -B --disable-column-names --user=$mysqlusername --password=$mysqlpassword webservice -e "SELECT latitude FROM gps WHERE gpsID='$gpsMaxId'";)

#Run Commands
if [ "$direction1" == "out" ]; then
	echo "out" > /sys/class/gpio/gpio1/direction
	if [ "$status1" == "1" ]; then
		python /home/pi/motor.py f 1 &
		echo "1" > /sys/class/gpio/gpio1/value
		echo "GPIO 1 Turned On  (Forward)"
	else
		echo "0" > /sys/class/gpio/gpio1/value
		echo "GPIO 1 Turned Off (Forward)"
	fi
else
	echo "in" > /sys/class/gpio/gpio1/direction
fi
if [ "$direction2" == "out" ]; then
        echo "out" > /sys/class/gpio/gpio2/direction
	if [ "$status2" == "1" ]; then
				python /home/pi/motor.py l 1 &
                echo "1" > /sys/class/gpio/gpio2/value
                echo "GPIO 2 Turned On  (Left)"
        else
                echo "0" > /sys/class/gpio/gpio2/value
                echo "GPIO 2 Turned Off (Left)"
        fi
else
        echo "in" > /sys/class/gpio/gpio2/direction
fi
if [ "$direction3" == "out" ]; then
        echo "out" > /sys/class/gpio/gpio3/direction
	if [ "$status3" == "1" ]; then
				python /home/pi/motor.py r 1 &
                echo "1" > /sys/class/gpio/gpio3/value
                echo "GPIO 3 Turned On  (Right)"
        else
                echo "0" > /sys/class/gpio/gpio3/value
                echo "GPIO 3 Turned Off (Right)"
        fi
else
        echo "in" > /sys/class/gpio/gpio3/direction
fi
if [ "$direction4" == "out" ]; then
        echo "out" > /sys/class/gpio/gpio4/direction
	if [ "$status4" == "1" ]; then
				python /home/pi/motor.py b 1 &
                echo "1" > /sys/class/gpio/gpio4/value
                echo "GPIO 4 Turned On  (Back)"
        else
                echo "0" > /sys/class/gpio/gpio4/value
                echo "GPIO 4 Turned Off (Back)"
        fi
else
        echo "in" > /sys/class/gpio/gpio4/direction
fi
if [ "$directionFollow" == "out" ]; then
	echo "out" > /sys/class/gpio/gpio5/direction
	if [ "$statusFollow" == "1" ]; then
		echo "1" > /sys/class/gpio/gpio5/value
		echo "GPIO 5 Turned On  (Follow)"
		echo $gpsMaxId
		echo $gpsLong
		echo $gpsLat
		
		python /home/pi/GPSpython.py $gpsLat $gpsLong
	else
		echo "0" > /sys/class/gpio/gpio5/value
		echo "GPIO 5 Turned Off (Follow)"
	fi
else
	echo "in" > /sys/class/gpio/gpio5/direction
fi
#Complete Loop
sleep $waitTime
done
