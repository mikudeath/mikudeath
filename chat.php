<html>
<?php
include_once "handler.php";

if(!$user){
    header("Location: index.php");
}
else{
    $title = "chat";
    }
?>
<head>
    <title><?php echo $title; ?></title>
    <link rel="stylesheet" href="style.css" type="text/css" />
</head>
<body>
<?php

$activeUser = $user['username'];
echo "Hi, <b><a href = 'profiles/$activeUser.html'>$activeUser</a></b>.";
echo "Your message: <br>
      <form method = 'POST' action = 'add_m.php'>
      <textarea cols = 40 rows = 5 name = 'contents'></textarea><br>
      <input type='submit' value='Send'>
      </form><hr>";
$rows = mysql_result(mysql_query("SELECT COUNT(*) FROM `chat`"), 0);
echo "<div class='chat'>";
for($i = $rows-1; $i >= 0; $i--){
    $id = mysql_result(mysql_query("SELECT `id` FROM `chat`"), $i);
    $message = mysql_result(mysql_query("SELECT `contents` FROM `chat` WHERE `id` = $id"), 0);
    $username = mysql_result(mysql_query("SELECT `username` FROM `chat` WHERE `id` = $id"), 0);
    $dateTime = mysql_result(mysql_query("SELECT `datetime` FROM `chat` WHERE `id` = $id"), 0);
    echo "$dateTime nickname: <a href='profiles/$username.html'>$username</a> <div class='anchor'><a href = #id$id>#$id</a></div>
         <br><br>$message<hr>";
}
echo "</div>";

?>
</body>
</html>
