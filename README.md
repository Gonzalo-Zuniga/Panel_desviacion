# Integración MVC + Motor de Machine Learning para Detección de Anomalías

Este repositorio contiene la implementación de un sistema completo de **detección de anomalías en alertas de fraude**, integrando un motor de **Machine Learning desarrollado en Python** con un **backend y frontend en PHP bajo arquitectura MVC**.

El objetivo del proyecto es ofrecer un flujo claro, usable y escalable que permita cargar archivos CSV con datos históricos, procesarlos mediante un modelo entrenado y presentar resultados interpretables que apoyen la toma de decisiones operacionales.

---

## 1. Requisitos del entorno

Para ejecutar y evaluar correctamente el sistema en un entorno local se requiere contar con los siguientes componentes:

### 1.1. Herramientas de desarrollo
- **Visual Studio Code (VS Code)**  
  Editor recomendado para revisar y modificar el código del frontend, backend y scripts asociados.

- **XAMPP** (o stack equivalente como WAMP/LAMP)  
  Incluye:
  - Apache (servidor web)
  - PHP (backend MVC)
  - MySQL/MariaDB (opcional, no utilizado en esta versión)

> Nota: El sistema ha sido probado en un entorno local con XAMPP sobre Windows. Otros entornos equivalentes son compatibles siempre que permitan la ejecución de PHP y la invocación de scripts Python desde el backend.

### 1.2. Entorno de Machine Learning
- **Python 3.9 o superior**
- Librerías principales:
  - pandas
  - numpy
  - scikit-learn
  - joblib

El modelo entrenado y el script de inferencia se ejecutan desde el backend PHP mediante llamadas al intérprete de Python.

---

## 2. Estructura general del repositorio

El sistema se organiza en las siguientes carpetas principales:

- **Modelo en python/**  
  Contiene el desarrollo completo del modelo en Jupyter Notebook, incluyendo análisis exploratorio, entrenamiento y evaluación.

- **despliegue_web/**  
  Contiene el sistema web completo bajo arquitectura MVC en PHP (frontend y backend).

- **README.md**  
  Documento de descripción y guía de ejecución del proyecto.

---

## 3. Ejecución y visualización del sistema

El proyecto puede revisarse y ejecutarse de dos formas complementarias:  
 a) mediante el análisis del modelo en Python,  
 b) A través del despliegue web del sistema completo.

Ambos enfoques permiten evaluar el comportamiento del modelo y los resultados obtenidos, desde una perspectiva analítica y operacional, respectivamente.

---

### 3.1. Visualización y análisis del modelo en Python

La carpeta **`Modelo en python/`** contiene el desarrollo completo del modelo de aprendizaje automático en formato **Jupyter Notebook**, donde se documenta el proceso de preparación de datos, análisis exploratorio, feature engineering, entrenamiento y evaluación del modelo.

Para revisar el modelo en Python se recomienda:

1. Descargar o clonar el repositorio en su equipo.
2. Abrir la carpeta `Modelo en python/` en **Google Colab** o **Jupyter Notebook**.
3. Ejecutar el notebook principal de forma secuencial para reproducir:
   - El análisis exploratorio de datos  
   - La construcción de variables  
   - El entrenamiento del modelo  
   - La evaluación mediante métricas y gráficos  
4. Revisar la generación del modelo entrenado, el cual es persistido para su uso posterior en el sistema web.

Este enfoque permite comprender en detalle la lógica del modelo y validar los resultados desde una perspectiva analítica.

---

### 3.2. Ejecución del sistema web (Frontend + Backend)

La carpeta **`despliegue_web/`** contiene el sistema completo de despliegue bajo arquitectura **MVC en PHP**, integrado con el motor de Machine Learning desarrollado en Python.

Para ejecutar y visualizar el sistema web:

> **Importante:** Para la correcta ejecución de este paso, es necesario haber completado previamente el Paso 1. En caso de requerir apoyo adicional para la configuración del entorno, puede consultarse el Punto 5.


1. Descargar o clonar el repositorio en su equipo.
2. Copiar la carpeta `despliegue_web/` dentro del directorio `htdocs` de **XAMPP**.
3. Abrir la carpeta `despliegue_web/` en **Visual Studio Code** para revisar o modificar el código.
4. Iniciar el servicio **Apache** desde el panel de control de XAMPP.
5. Acceder al sistema desde un navegador web mediante la URL local correspondiente (por ejemplo, `http://localhost/despliegue_web`).

Desde la interfaz web es posible cargar archivos CSV con datos históricos y visualizar los resultados generados por el modelo, incluyendo alertas normales, alertas anómalas y el score de criticidad asociado.

---

### 3.3. Relación entre el modelo y el despliegue web

El modelo entrenado en Python es el mismo que se utiliza durante el despliegue web del sistema.  
El backend en PHP se encarga de invocar el script de inferencia en Python, enviar el archivo CSV para su análisis y recibir los resultados en formato JSON, los cuales son posteriormente procesados y presentados en el frontend.

De este modo, el repositorio permite evaluar el proyecto tanto desde una perspectiva académica (modelo en Python) como desde una perspectiva práctica y operativa (sistema web).

---

## 4. Consideraciones adicionales

- El dataset no se incluye en el repositorio debido a su carácter sensible.
- Para archivos de gran tamaño, se recomienda ajustar la configuración de PHP:
  - `upload_max_filesize`
  - `post_max_size`
  - `memory_limit` (recomendado ≥ 64M)
- Es necesario que el entorno permita la ejecución de Python desde PHP para el correcto funcionamiento del sistema.

---

## 5. Referencias externas:

Para usuarios que requieran apoyo adicional en la configuración del entorno local, se pueden consultar tutoriales públicos en Internet sobre:

 * Instalación de Visual Studio Code y extensiones de PHP
   
 *Instalación y configuración de XAMPP en Windows

> Nota: Estas referencias no forman parte del desarrollo del proyecto y se incluyen únicamente como material de apoyo opcional.

---

## 6. Acceso al dataset

El dataset no se encuentra disponible en este repositorio debido a su carácter sensible.  
Para consultas académicas o solicitud de acceso:

📧 g.zuigaguerra@uandresbello.edu

---

## 7. Resumen

- **Frontend:** carga y visualización de resultados
- **Backend MVC:** validación y orquestación del flujo
- **Machine Learning:** detección de anomalías y scoring automático

Este repositorio constituye una base sólida para futuras extensiones, tales como integración con APIs REST, despliegue en la nube y automatización de pipelines.
