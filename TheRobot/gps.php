<?php

//load and connect to MySQL database stuff
require("config.inc.php");

if (!empty($_POST)) {
	$longitude = $_POST['longitude'];
	$latitude = $_POST['latitude'];
	
	$query = "INSERT INTO gps (`gpsID`, `longitude`, `latitude`) VALUES (NULL, '$longitude', '$latitude');";
    
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
    
	$response["longitude"] = $longitude;
	$response["latitude"] = $latitude;
	die(json_encode($response));
} else {
?>
		<h1>GPS</h1> 
		<tr>
		<td align="center">Follow Me</td>
		<td>Post GPS</td>
		<td align="center" valign="middle">
		<form name="post gps location" action="gps.php" method="post">
			<input type="hidden" name="longitude" value="-111.80">
			<input type="hidden" name="latitude" value="43.8147305">
			<input type="submit" value="turn on">
		</form></td>
		<td>
		</tr>
	<?php
}

?> 
