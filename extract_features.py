import pandas as pd
import re
from urllib.parse import urlparse

def extract_features(url):
    """
    Extrae características de una URL para entrenar el modelo
    """
    features = {}
    
    try:
        # Parsing básico
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        
        # 1. Longitud de la URL
        features['url_length'] = len(url)
        
        # 2. Longitud del dominio
        features['domain_length'] = len(domain)
        
        # 3. Número de puntos en el dominio
        features['dots_in_domain'] = domain.count('.')
        
        # 4. Número de guiones en el dominio
        features['dashes_in_domain'] = domain.count('-')
        
        # 5. Número de subdominios
        features['subdomains'] = len(domain.split('.')) - 1
        
        # 6. Presencia de '@' (usuario en URL)
        features['has_at_sign'] = 1 if '@' in url else 0
        
        # 7. Presencia de IP en lugar de dominio
        features['has_ip'] = 1 if re.match(r'\d+\.\d+\.\d+\.\d+', domain) else 0
        
        # 8. Presencia de puerto
        features['has_port'] = 1 if ':' in domain else 0
        
        # 9. Uso de HTTPS
        features['uses_https'] = 1 if parsed.scheme == 'https' else 0
        
        # 10. Número de caracteres especiales en la URL
        special_chars = re.findall(r'[^a-zA-Z0-9/.:\-_?=&]', url)
        features['special_chars_count'] = len(special_chars)
        
        # 11. Presencia de números en el dominio
        features['has_digits_in_domain'] = 1 if any(c.isdigit() for c in domain) else 0
        
        # 12. Longitud del path
        features['path_length'] = len(path)
        
        # 13. Número de slashes en la URL
        features['slashes_count'] = url.count('/')
        
        # 14. Presencia de palabras comunes de phishing
        phishing_keywords = ['verify', 'confirm', 'account', 'login', 'signin', 'update', 'secure', 'bank', 'password']
        features['phishing_keywords'] = sum(1 for keyword in phishing_keywords if keyword in url.lower())
        
        # 15. Presencia de TLD común
        common_tlds = ['com', 'org', 'net', 'edu', 'gov', 'co', 'uk', 'de', 'fr']
        tld = domain.split('.')[-1] if '.' in domain else ''
        features['common_tld'] = 1 if tld.lower() in common_tlds else 0
        
    except Exception as e:
        print(f"Error procesando URL {url}: {e}")
        feature_names = ['url_length', 'domain_length', 'dots_in_domain', 'dashes_in_domain',
                        'subdomains', 'has_at_sign', 'has_ip', 'has_port', 'uses_https',
                        'special_chars_count', 'has_digits_in_domain', 'path_length',
                        'slashes_count', 'phishing_keywords', 'common_tld']
        features = {name: 0 for name in feature_names}
    
    return features

def process_dataset(input_file, output_file):
    """
    Procesa el dataset completo
    """
    print(f"Leyendo {input_file}...")
    df = pd.read_csv(input_file)
    
    print(f"Extrayendo características de {len(df)} URLs...")
    
    # Aplicar extractor de características
    features_list = []
    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"  Procesadas {idx}/{len(df)} URLs...")
        
        features = extract_features(row['url'])
        features['label'] = 1 if row['label'] == 'phishing' else 0
        features_list.append(features)
    
    df_features = pd.DataFrame(features_list)
    
    print(f"Guardando en {output_file}...")
    df_features.to_csv(output_file, index=False)
    
    print(f"\nCaracterísticas extraídas:")
    print(df_features.head())
    
    return df_features

if __name__ == "__main__":
    process_dataset('dataset_combined.csv', 'features_dataset.csv')