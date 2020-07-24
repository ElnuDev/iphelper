<?php
// https://v6.iphelper.io/
header("Content-Type: text/plain");
if (filter_var($_SERVER['REMOTE_ADDR'], FILTER_VALIDATE_IP, FILTER_FLAG_IPV6)) {
	echo $_SERVER['REMOTE_ADDR'];
} else {
	echo "Invalid";
}
?>
