<?php

if (!isset($_SESSION['auth'])) {
	die('HIS EXCELLENCE (and daughter) ONLY!');
}

$db = new SQLite3('./ooosql', 0666, $sqliteerror);
if (!$db) {
	die('connection failed');
}

$head = '<html><head><link rel="stylesheet" href="bOootstrap.css">
				<title>OooSQL</title></head>
				<body>
				<h1>OooSQL Control Panel</h1>
				<table>';

$foot = '</table></body></html>';

echo $head;
