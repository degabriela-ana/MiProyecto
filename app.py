from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import re
from urllib.parse import urlparse

app = Flask(__name__, template_folder='templates')
CORS(app)

def extract_features(url):
    features = {}
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        
        features['url_length'] = len(url)
        features['domain_length'] = len(domain)
        features['dots_in_domain'] = domain.count('.')
        features['dashes_in_domain'] = domain.count('-')
        features['subdomains'] = len(domain.split('.')) - 1
        features['has_at_sign'] = 1 if '@' in url else 0
        features['has_ip'] = 1 if re.match(r'\d+\.\d+\.\d+\.\d+', domain) else 0
        features['has_port'] = 1 if ':' in domain else 0
        features['uses_https'] = 1 if parsed.scheme == 'https' else 0
        features['special_chars_count'] = len(re.findall(r'[^a-zA-Z0-9/.:\-_?=&]', url))
        features['has_digits_in_domain'] = 1 if any(c.isdigit() for c in domain) else 0
        features['path_length'] = len(path)
        features['slashes_count'] = url.count('/')
        features['phishing_keywords'] = sum(1 for kw in ['verify', 'confirm', 'account', 'login', 'update', 'secure'] if kw in url.lower())
        features['common_tld'] = 1 if domain.split('.')[-1].lower() in ['com', 'org', 'net', 'edu', 'gov', 'co', 'uk'] else 0
    except:
        pass
    
    return features

def predict_phishing(url):
    features = extract_features(url)
    
    score = 0
    
    if features['url_length'] > 75:
        score += 2
    if features['has_ip'] == 1:
        score += 3
    if features['has_at_sign'] == 1:
        score += 2
    if features['uses_https'] == 0:
        score += 2
    if features['phishing_keywords'] > 0:
        score += 2
    if features['dashes_in_domain'] > 2:
        score += 1
    if features['dots_in_domain'] > 3:
        score += 1
    if features['special_chars_count'] > 5:
        score += 1
    
    if score >= 6:
        prob_phishing = min(95, 40 + (score * 5))
    else:
        prob_phishing = max(5, score * 8)
    
    prob_legitimate = 100 - prob_phishing
    
    return {
        'prediction': 'PHISHING' if score >= 6 else 'LEGÍTIMA',
        'confidence': max(prob_phishing, prob_legitimate),
        'probability_phishing': prob_phishing,
        'probability_legitimate': prob_legitimate,
        'score': score
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL no proporcionada', 'status': 'error'}), 400
        
        result = predict_phishing(url)
        
        return jsonify({
            'url': url,
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'probability_legitimate': result['probability_legitimate'],
            'probability_phishing': result['probability_phishing'],
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
