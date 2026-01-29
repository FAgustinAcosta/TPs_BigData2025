# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

## Pregunta 1.2 

import pandas as pd
from pathlib import Path

# Ruta a Descargas
downloads = Path.home() / "Downloads"

# Cargar bases 2005 desde Descargas
ind_2005 = pd.read_stata(downloads / "Individual_T105.dta")
hog_2005 = pd.read_stata(downloads / "Hogar_t105.dta")
ind_2025 = pd.read_excel(downloads / "usu_individual_T125.xls")
hog_2025 = pd.read_excel(downloads / "usu_hogar_T125.xls")

hog_2005.info()
ind_2005.head()
ind_2025.head()



ind_2025 = ind_2025[ind_2025["AGLOMERADO"] == 3]
hog_2025 = hog_2025[hog_2025["AGLOMERADO"] == 3]

hog_2005.head()

ind_2005 = ind_2005[ind_2005["aglomerado"] == "Bahía Blanca - Cerri"]
hog_2005 = hog_2005[hog_2005["aglomerado"] == "Bahía Blanca - Cerri"]

## Pasamos todos los nombres a mayuscula

hog_2005.columns = hog_2005.columns.str.upper()
ind_2005.columns = ind_2005.columns.str.upper()

## Se une respectivamente a hogares e individuos en dos bases únicas.

hogares = pd.concat(
    [hog_2005, hog_2025],
    axis=0,        # filas
    join="outer",  # conserva todas las columnas
    ignore_index=True
)

individuos = pd.concat(
    [ind_2005, ind_2025],
    axis=0,        
    join="outer",  
    ignore_index=True
)

## Merge entre individuos y hogares

base_def = individuos.merge(
    hogares,
    on=["CODUSU", "NRO_HOGAR", "ANO4"],
    how="left"
)

## Dejamos Nan para valores negativos

import numpy as np

num_cols = base_def.select_dtypes(include="number").columns
base_def[num_cols] = base_def[num_cols].where(base_def[num_cols] >= 0, np.nan)

## Filtrar para que columnas digan Si o No
cols = ['V1','V2','V3','V4','V6','V7','V12','V13','V14','V15','V17','V18','V19_A','V19_B',
        'H15','II3','II6','REALIZADA','CH13','CH09']

for c in cols:
    base_def[c] = (
        base_def[c]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace({
            '1': 1,
            '2': 2,
            'si': 1,
            'sí': 1,
            'no': 2
        })
    )
    
    
    
## Se crean 3 variables adicionales:

import numpy as np

# ============================
## 1) Máxima educación en el hogar (max_ed_h)
# ============================
    # -> Indica el nivel educativo más alto alcanzado por algún miembro del hogar. Da idea del clima educativo del hogar capturando el "techo" de capital humano y de posibilidad de "efecto par" (efecto impulso a los demás miembros), que puede influir en la probabilidad de desocupación. Más detalle en el documento.

# Paso A: Trabajar la variable NIVEL_ED de la EPH.
# En la EPH, NIVEL_ED toma los valores 1 a 6 de manera incremental en el nivel educativo alcanzado, pero el valor 7 indica "sin instrucción". Por lo tanto, para mantener la lógica incremental, reasignamos el valor 0 a "sin instrucción". La variable NIVEL_ED computa con el valor 9 los casos de "no sabe" o "no responde", los cuales convertimos a NaN para que no afecten el cálculo de la nueva variable.

base_def["NIVEL_ED"] = base_def["NIVEL_ED"].replace({7: 0, 9: np.nan}) # 'Ns/Nr' -> NaN ; 'Sin instrucción' -> 0.

# Paso B: Cálculo de la variable max_ed_h.
base_def['max_ed_h'] = base_def.groupby(['CODUSU', 'NRO_HOGAR'])['NIVEL_ED'].transform('max')
# 'transform' calcula el max del grupo y lo pega en todas las filas de ese grupo.

print("1ra variable creada: 'max_ed_h'")

## pasamos strings de base del 2005 a nros del 2025

base_def["max_ed_h"] = base_def["max_ed_h"].map({
    "Primaria Incompleta": 1,
    "Primaria Incompleta (incluye educación especial)": 1,
    "Primaria Completa": 2,
    "Secundaria Incompleta": 3,
    "Secundaria Completa": 4,
    "Superior Universitaria Incompleta": 5,
    "Superior Universitaria Completa": 6,
    "Sin instrucción": 1,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 4,
    6: 5,
    7: 6,
    8: 6
})


# ============================
## 2) Tasa de "dependencia" (tdep)
# ============================
    # -> Relación entre miembros dependientes (menores de 14 años y mayores de 65 años) y miembross en edad activa (14 a 65 años) en el hogar. Puede ser un predictor importante en cuanto a que requiere que la persona dedique más tiempo a quedarse en su casa, especialmente en caso de mujeres.  Más detalle en el documento.

base_def['CH06'] = pd.to_numeric(base_def['CH06'], errors='coerce')

    
# Paso A: crear dummies auxiliares para dependientes (menores de 14 años y mayores de 65 años) y en edad activa (entre 14 y 65 años).
base_def['es_dependiente'] = np.where((base_def['CH06'] < 14) | (base_def['CH06'] > 65), 1, 0)
base_def['edad_activa'] = np.where((base_def['CH06'] >= 14) & (base_def['CH06'] <= 65), 1, 0)

