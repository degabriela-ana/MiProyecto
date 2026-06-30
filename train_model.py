import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle

def train_model(features_file='features_dataset.csv'):
    """
    Entrena un modelo Random Forest para detectar phishing
    """
    print("Cargando características...")
    df = pd.read_csv(features_file)
    
    # Separar características y etiquetas
    X = df.drop('label', axis=1)
    y = df['label']
    
    print(f"Dataset: {len(X)} muestras")
    print(f"Características: {X.shape[1]}")
    print(f"Distribución: {y.value_counts().to_dict()}")
    
    # Dividir en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nEntrenamiento: {len(X_train)} muestras")
    print(f"Prueba: {len(X_test)} muestras")
    
    # Entrenar modelo
    print("\nEntrenando modelo Random Forest...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Predicciones
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Métricas
    print("\n" + "="*50)
    print("RESULTADOS DEL ENTRENAMIENTO")
    print("="*50)
    
    print("\nEntrenamiento:")
    print(f"  Accuracy: {accuracy_score(y_train, y_pred_train):.4f}")
    print(f"  Precision: {precision_score(y_train, y_pred_train):.4f}")
    print(f"  Recall: {recall_score(y_train, y_pred_train):.4f}")
    print(f"  F1-Score: {f1_score(y_train, y_pred_train):.4f}")
    
    print("\nPrueba:")
    print(f"  Accuracy: {accuracy_score(y_test, y_pred_test):.4f}")
    print(f"  Precision: {precision_score(y_test, y_pred_test):.4f}")
    print(f"  Recall: {recall_score(y_test, y_pred_test):.4f}")
    print(f"  F1-Score: {f1_score(y_test, y_pred_test):.4f}")
    
    # Matriz de confusión
    cm = confusion_matrix(y_test, y_pred_test)
    print(f"\nMatriz de confusión:")
    print(f"  TN: {cm[0,0]}, FP: {cm[0,1]}")
    print(f"  FN: {cm[1,0]}, TP: {cm[1,1]}")
    
    # Guardar modelo
    print("\nGuardando modelo...")
    with open('phishing_detector_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('feature_names.pkl', 'wb') as f:
        pickle.dump(X.columns.tolist(), f)
    
    print("Modelo guardado en: phishing_detector_model.pkl")
    
    return model

if __name__ == "__main__":
    train_model()