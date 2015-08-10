<?php

include_once "handler.php";
$username = $user["username"];
$date_time = date("m.d.Y - H:i:s");
$contents = $_POST['contents'];
mysql_query("INSERT INTO `chat` (`datetime`, `contents`, `username`) VALUES ('$date_time', '$contents', '$username')") or die("error");
header("Location: chat.php");

?>