# Paso B: Cálculo de las sumas por hogar.
cant_dep = base_def.groupby(['CODUSU', 'NRO_HOGAR'])['es_dependiente'].transform('sum')
cant_edad_act = base_def.groupby(['CODUSU', 'NRO_HOGAR'])['edad_activa'].transform('sum')
# Usamos transform('sum') para tener el total del hogar repetido en cada fila

# Paso C: Cálculo de la tasa de dependencia.
# 1. Calculamos primero una tasa de dependencia temporal con NaN para no romper nada
tasa_temp = cant_dep / cant_edad_act.replace(0, np.nan)
    
# 2. Reemplazamos los infinitos (NaNs por div/0) con el valor máximo de la muestra + un delta
max_val = tasa_temp.max() # Máximo de la muestra
delta = tasa_temp[tasa_temp > 0].min()  # delta = Mínimo positivo de la muestra
# Fallback por seguridad: si delta es NaN (ej. toda la muestra es 0), usar un default
if pd.isna(delta): 
    delta = 0.01 # Cappeo arbitrario en caso de delta NaN.

base_def['tdep'] = tasa_temp.fillna(max_val + delta)
    
# Estamos "cappeando" la tasa de dependencia en casos de completa dependencia asignando un límite superior razonable, ya que si un hogar no tiene miembros en edad activas (denominador 0) pero sí tiene dependientes, la tasa es teóricamente infinita. Económicamente, esto indica dependencia máxima. Por ende, de esta manera se mantiene el orden relativo entre hogares (estos hogares tienen la mayor dependencia).

# Establecemos ese delta lo "menos arbitrario" posible, utilizando el valor mínimo positivo de la tasa en la muestra. Con este criterio, se mantiene el orden relativo (ranking) poniendo a los de "infinita" dependencia en la cima utilizando una brecha "data-driven" con el "salto mínimo" de dependencia observado en la muestra.
    
# Vemos valores
print(f"Máximo finito: {max_val:.4f} | Delta (mínimo positivo): {delta:.4f}")
print(f"Valor imputado a casos sin activos: {max_val + delta:.4f}")
    
print("2da variable creada: 'tdep'")

# ============================
## 3) Ingreso Adicional
# ============================

ingresos_no_lab = ["V3", "V4", "V5", "V6", "V7", "V12", "V14",
                   "V17", "V18", "V19_A", "V19_B"]

# Armonización de V5 entre bases 2005 y 2025
cols_v5_desag = ['V5_1', 'V5_2', 'V5_3']
cols_presentes = [c for c in cols_v5_desag if c in base_def.columns]

if cols_presentes:
    v5_combinada = (
        base_def[cols_presentes]
        .replace({1: 1, 2: 0})
        .fillna(-1)
        .max(axis=1)
        .replace(-1, np.nan)
    )

    base_def['V5'] = base_def['V5'].fillna(v5_combinada)

# Limpieza: borrar columnas desagregadas
base_def.drop(columns=cols_presentes, inplace=True, errors='ignore')

print("Armonización V5 completada (respetando Missings reales).")

# Creación de ADICIONAL a nivel hogar

# 1) Pasamos a binario (1 = sí, todo lo demás = 0)
subset = (
    base_def[ingresos_no_lab]
    .apply(pd.to_numeric, errors="coerce")
    .replace({1: 1, 2: 0})
    .fillna(0)
)

# 2) Indicador a nivel individuo
flag_ind = subset.max(axis=1)

# 3) Colapsamos a nivel hogar
base_def['flag_hogar_adic'] = (
    flag_ind
    .groupby([base_def['CODUSU'], base_def['NRO_HOGAR']])
    .transform('max')
)

# 4) Dummy final según regla
base_def['ADICIONAL'] = np.where(
    base_def['flag_hogar_adic'] == 1, 1, 2
)

# Limpieza
base_def.drop(columns='flag_hogar_adic', inplace=True)

print("Variable ADICIONAL creada")
print(base_def['ADICIONAL'].value_counts(dropna=False))

## 1.5 Estadística Descriptiva

## Se realiza estadística descriptiva de las tres variables creadas. Adicionalmente,
## se agregan dos variables ya existentes.

## i) Maxima educación en el Hogar.

import matplotlib.pyplot as plt

# Conteo ordenado
counts = base_def['max_ed_h'].value_counts().sort_index()

# Gráfico de barras
plt.bar(counts.index, counts.values)

# Etiquetas del eje X
plt.xticks(
    ticks=counts.index,
    labels=[
        'Primaria Incompleta',
        'Primaria Completa',
        'Secundaria Incompleta/EGB',
        'Secundaria completa',
        'Universitaria Incompleta/Terciaria',
        'Universitaria'
    ],
    rotation=30,
    ha='right'
)

plt.ylabel('Frecuencia')
plt.title('Máximo nivel de educación alcanzado por hogar')

plt.show()


## ii) Tasa de dependencia.




## iii) Ingreso Adicional

# Variable a graficar
counts = base_def['ADICIONAL'].value_counts().sort_index()

# Labels para 1 y 2
labels_map = {
    1: 'Hogar recibe ingreso adicional',
    2: 'Hogar no recibe ingreso adicional'
}

labels = [labels_map.get(i, str(i)) for i in counts.index]

plt.figure(figsize=(6, 6))
plt.pie(
    counts.values,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90
)

plt.title('Fracción de Hogares que reportan ingreso adicional')
plt.axis('equal')

plt.show()












