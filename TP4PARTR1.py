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

hogares = pd.concat([hog_2025, hog_2005], axis=0, ignore_index=True)
individuos = pd.concat([ind_2025, ind_2005], axis=0, ignore_index=True)

## Se eliminan columnas con datos faltanes

hogares = hogares.dropna(axis=1, how="any")
individuos = individuos.dropna(axis=1, how="any")

## Merge entre individuos y hogares

base_def = individuos.merge(
    hogares,
    on=["CODUSU", "NRO_HOGAR", "ANO4"],
    how="left"
)

# borrar filas con algún valor negativo en columnas numéricas
num_cols = base_def.select_dtypes(include="number").columns
base_def = base_def[(base_def[num_cols] >= 0).all(axis=1)]

## Eliminamos las columnas no necesarias. Por simplicidad, esta parte la hacemos directamente
## en excel. Se eliminan variables que no predicen si una persona está desocupada o lo hacen de
## manera muy indirecta.
downloads = Path.home() / "Downloads"
Base_def = pd.read_excel(downloads / "Base_def.xls")


cols = ['V1','V2','V3','V4','V6','V7','V12','V13','V14','V15','V17','V18','V19_A','V19_B',
        'H15','II3','II6','REALIZADA','CH13','CH09']

for c in cols:
    Base_def[c] = (
        Base_def[c]
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
    
Base_def = Base_def[(Base_def.select_dtypes(include="number") >= 0).all(axis=1)]
Base_def = Base_def.dropna(axis=1, how="any")

cl2 = ["CHO4"]

for c in cl2:
    Base_def[c] = (
        Base_def[c]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace({
            'Varón': 1,
            'Mujer': 2,
        })
    )

from pathlib import Path

downloads = Path.home() / "Downloads"
Base_def.to_excel(downloads / "Base_def_final.xlsx", index=False)

print("Guardado en:", downloads)

## 1.4. Se crean 3 variables adicionales:
    
## La primera es la proporción de personas que trabaja en el hogar.    

Base_def["TRABAJA"] = (
    (Base_def["ESTADO"] == 1) |
    (Base_def["ESTADO"].astype(str).str.upper() == "OCUPADO")
).astype(int)

Base_def["PROP_TRABAJAN_HOGAR"] = (
    Base_def
    .groupby("CODUSU")["TRABAJA"]
    .transform("mean")
)

## La segunda toma el valor 1 si hay menores de 14 años en el hogar. Puede ser 
## un predictor importante en cuanto requiere que la persona dedique más tiempo 
## a quedarse en su casa, especialmente en caso de mujeres.

Base_def["MENOR14HOG"] = (
    Base_def
    .groupby("CODUSU")["CH06"]
    .transform(lambda x: (x < 14).any())
    .astype(int)
)

## Por último, se crea una dummy para hogares que reciben un ingreso no laboral de
## cualquier tipo (subsidio, interés, etc.), descartando pensiones.

ingresos = ["V3", "V4", "V6","V7","V12","V14",'V17','V18','V19_A','V19_B']   

Base_def["ADICIONAL"] = (
    Base_def[ingresos]
    .eq(1)
    .any(axis=1)
    .astype(int)
)

## 1.5

## Se analiza estadística descriptiva de siguientes variables:
    
    ## i) Edad de los encuestados.
    
Base_def["CH06"].agg(
    media="mean",
    mediana="median",
    volatilidad="std",
    max="max",
    min="min"
)

    ## ii) Prob Niños en el hogar
    
Base_def["MENOR14HOG"].agg(
    media="mean",
    mediana="median",
    volatilidad="std",
    max="max",
    min="min"
)

    ## Histograma de edad.
    
    
    ## Desocupados por años de educación.

















