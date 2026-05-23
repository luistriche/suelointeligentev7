# ======================================================
# SUELO INTELIGENTE - Viabilidad para Cultivo de Vid
# Dispositivo: Medidor Inteligente de Suelo 6 en 1 (ST03)
# Algoritmo: K-Neighbors Classifier (KNN, k=5)
# Enfoque: Reporte Ejecutivo para Inversionistas
# ======================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

# ======================================================
# 1. Simulación de Datos (Optimizada para Presentación)
# Usamos Distribución Normal centrada en el clima de Tijuana
# ======================================================
np.random.seed(42)
n_muestras = 150

datos_medidor = {
    # Conductividad moderada
    'Fertilidad_uS_cm': np.random.normal(1200, 300, n_muestras).clip(0, 3000).astype(int),
    # Centrado en 25% (Suelo con buen drenaje, ideal < 40%)
    'Humedad_Suelo_pct': np.random.normal(25, 8, n_muestras).clip(0, 99).astype(int),
    # Centrado en 6.8 (Óptimo para la vid entre 6.0 y 7.5)
    'pH': np.round(np.random.normal(6.8, 0.4, n_muestras).clip(3.5, 9.0), 1),
    # Centrado en 20°C (Clima templado ideal)
    'Temperatura_C': np.round(np.random.normal(20, 3, n_muestras).clip(0, 50), 1),
    # Días soleados en B.C. (Alto LUX)
    'Luz_Solar_LUX': np.random.normal(75000, 10000, n_muestras).clip(0, 100000).astype(int),
    # Clima árido/seco (Ideal < 50%)
    'Humedad_Amb_pct': np.random.normal(35, 10, n_muestras).clip(0, 99).astype(int)
}

df = pd.DataFrame(datos_medidor)

# ======================================================
# 2. Etiquetado: Condiciones idóneas para la Vid
# ======================================================
def evaluar_vid(fila):
    ph_ok = 6.0 <= fila['pH'] <= 7.5
    temp_ok = 15.0 <= fila['Temperatura_C'] <= 25.0
    humedad_amb_baja = fila['Humedad_Amb_pct'] < 50
    buen_drenaje = fila['Humedad_Suelo_pct'] < 40 
    buena_luz = fila['Luz_Solar_LUX'] > 50000     
    
    condiciones_cumplidas = sum([ph_ok, temp_ok, humedad_amb_baja, buen_drenaje, buena_luz])
    return 1 if condiciones_cumplidas >= 3 else 0

df['Viabilidad_Vid'] = df.apply(evaluar_vid, axis=1)

# ======================================================
# 3. Preparación y Entrenamiento del Modelo KNN
# ======================================================
X = df.drop('Viabilidad_Vid', axis=1)
y = df['Viabilidad_Vid']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)

# ======================================================
# 4. Visualización Gráfica para la Presentación
# ======================================================
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='pH', y='Humedad_Suelo_pct', 
                hue='Viabilidad_Vid', size='Luz_Solar_LUX', sizes=(20, 250), 
                palette={0: '#e74c3c', 1: '#2ecc71'}, alpha=0.8)

plt.axvline(x=6.0, color='gray', linestyle='--', label='Min pH (6.0)')
plt.axvline(x=7.5, color='gray', linestyle='--', label='Max pH (7.5)')
plt.axhline(y=40, color='blue', linestyle='--', label='Max Humedad (<40%)')

plt.title('Análisis de Parcela: Zona de Viabilidad para la Vid', fontsize=14, fontweight='bold')
plt.xlabel('Nivel de pH (Óptimo entre 6.0 y 7.5)', fontsize=12)
plt.ylabel('Humedad del Suelo % (Óptimo < 40%)', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# ======================================================
# 5. Generador de Reporte Ejecutivo
# ======================================================
def reporte_inversionista(fertilidad, humedad_suelo, ph, temp, luz, humedad_amb):
    nombres_columnas = ['Fertilidad_uS_cm', 'Humedad_Suelo_pct', 'pH', 
                        'Temperatura_C', 'Luz_Solar_LUX', 'Humedad_Amb_pct']
    
    nueva_lectura = pd.DataFrame([[fertilidad, humedad_suelo, ph, temp, luz, humedad_amb]], 
                                 columns=nombres_columnas)
    
    lectura_escalada = scaler.transform(nueva_lectura)
    
    probabilidades = knn.predict_proba(lectura_escalada)[0]
    porcentaje_exito = probabilidades[1] * 100 
    
    print("\n" + "="*60)
    print("📊 REPORTE EJECUTIVO DE VIABILIDAD AGRÍCOLA - BLVD 2000")
    print("="*60)
    
    print(f"ÍNDICE DE VIABILIDAD CALCULADO: {porcentaje_exito:.1f}%\n")
    
    if porcentaje_exito >= 60.0:
        print("✅ VEREDICTO: TERRENO ALTAMENTE RENTABLE PARA LA VID.")
        print("Recomendación: Proceder con la planeación de siembra. El suelo presenta las")
        print("condiciones de estrés hídrico y acidez óptimas para uva de calidad enológica.")
    else:
        print("❌ VEREDICTO: TERRENO DE ALTO RIESGO / NO APTO ACTUALMENTE.")
        print("Recomendación: Detener inversión en plantío de vid hasta acondicionar el suelo.")
        print("Se requiere tratamiento intensivo de la tierra para mitigar riesgos de pérdida.")
        
    print("\n--- DESGLOSE DE VARIABLES DEL SENSOR ST03 ---")
    
    print(f"1. pH del Suelo: {ph}")
    if 6.0 <= ph <= 7.5:
        print("   -> Excelente. Permite la correcta absorción de nutrientes.")
    else:
        print("   -> Riesgo. Fuera del rango óptimo (6.0 - 7.5).")

    print(f"2. Humedad del Suelo: {humedad_suelo}%")
    if humedad_suelo < 40:
        print("   -> Excelente. Buen drenaje detectado, previene la pudrición de raíz.")
    else:
        print("   -> Riesgo. Suelo demasiado húmedo/encharcado para la vid.")
        
    print(f"3. Temperatura Radicular: {temp}°C")
    if 15.0 <= temp <= 25.0:
        print("   -> Excelente. Clima de subsuelo ideal para el desarrollo de la vid.")
    else:
        print("   -> Riesgo. Temperatura fuera de la zona de confort de la planta.")

    print(f"4. Luz Solar Receptada: {luz} LUX")
    if luz > 50000:
        print("   -> Excelente. Exposición solar alta, vital para la fotosíntesis y azúcar.")
    else:
        print("   -> Riesgo. Zona muy sombreada, afectará la maduración de la uva.")
        
    print(f"5. Humedad Ambiental: {humedad_amb}%")
    if humedad_amb < 50:
        print("   -> Excelente. Clima seco que evita la proliferación de hongos.")
    else:
        print("   -> Riesgo. Demasiada humedad en el aire, propenso a enfermedades.")
        
    print(f"6. Fertilidad (Conductividad): {fertilidad} uS/cm")
    print("   -> Indicador base de sales minerales disponibles. Se ajustará con fertirriego.")
    print("="*60)

# ======================================================
# 6. Prueba final para la presentación
# ======================================================
# Lectura ideal para cerrar con broche de oro la presentación:
reporte_inversionista(fertilidad=1250, humedad_suelo=22, ph=6.8, temp=21.5, luz=85000, humedad_amb=30)