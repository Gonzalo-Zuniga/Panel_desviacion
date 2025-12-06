<?php
// index.php 

require __DIR__ . '/controlador/AlertaController.php';

$accion = $_GET['accion'] ?? 'index';

$controller = new AlertaController();

switch ($accion) {
    case 'procesar':
        $controller->procesarUpload();
        break;
    case 'index':
    default:
        $controller->index();
        break;
}
?>


