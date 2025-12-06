
# Integración MVC + Motor de Machine Learning  
Este repositorio contiene los elementos necesarios para comprender e implementar un sistema completo de **detección de anomalías** utilizando un modelo de Machine Learning entrenado en Python e integrado a un frontend y backend desarrollados bajo la arquitectura **MVC en PHP**.

El objetivo del proyecto es ofrecer un flujo claro, escalable y usable que permita cargar archivos CSV, procesarlos mediante el modelo entrenado y presentar resultados interpretables para apoyar la toma de decisiones.

---

## 1. Estructura general del repositorio

El sistema se divide en tres componentes principales:

### 1.1. Motor de Machine Learning (Python)  
Este módulo contiene todo el desarrollo del modelo, incluyendo:

- Preparación y análisis previo de datos  
- Feature engineering  
- Entrenamiento del modelo seleccionado (Random Forest)  
- Guardado del modelo (`model.pkl`) y preprocesador (`preprocessor.pkl`)  
- Script de inferencia (`run_model.py`) encargado de recibir un CSV, procesarlo y devolver las predicciones en formato JSON  

Este componente debe ejecutarse en un entorno Python 3.9+ con las librerías indicadas.  
El dataset no está incluido, ya que contiene información sensible. Para acceder, debe solicitarse directamente al autor.

**Recomendación:** abrir y ejecutar el notebook original en Google Colab o Jupyter Notebook para visualizar el proceso completo de entrenamiento.

---

## 2. Backend en MVC (PHP)

El backend está construido bajo el patrón Modelo–Vista–Controlador, lo que facilita la mantenibilidad y escalabilidad del sistema.  
Su función es:

- Validar el archivo cargado por el usuario  
- Verificar que el dataset cumpla con las condiciones mínimas (formato CSV, existencia de columnas esperadas y ≥ 30 días de registros por alerta)  
- Enviar el archivo al motor Python para su análisis  
- Recibir los resultados en JSON y preparar la respuesta para el frontend  

El backend también establece los mecanismos de comunicación con el modelo de ML y actúa como intermediario entre la vista y la ejecución del modelo.

---

## 3. Frontend del sistema

El frontend está desarrollado utilizando HTML5, Bootstrap 5 y estilos personalizados para entregar una interfaz clara, moderna y fácil de usar.  
Incluye las siguientes funciones:

- Pantalla principal con carga de archivo CSV  
- Validación visual de errores (formato incorrecto, falta de columnas, archivo sin datos suficientes, etc.)  
- Vista de resultados que presenta:  
  - Alertas normales  
  - Alertas anómalas  
  - Score del modelo para cada registro  
  - Explicación resumida basada en variables importantes  

Cuando el dataset cargado contiene más de un día de información, el sistema muestra únicamente el día más reciente, cumpliendo con el requisito de facilitar la inspección operativa diaria.

---

## 4. Flujo completo del sistema

El funcionamiento general es el siguiente:

1. El usuario accede al sistema y carga un archivo CSV con datos históricos.  
2. El controlador valida el archivo y lo envía al script Python.  
3. El motor de ML procesa el archivo, aplica el preprocesamiento original y ejecuta el modelo entrenado.  
4. Python retorna un archivo JSON con predicciones, scores y explicabilidad.  
5. El backend presenta los resultados en la interfaz, separando alertas normales de anomalías.  

Este flujo reproduce de manera fiel el comportamiento esperado de un sistema real de monitoreo operativo.

---

## 5. Sobre el modelo utilizado

El modelo principal es un **Random Forest Classifier**, seleccionado tras evaluar múltiples configuraciones.  
Se eligió por ser:

- Robusto ante ruido  
- Adecuado para datos tabulares  
- Capaz de manejar desbalance moderado mediante `class_weight=balanced`  
- Compatibile con explicabilidad mediante feature importance  
- Rápido en inferencia y apto para entornos productivos  

El preprocesamiento se mantiene consistente con el notebook original, asegurando que el modelo reciba los mismos tipos de transformaciones.

---

## 6. Recomendaciones de uso

1. Ejecutar primero el notebook de entrenamiento para comprender la lógica del modelo.  
2. Mantener la estructura del directorio tal como se presenta en este repositorio.  
3. Asegurarse de que la ejecución de Python desde PHP esté habilitada en el servidor local.  
4. configurar php.init a 64M para archivos con grandes volumenes de datos.
---

## 7. Contacto para acceso al dataset

Debido a la naturaleza sensible de los datos, el dataset no está disponible en el repositorio.  
Para solicitar acceso:

📧 g.zuigaguerra@uandresbello.edu

---

## 8. Resumen del uso del repositorio

1. **Frontend:** Carga y presentación de resultados  
2. **Backend MVC:** Validación, control del flujo y comunicación Python ↔ PHP  
3. **ML Engine:** Modelo entrenado + preprocesador + inferencia automática  

Este repositorio constituye una base sólida para evolucionar hacia una arquitectura más completa, incluyendo APIs REST, integración con AWS, pipelines automáticos y despliegue productivo.

