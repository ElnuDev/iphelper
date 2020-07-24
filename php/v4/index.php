<?php
// https://v4.iphelper.io/
header("Content-Type: text/plain");
if (filter_var($_SERVER['REMOTE_ADDR'], FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
	echo $_SERVER['REMOTE_ADDR'];
} else {
	echo "Invalid";
}
?>
