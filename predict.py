import pickle
from extract_features import extract_features
import pandas as pd

def load_model():
    """Carga el modelo entrenado"""
    with open('phishing_detector_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('feature_names.pkl', 'rb') as f:
        feature_names = pickle.load(f)
    
    return model, feature_names

def predict_url(url):
    """
    Predice si una URL es phishing o legítima
    """
    model, feature_names = load_model()
    
    # Extraer características
    features = extract_features(url)
    
    # Crear DataFrame con el orden correcto
    df = pd.DataFrame([features])
    df = df[feature_names]
    
    # Predecir
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0]
    
    result = "PHISHING" if prediction == 1 else "LEGÍTIMA"
    confidence = probability[prediction] * 100
    
    return {
        'url': url,
        'prediction': result,
        'confidence': confidence,
        'probability_legitimate': probability[0] * 100,
        'probability_phishing': probability[1] * 100
    }

if __name__ == "__main__":
    # Ejemplo de uso
    test_urls = [
        'https://www.google.com',
        'http://goog1e-verify.com',
        'https://www.amazon.com',
        'http://amaz0n-secure.com'
    ]
    
    print("Probando detector de phishing:\n")
    
    for url in test_urls:
        result = predict_url(url)
        print(f"URL: {result['url']}")
        print(f"Predicción: {result['prediction']}")
        print(f"Confianza: {result['confidence']:.2f}%")
        print(f"  Legítima: {result['probability_legitimate']:.2f}%")
        print(f"  Phishing: {result['probability_phishing']:.2f}%")
        print("-" * 60)