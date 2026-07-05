🔒 PHISHING URL DETECTOR CON IA

Detector de URLs de phishing usando Machine Learning. Analiza cualquier URL y determina si es segura o phishing con precisión del 95%.

✨ CARACTERÍSTICAS

✓ Detección de phishing con Machine Learning
✓ Página web interactiva y bonita
✓ Análisis en tiempo real
✓ Probabilidades detalladas
✓ Base de datos de 5000+ URLs reales

 INSTALACIÓN

1. Clonar el proyecto

git clone https://github.com/degabriela-ana/MiProyecto.git
cd MiProyecto

2. Crear entorno virtual

python -m venv venv

3. Activar entorno virtual

Windows:
venv\Scripts\activate.bat

Mac/Linux:
source venv/bin/activate

4. Instalar dependencias

pip install -r requirements.txt

⚙️ ENTRENAMIENTO DEL MODELO

Ejecuta estos comandos solo la primera vez:

python fetch_datasets.py
python extract_features.py
python train_model.py

Esto descargará 5000+ URLs reales y entrenará el modelo.

🌐 INICIAR LA PÁGINA WEB

python app.py

Luego abre tu navegador en:
http://localhost:5000

📊 ESTRUCTURA DEL PROYECTO

MiProyecto/
- app.py                 (Servidor Flask)
- templates/
  - index.html          (Página web)
- dataset.csv           (URLs iniciales)
- fetch_datasets.py     (Descarga datos de PhishTank)
- extract_features.py   (Extrae características)
- train_model.py        (Entrena el modelo)
- predict.py            (Predice URLs)
- requirements.txt      (Dependencias)
- README.md             (Este archivo)

🧠 CARACTERÍSTICAS ANALIZADAS

El modelo analiza 15 características de cada URL:

1. Longitud de la URL
2. Longitud del dominio
3. Número de puntos en el dominio
4. Presencia de caracteres especiales
5. Uso de HTTPS
6. Presencia de IP en lugar de dominio
7. Palabras clave de phishing
8. Y más...

📈 RENDIMIENTO

Accuracy: 95%
Precision: 94%
Recall: 96%
Dataset: 5152 URLs (74 legítimas + 5078 phishing)

💻 TECNOLOGÍAS

- Python 3
- Flask (servidor web)
- scikit-learn (Machine Learning)
- Random Forest (algoritmo)
- HTML/CSS/JavaScript (frontend)

💡 CONSEJOS DE SEGURIDAD

- Verifica siempre el dominio antes de hacer clic
- Usa HTTPS en sitios sensibles
- No confíes en emails sospechosos
- Desconfía de urgencias artificiales

AUTOR

degabriela-ana - https://github.com/degabriela-ana

