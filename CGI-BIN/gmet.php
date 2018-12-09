<?php
$station = $_POST['station'];

$cwd =getcwd();
$rc=0;
echo 'station='.$station.'<br>';
//echo getcwd();
ob_start();

passthru('/usr/bin/python2.7  ./gmet.py '.$station, $rc);

$output = ob_get_clean();
echo nl2br($output);
?>
