<?php
$regis = $_POST['regis'];

$cwd =getcwd();
$rc=0;
echo 'regis='.$regis.'<br>';
//echo getcwd();
ob_start();

passthru('/usr/bin/python2.7  ./glive.py '.$regis, $rc);

$output = ob_get_clean();
echo nl2br($output);
?>
