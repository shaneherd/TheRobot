TheRobot
========
TheRobot.sh is ran by using the following command on the command line:
    sudo -i ./TheRobot.sh

This script checks a MySQL database as to whether or not pins 1 through 5 are high. The pins correspond to what action to take.
    Pin 1: Forward
    Pin 2: Left
    Pin 3: Right
    Pin 4: Backwards
    Pin 5: Follow
    
You can set this script to run on start up by adding the above command to the following file:
    
    
The motor.py script can be ran by using the following commands on the command line:
    python motor.py direction action &

The following options are available for direction:
    f
    l
    r
    b

The following options are available for action:
    1: turn on
    0: turn off

Adding the '&' runs the script on a seperate thread.

The GPSPythoon.py script can be ran using the following command on the command line:
    python GPSPython.py latitude longitude
    
This script gets the carts initial bearing, calculates which direction to turn to go towards the destination, turns
towards the destination, and then starts moving forward. It continually checks to make sure that is hasn't deviated from
its course and whether or not it is within range of the player. If it gets within range of the player, it stops moving and 
waits until the player has moved away. It then recalculates the direction to the player's new location and repeats the 
above steps.
