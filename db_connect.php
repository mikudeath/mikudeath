<?php 

mysql_connect('127.0.0.1', 'root', 'vertrigo') or die('error MySQL!');
mysql_select_db('chat') or die ('error MySQL!');
mysql_query("SET NAMES cp1251");

?>
