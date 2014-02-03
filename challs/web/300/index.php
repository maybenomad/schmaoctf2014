<? session_start();

if (!isset($_SESSION['id'])) {
	header('Location: login.php');
	exit();
}

if (isset($_POST['search'])) {

	$db = new SQLite3('./ooosql', 0666, $sqliteerror);
	if (!$db) {
		die('connection failed');
	}

	$qry = sprintf("SELECT * FROM souls WHERE first_name LIKE '%s%%' OR 
		last_name LIKE '%s%%';", $_POST['search'], $_POST['search']);

	echo '<!-- ' . $qry . '-->';
}
?>

<html>
	<head>
		<link rel="stylesheet" href="bOootstrap.css">
		<title>OooSQL</title>
	</head>
	<body>
		<h1>OooSQL Control Panel</h1>
		<div id="searchbox">
			<form method="post" action="index.php">
				<input type="text" class="search" name="search">
				<input type="submit" name="submit" class="find" value="Find Souls">
			</form>
			<table>

<?
// ' UNION ALL SELECT null, null, username, password FROM users WHERE username='hunson_abadeer'; --
if ($_SESSION['username'] == 'hunson_abadeer') {
	echo '<p style="font-size: 20px; color: #27ae60; text-align: center; margin: 0;">0ffer_y0ur_s0ul_t0_m3_d4rk_0ne</p>';
}

if (isset($_POST['search'])) {

	$results = $db->query($qry);

	echo '<tr class="head"><td class="first">First Name</td>
				<td class="last">Last Name</td><td class="age">Age</td></tr>';

	while ($res = ($results->fetchArray(SQLITE3_ASSOC))) {
		echo '<tr>';
		foreach ($res as $td) {
			if ($res['id'] == $td) 
				continue;
			echo '<td>' . $td . '</td>';
		}
		echo '</tr>';
	}
}

?>
			</table>
		</div>
  </body>
</html>