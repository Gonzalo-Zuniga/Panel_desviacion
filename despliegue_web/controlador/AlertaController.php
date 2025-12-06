<?php
// controlador/AlertaController.php

class AlertaController
{
    public function index()
    {
        $resumen = null;
        $error   = null;

        include __DIR__ . '/../vista/dashboard_alertas.php';
    }

    public function procesarUpload()
    {
        $resumen = null;
        $error   = null;

        if (!isset($_FILES['archivo_csv'])) {
            $error = "No se recibió ningún archivo.";
            include __DIR__ . '/../vista/dashboard_alertas.php';
            return;
        }

        $file = $_FILES['archivo_csv'];

        // Validar extensión
        $ext = pathinfo($file['name'], PATHINFO_EXTENSION);
        if (strtolower($ext) !== 'csv') {
            $error = "El archivo debe estar en formato .csv";
            include __DIR__ . '/../vista/dashboard_alertas.php';
            return;
        }

        // Carpeta de uploads
        $uploadDir = __DIR__ . '/../storage/uploads/';
        if (!is_dir($uploadDir)) {
            mkdir($uploadDir, 0777, true);
        }

        $destino = $uploadDir . basename($file['name']);

        if (!move_uploaded_file($file['tmp_name'], $destino)) {
            $error = "No se pudo guardar el archivo en el servidor.";
            include __DIR__ . '/../vista/dashboard_alertas.php';
            return;
        }

        // Ejecutar script de scoring en Python
        // Cambia "python" por "python3" si tu entorno lo requiere.
        $cmd = 'python ' . escapeshellarg(__DIR__ . '/../modelo/scoring.py') .
               ' ' . escapeshellarg($destino);

        $output = shell_exec($cmd);

        if ($output === null) {
            $error = "No se pudo ejecutar el modelo de scoring.";
            include __DIR__ . '/../vista/dashboard_alertas.php';
            return;
        }

        $json = json_decode($output, true);

        if ($json === null || isset($json['error'])) {
            $error = $json['error'] ?? "Error al procesar el archivo en el modelo.";
        } else {
            $resumen = $json;
        }

        include __DIR__ . '/../vista/dashboard_alertas.php';
    }
}
?>

