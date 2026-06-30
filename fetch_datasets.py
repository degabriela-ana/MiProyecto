import pandas as pd
import requests
import json
from urllib.parse import urlparse

def fetch_phishtank_data(output_file='phishtank_data.csv'):
    """
    Descarga datos de PhishTank (público)
    PhishTank es una base de datos colaborativa de URLs de phishing
    """
    print("Descargando datos de PhishTank...")
    
    try:
        # PhishTank proporciona un JSON público
        url = "http://data.phishtank.com/data/online-valid.json"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extraer URLs y convertir a DataFrame
            urls = []
            for item in data:
                urls.append({
                    'url': item.get('url', ''),
                    'label': 'phishing'
                })
            
            df = pd.DataFrame(urls)
            print(f"Se descargaron {len(df)} URLs de phishing de PhishTank")
            
            # Guardar a CSV
            df.to_csv(output_file, index=False)
            print(f"Guardado en {output_file}")
            
            return df
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error descargando de PhishTank: {e}")
        return None

def combine_datasets():
    """
    Combina el dataset inicial con los datos descargados
    """
    print("\nCombinando datasets...")
    
    # Leer dataset inicial
    df_initial = pd.read_csv('dataset.csv')
    
    dataframes = [df_initial]
    
    # Intentar descargar de PhishTank
    df_phishtank = fetch_phishtank_data()
    if df_phishtank is not None:
        dataframes.append(df_phishtank)
    
    # Combinar y eliminar duplicados
    df_combined = pd.concat(dataframes, ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=['url'])
    
    # Guardar
    df_combined.to_csv('dataset_combined.csv', index=False)
    
    print(f"\nDataset final: {len(df_combined)} URLs únicas")
    print(f"Legítimas: {len(df_combined[df_combined['label'] == 'legitimate'])}")
    print(f"Phishing: {len(df_combined[df_combined['label'] == 'phishing'])}")
    print(f"Guardado en: dataset_combined.csv")
    
    return df_combined

if __name__ == "__main__":
    combine_datasets()