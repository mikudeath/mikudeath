<?php 
include_once 'handler.php'; // checking is the user is authorized
include_once 'log.php';

if($user) { 
// if yes showing the information for him 
echo 'hi, <b>'.$user['username'].'</b>!<br /> 
- <a href="chat.php">chat</a></br>
- <a href="exit.php">exit</a><br /> 
'; 
} else { 
// if no showing guest-information
echo ' 
- <a href="login.php">authorization</a><br /> 
- <a href="register.php">registration</a><br />
'; 
} 
?>
