# Detector de Phishing con IA

Este proyecto es un detector de URLs que utiliza Machine Learning (Aprendizaje Automático) para identificar si un enlace es legítimo o un intento de phishing. La idea es simple: ingresas una URL y el modelo te dice si es segura o no.

La aplicación está en la web y funciona 24/7, así que cualquiera puede usarla en cualquier momento.

---

## ¿Qué es el Phishing?

El phishing es cuando alguien crea un sitio web falso que se parece al real (como un banco o PayPal) para robarte contraseñas o datos. Este detector ayuda a identificar esos intentos analizando características de la URL.

---

## Herramientas:

**Backend (Servidor):**
- Python 3.9 - Lenguaje principal
- Flask - Para crear la API (Interfaz de Programación de Aplicaciones) web
- scikit-learn - Para entrenar el modelo de Machine Learning (Aprendizaje Automático)
- pandas y numpy - Para manejar datos

**Frontend (Página Web):**
- HTML5, CSS3 y JavaScript - Para la página web

**Deployment (Alojamiento):**
- Vercel - Para que la app esté en internet
- GitHub - Para guardar el código

---

## ¿Cómo Funciona?

### Paso 1: Extracción de Características

Cuando ingresas una URL, el sistema analiza cosas como:
- ¿Tiene HTTPS (protocolo seguro)?
- ¿Qué tan larga es?
- ¿Tiene caracteres raros?
- ¿El dominio se ve normal?
- ¿Tiene una IP en lugar de un dominio?

### Paso 2: Análisis con el Modelo

El modelo de Machine Learning (Aprendizaje Automático) (entrenado con cientos de URLs) analiza todas esas características y calcula la probabilidad de que sea phishing o legítima.

### Paso 3: Resultado

Te muestra:
- Si es PHISHING o LEGÍTIMA
- El porcentaje de confianza
- Las probabilidades detalladas

---

## Estructura del Proyecto
