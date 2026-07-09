from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import os
import pandas as pd
from extract_features import extract_features
import traceback
from sklearn.ensemble import RandomForestClassifier
import numpy as np

app = Flask(__name__, template_folder='templates')
CORS(app)

MODEL_LOADED = False
model = None
feature_names = None

def create_simple_model():
    """Crea un modelo simple sin necesidad de descargar datos"""
    global MODEL_LOADED, model, feature_names
    
    print("🤖 Creando modelo simple...")
    
    try:
        feature_names = ['url_length', 'domain_length', 'dots_in_domain', 'dashes_in_domain',
                        'subdomains', 'has_at_sign', 'has_ip', 'has_port', 'uses_https',
                        'special_chars_count', 'has_digits_in_domain', 'path_length',
                        'slashes_count', 'phishing_keywords', 'common_tld']
        
        X_train = np.array([
            [19, 10, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 1],
            [20, 11, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 3, 0, 1],
            [25, 12, 1, 0, 0, 0, 0, 0, 1, 0, 0, 2, 3, 0, 1],
            [18, 9, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 1],
            [22, 13, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 2, 0, 1],
            [50, 20, 2, 1, 1, 0, 0, 0, 0, 5, 1, 3, 5, 2, 0],
            [45, 18, 3, 2, 2, 1, 0, 0, 0, 4, 1, 2, 4, 1, 0],
            [55, 22, 2, 1, 1, 0, 0, 1, 0, 6, 0, 4, 6, 3, 0],
            [48, 19, 3, 1, 1, 0, 1, 0, 0, 5, 1, 3, 5, 2, 0],
            [52, 21, 2, 2, 1, 0, 0, 0, 0, 5, 0, 3, 5, 2, 0],
        ])
        
        y_train = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
        
        model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
        model.fit(X_train, y_train)
        
        with open('phishing_detector_model.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        with open('feature_names.pkl', 'wb') as f:
            pickle.dump(feature_names, f)
        
        MODEL_LOADED = True
        print("✅ Modelo simple creado y guardado")
        return True
        
    except Exception as e:
        print(f"❌ Error creando modelo: {e}")
        return False

def load_or_create_model():
    """Carga modelo existente o crea uno simple"""
    global MODEL_LOADED, model, feature_names
    
    print("🔍 Verificando modelo...")
    
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
    
    create_simple_model()

load_or_create_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400
        
        if not MODEL_LOADED:
            return jsonify({'error': 'Modelo no cargado.'}), 500
        
        features = extract_features(url)
        df = pd.DataFrame([features])
        df = df[feature_names]
        
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
            'st
