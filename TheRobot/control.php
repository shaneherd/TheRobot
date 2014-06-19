<?php

//load and connect to MySQL database stuff
require("config.inc.php");

if (!empty($_POST)) {
	$action = $_POST['action'];
	$pin = $_POST['pin'];
	
	if ($action == "turnOn") {
		$query = "UPDATE pinstatus SET pinStatus=1 WHERE pinNumber='$pin'";
	}
	else {
		$query = "UPDATE pinstatus SET pinStatus=0 WHERE pinNumber='$pin'";
	}
    
    try {
        $stmt   = $db->prepare($query);
        $result = $stmt->execute();
    }
    catch (PDOException $ex) {
        $response["success"] = 0;
        $response["message"] = "Database Error1. Please Try Again!";
        die(json_encode($response));
    }
    
    //This will be the variable to determine whether or not the user's information is correct.
    //we initialize it as false.
    $validated_info = false;
    
	$response["action"] = $action;
	$response["pin"] = $pin;
	die(json_encode($response));
} else {
?>
		<h1>Control</h1> 
		<tr>
		<td align="center">Forward</td>
		<td>pin 1</td>
		<td align="center" valign="middle">
		<form name="pin 1 edit" action="control.php" method="post">
			<input type="hidden" name="action" value="turnOn">
			<input type="hidden" name="pin" value="1">
			<input type="submit" value="turn on">
		</form></td>
		<td>
		</tr>
		
		<tr>
		<td align="center">Left</td>
		<td>pin 2</td>
		<td align="center" valign="middle">
		<form name="pin 2 edit" action="control.php" method="post">
			<input type="hidden" name="action" value="turnOn">
			<input type="hidden" name="pin" value="2">
			<input type="submit" value="turn on">
		</form></td>
		<td>
		</tr>
	<?php
}

?> 
