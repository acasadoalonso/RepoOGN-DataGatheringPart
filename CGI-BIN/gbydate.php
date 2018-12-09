<?php
$dd = $_POST['dd'];
$mm = $_POST['mm'];
$yy = $_POST['yy'];

$cwd =getcwd();
$rc=0;
echo 'Date='.$dd.$mm.$yy.'<br>';
//echo getcwd();
ob_start();

passthru('/usr/bin/python2.7  ./gbydate.py '.$dd.$mm.$yy, $rc);

$output = ob_get_clean();
echo nl2br($output);
?>
