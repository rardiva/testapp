<?php
$host = "localhost";
$port = "5433";
$dbname = "TB_APP";
$user = "postgres";
$password = "100postgres100";

$conn = pg_connect("host=$host port=$port dbname=$dbname user=$user password=$password");

if (!$conn) {
    die("Database connection failed!");
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST['email'];
    $password = password_hash($_POST['password'], PASSWORD_BCRYPT);

    $query = "INSERT INTO users (email, password) VALUES ($1, $2)";
    $result = pg_query_params($conn, $query, array($email, $password));

    if ($result) {
        echo "Registration successful! You can now log in.";
    } else {
        echo "Error: Email might already be registered.";
    }
}
?>
