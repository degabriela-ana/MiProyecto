import pandas as pd
import requests
import json
from urllib.parse import urlparse

def fetch_phishtank_data(output_file='phishtank_data.csv'):
    """Descarga datos de PhishTank"""
    print("⏳ Descargando datos de PhishTank...")
    
    try:
        url = "http://data.phishtank.com/data/online-valid.json"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            urls = []
            for item in data[:5000]:  # Primeras 5000
                urls.append({
                    'url': item.get('url', ''),
                    'label': 'phishing'
                })
            
            df = pd.DataFrame(urls)
            print(f"✅ Descargadas {len(df)} URLs de phishing")
            df.to_csv(output_file, index=False)
            return df
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return None

def combine_datasets():
    """Combina datasets"""
    print("\n🔄 Combinando datasets...")
    
    # Leer dataset inicial
    df_initial = pd.read_csv('dataset.csv')
    print(f"Dataset inicial: {len(df_initial)} URLs")
    
    dataframes = [df_initial]
    
    # Descargar phishing
    df_phishtank = fetch_phishtank_data()
    if df_phishtank is not None:
        dataframes.append(df_phishtank)
    
    # Combinar
    df_combined = pd.concat(dataframes, ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=['url'])
    
    # Guardar
    df_combined.to_csv('dataset_combined.csv', index=False)
    
    # Mostrar resumen
    print(f"\n{'='*50}")
    print(f"📊 DATASET FINAL COMBINADO")
    print(f"{'='*50}")
    print(f"Total de URLs: {len(df_combined)}")
    print(f"✅ URLs Legítimas: {len(df_combined[df_combined['label'] == 'legitimate'])}")
    print(f"⚠️  URLs Phishing: {len(df_combined[df_combined['label'] == 'phishing'])}")
    print(f"📁 Guardado en: dataset_combined.csv")
    print(f"{'='*50}\n")
    
    return df_combined

if __name__ == "__main__":
    combine_datasets()