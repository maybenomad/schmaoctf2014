<?php

$db = new SQLite3('./ooosql', 0666, $sqliteerror);
if (!$db) {
	die('connection failed');
}

$create_souls_table = 
'CREATE TABLE souls(
	id INTEGER PRIMARY KEY, 
	first_name Text, 
	last_name Text, 
	age Integer);';

$create_users_table = 
'CREATE TABLE users(
	id INTEGER PRIMARY KEY,
	username Text, 
	password Text);';

$db->query($create_souls_table);
$db->query($create_users_table);

$file_handle = fopen('names', 'r');
$i = 0; 
while (!feof($file_handle)) {
	$line = explode(" ", fgets($file_handle));
	$db->query('INSERT INTO souls (id, first_name, last_name, age) VALUES (' . 
		$i . ',\'' . $line[0] . '\',\'' . $line[1] . '\',' . rand(5, 10000) . ');');
	$i++;
}
fclose($file_handle);

$db->query("INSERT INTO users (id, username, password) VALUES (0, 'hunson_abadeer', 'soulsucker9001');");
$db->query("INSERT INTO users (id, username, password) VALUES (1, 'marceline', 'daddyslittlemonster');");
?>
