<?php 
include_once 'handler.php';

if($user) { 
header ('Location: index.php'); 
exit(); 
} 

if(!empty($_POST['login']) AND !empty($_POST['password'])) 
{ 
$login = mysql_real_escape_string(htmlspecialchars($_POST['login']));
$password = mysql_real_escape_string(htmlspecialchars($_POST['password']));

$search_user = mysql_result(mysql_query("SELECT COUNT(*) FROM `users_profiles` WHERE `username` = '".$login."' AND `password` = '".md5($password)."'"), 0);
if($search_user == 0) 
{ 
echo 'error';
exit(); 
} 
else 
{ 
$time = 60*60*24;
setcookie('username', $login, time()+$time, '/'); 
setcookie('password', md5($password), time()+$time, '/'); 
echo 'welcome, ' .$user['username'] .'. <a href="chat.php">chat</a>';
exit(); 
}
} 
echo ' 
<form action="login.php" method="POST"> 
login:<br /> 
<input name="login" type="text" /><br /> 
password:<br /> 
<input name="password" type="password" /><br /> 
<input type="submit" value="authorize" /> 
</form>'; 
?>
