<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

$file = file_get_contents('php://input');
$data = json_decode($file);

$ip_addr = $_SERVER['REMOTE_ADDR'];
if($ip_addr === '127.0.0.1') {

	$timestamp = $data->ts;
	$kyocera = $data->kyocera;
	$dell = $data->dell;

	$db = new SQLite3("printer.db");
	$db->exec("CREATE TABLE IF NOT EXISTS printer (ts INTEGER, kyocera INTEGER, dell INTEGER);");
	$statement = $db->prepare('INSERT INTO printer (ts, kyocera, dell) VALUES (:ts, :kyocera, :dell);');
	$statement->bindValue(':ts', $timestamp);
	$statement->bindValue(':kyocera', $kyocera);
	$statement->bindValue(':dell', $dell);
	$result = $statement->execute();

}else{
	http_response_code(403);
}
?>
