<?php
$dd = $_POST['dd'];
$mm = $_POST['mm'];
$yy = $_POST['yy'];
$md = $_POST['md'];

$Filename='DATA'.$yy.$mm.$dd.'.log';
$cwd =getcwd();
$rc=0;
echo 'Filename='.$Filename.'<br>';
$DD=date('d');
$MM=date('m');
$YY=date('y');
// Change directory
if ($dd == $DD and $mm == $MM and $YY == $yy)
	{
	chdir("/nfs/OGN/DIRdata/");
	$pgm ="../src/analysisrelay.py";
	}
else
	{
	chdir("/nfs/OGN/DIRdata/data/");
	$pgm ="../../src/analysisrelay.py";
	}
//echo getcwd();
ob_start();

passthru('/usr/bin/python2.7 '.$pgm.' -sa YES -n '.$Filename.' -m '.$md, $rc);

$output = ob_get_clean(); 
echo nl2br($output);
?>

