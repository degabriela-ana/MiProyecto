from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import os
import pandas as pd
from extract_features import extract_features
import traceback

app = Flask(__name__, template_folder='templates')
CORS(app)

MODEL_LOADED = False
model = None
feature_names = None

def train_model_if_needed():
    """Entrena el modelo si no existe"""
    global MODEL_LOADED, model, feature_names
    
    print("🔍 Verificando modelo...")
    
    # Si el modelo existe, cargarlo
    if os.path.exists('phishing_detector_model.pkl') and os.path.exists('feature_names.pkl'):
        try:
            with open('phishing_detector_model.pkl', 'rb') as f:
                model = pickle.load(f)
            with open('feature_names.pkl', 'rb') as f:
                feature_names = pickle.load(f)
            MODEL_LOADED = True
            print("✅ Modelo cargado correctamente")
            return
        except Exception as e:
            print(f"⚠️ Error cargando modelo: {e}")
    
    # Si no existe, entrenar
    print("⏳ Entrenando modelo (esto puede tomar unos minutos)...")
    
    try:
        from fetch_datasets import combine_datasets
        from extract_features import process_dataset
        from train_model import train_model
        
        # 1. Descargar datos
        print("📥 Descargando datos...")
        combine_datasets()
        
        # 2. Extraer características
        print("🔧 Extrayendo características...")
        process_dataset('dataset_combined.csv', 'features_dataset.csv')
        
        # 3. Entrenar modelo
        print("🤖 Entrenando modelo...")
        model = train_model('features_dataset.csv')
        
        # 4. Cargar feature names
        with open('feature_names.pkl', 'rb') as f:
            feature_names = pickle.load(f)
        
        MODEL_LOADED = True
        print("✅ Modelo entrenado y guardado correctamente")
        
    except Exception as e:
        print(f"❌ Error entrenando modelo: {e}")
        print(traceback.format_exc())
        MODEL_LOADED = False

# Entrenar modelo al iniciar
train_model_if_needed()

@app.route('/')
def index():
    """Sirve la página principal"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """Endpoint para predecir si una URL es phishing"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400
        
        if not MODEL_LOADED:
            return jsonify({'error': 'Modelo no cargado. Intenta más tarde.'}), 500
        
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
    """Verifica si el servidor está activo"""
    return jsonify({
        'status': 'ok',
        'model_loaded': MODEL_LOADED
    })

if __name__ == '__main__':
    print("\n🚀 Servidor iniciando...")
    print("📖 Abre tu navegador en: http://localhost:5000")
    app.run(debug=True, port=5000)
