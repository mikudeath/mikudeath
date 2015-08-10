<?php

include_once 'handler.php';
$dateTime = date("m.d.Y - H:i:s");
$browser = $_SERVER['HTTP_USER_AGENT'];
$ip = $_SERVER['REMOTE_ADDR'];
if($user){
    $username = $user['username'];
}
else{
    $username = "guest";
}
mysql_query("INSERT INTO `log` VALUES ('$dateTime', '$browser', '$username', '$ip')");

?>
