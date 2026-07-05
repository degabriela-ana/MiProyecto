PHISHING URL DETECTOR CON IA

Detector de URLs de phishing usando Machine Learning.

INSTALACION

1. Clonar proyecto
git clone https://github.com/degabriela-ana/MiProyecto.git
cd MiProyecto

2. Crear entorno virtual
python -m venv venv

3. Activar entorno virtual
Windows: venv\Scripts\activate.bat
Mac/Linux: source venv/bin/activate

4. Instalar dependencias
pip install -r requirements.txt

ENTRENAR MODELO

python fetch_datasets.py
python extract_features.py
python train_model.py

INICIAR SERVIDOR

python app.py

Abre: http://localhost:5000

AUTOR

degabriela-ana
