<?php 
include_once 'handler.php'; // проверяем авторизирован ли пользователь

// если да, перенаправляем его на главную страницу 
if($user) { 
header ('Location: index.php'); 
exit(); 
} 

if (!empty($_POST['login']) AND !empty($_POST['password'])) 
{ 
// фильтрируем логин и пароль 
$login = mysql_real_escape_string(htmlspecialchars($_POST['login']));
$password = mysql_real_escape_string(htmlspecialchars($_POST['password']));

if (mysql_result(mysql_query("SELECT COUNT(*) FROM `users_profiles` WHERE `username` = '".$login."' LIMIT 1;"), 0) != 0)
{ 
echo 'login already exists'; 
exit(); 
} 
mysql_query("INSERT INTO `users_profiles` (`username`, `password`) VALUES ('".$login."', '".md5($password)."')");
if(!file_exists("profiles\\".$login.".html")){
    $profile = fopen("profiles\\$login.html", "w");
    fclose($profile);
}
echo 'registration was succesful';
exit(); 
} 
echo ' 
<form action="register.php" method="POST"> 
login:
 
<input name="login" type="text" value="" />
 
password:
 
<input name="password" type="password" value="" />
 
<input type="submit" value="make new profile" /> 
</form>'; 
?>
