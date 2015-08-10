<?php 
include_once 'handler.php'; // проверяем авторизирован ли пользователь
include_once 'log.php';

if($user) { 
// выводим информацию для пользователя 
echo 'hi, <b>'.$user['username'].'</b>!<br /> 
- <a href="chat.php">chat</a></br>
- <a href="exit.php">exit</a><br /> 
'; 
} else { 
// выводим информацию для гостя 
echo ' 
- <a href="login.php">authorization</a><br /> 
- <a href="register.php">registration</a><br />
<br><img src = "9ECA_52007441.gif">
'; 
} 
?>
