<?php session_start(); 

unset($_SESSION['id']);

if (isset($_SESSION['id'])) {
	header('Location: index.php');
	exit();
}

if (isset($_POST['username'])) {

	$db = new SQLite3('./ooosql', 0666, $sqliteerror);
	if (!$db) {
		die('connection failed');
	}

	$qr = sprintf("SELECT * FROM users WHERE username='%s';", $_POST['username']);
	$result = $db->query($qr);

	if ($res = ($result->fetchArray(SQLITE3_ASSOC))) {
		if ($res['password'] == $_POST['password']) {
			$_SESSION['id'] = 1;
			$_SESSION['username'] = $_POST['username'];
			header('Location: index.php');
			exit();	
		}
	}
}

?>

<html>
	<head>
		<link rel="stylesheet" href="bOootstrap.css">
		<title>OooSQL</title>
	</head>
	<body>
		<div id="login">
  		<h1>OooSQL v0.666</h1>
  		<form id="loginform" action="login.php" method="post">
  			<input type="text" name="username" class="text" placeholder="Username">
  			<input type="text" name="password" class="text" placeholder="Password">
  			<input type="submit" class="submit">
  		</form>
  	</div>
  </body>
 </html>