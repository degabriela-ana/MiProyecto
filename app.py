from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
from extract_features import extract_features
import pandas as pd
import traceback

app = Flask(__name__, template_folder='templates')
CORS(app)

# Cargar modelo al iniciar
try:
    with open('phishing_detector_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('feature_names.pkl', 'rb') as f:
        feature_names = pickle.load(f)
    
    MODEL_LOADED = True
except Exception as e:
    print(f"Error cargando modelo: {e}")
    MODEL_LOADED = False

@app.route('/')
def index():
    """
    Sirve la página principal
    """
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Endpoint para predecir si una URL es phishing
    """
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400
        
        if not MODEL_LOADED:
            return jsonify({'error': 'Modelo no cargado. Entrena el modelo primero.'}), 500
        
        # Extraer características
        features = extract_features(url)
        
        # Crear DataFrame con el orden correcto
        df = pd.DataFrame([features])
        df = df[feature_names]
        
        # Predecir
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0]
        
        result = "PHISHING" if prediction == 1 else "LEGÍTIMA"
        confidence = float(probability[prediction] * 100)
        
        return jsonify({
            'url': url,
            'prediction': result,
            'confidence': confidence,
            'probability_legitimate': float(probability[0] * 100),
            'probability_phishing': float(probability[1] * 100),
            'status': 'success'
        })
    
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        return jsonify({
            'error': f'Error procesando URL: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """
    Verifica si el servidor está activo
    """
    return jsonify({
        'status': 'ok',
        'model_loaded': MODEL_LOADED
    })

if __name__ == '__main__':
    if not MODEL_LOADED:
        print("⚠️  ADVERTENCIA: El modelo no está cargado.")
        print("Debes ejecutar primero:")
        print("  1. python fetch_datasets.py")
        print("  2. python extract_features.py")
        print("  3. python train_model.py")
    
    print("\n🚀 Servidor iniciando en http://localhost:5000")
    print("📖 Abre tu navegador en: http://localhost:5000")
    app.run(debug=True, port=5000)