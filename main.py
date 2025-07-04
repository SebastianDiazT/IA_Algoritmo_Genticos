import pandas as pd
import numpy as np
import random

# === Paso 1: Cargar el archivo CSV ===
# Asegúrate de que 'quinua.csv' esté en la misma carpeta que este script
df = pd.read_csv("datos_pivoteados.csv",sep=";")

# Mostrar los primeros registros
print("Primeras filas del dataset:")
print(df.head())

# === Paso 2: Elegir año base y simular parámetros económicos ===
año_base = df["Anio"].max()
datos = df[df["Anio"] == año_base].iloc[0]

rendimiento = datos["Rendimiento (kg/ha)"]

# Simulación de valores económicos
precio_tonelada = 8000  # S/. por tonelada
precio_kg = precio_tonelada / 1000
costo_por_ha = 9000  # S/. por hectárea

print(f"Usando datos del año {año_base}")
print(f"Rendimiento: {rendimiento} kg/ha")
print(f"Precio: S/. {precio_kg:.2f} por kg")
print(f"Costo por hectárea: S/. {costo_por_ha}")


# === Paso 3: Definición de la función de utilidad ===
def utilidad_total(x, df, precio_ton=15000, costo_ha=9000):
    precio_kg = precio_ton / 1000
    utilidad_total = 0
    for _, fila in df.iterrows():
        rendimiento = fila["Rendimiento (kg/ha)"]
        produccion = x * rendimiento
        ingresos = produccion * precio_kg
        costos = x * costo_ha
        utilidad_total += ingresos - costos
    return utilidad_total
def utilidad(x):
    return utilidad_total(x, df, precio_ton=15000, costo_ha=9000)

# === Paso 4: Configuración del algoritmo genético ===
POBLACION_SIZE = 100
GENERACIONES = 300
PROB_CRUCE = 0.7
PROB_MUTACION = 0.1
RANGO_X = (0, 25500)

def inicializar_poblacion():
    return [random.uniform(*RANGO_X) for _ in range(POBLACION_SIZE)]

def cruzar(p1, p2):
    if random.random() < PROB_CRUCE:
        alpha = random.random()
        hijo = alpha * p1 + (1 - alpha) * p2
        return max(RANGO_X[0], min(RANGO_X[1], hijo))
    return p1

def mutar(individuo):
    if random.random() < PROB_MUTACION:
        return max(RANGO_X[0], min(RANGO_X[1], individuo + random.uniform(-500, 500)))
    return individuo

def seleccion_torneo(poblacion, fitness, k=3):
    seleccionados = []
    for _ in range(POBLACION_SIZE):
        aspirantes = random.sample(list(zip(poblacion, fitness)), k)
        seleccionados.append(max(aspirantes, key=lambda x: x[1])[0])
    return seleccionados

# === Paso 5: Ejecución del algoritmo genético ===
poblacion = inicializar_poblacion()
for _ in range(GENERACIONES):
    fitness = [utilidad(x) for x in poblacion]
    seleccionados = seleccion_torneo(poblacion, fitness)
    hijos = [mutar(cruzar(seleccionados[i], seleccionados[(i + 1) % POBLACION_SIZE])) for i in range(POBLACION_SIZE)]
    poblacion = hijos

fitness_final = [utilidad(x) for x in poblacion]
mejor_area = poblacion[fitness_final.index(max(fitness_final))]
mejor_utilidad = max(fitness_final)

# === Resultados ===
print(f"\nÁrea óptima para año {año_base}: {mejor_area:.2f} ha")
print(f"Utilidad máxima estimada: S/. {mejor_utilidad:,.2f}")