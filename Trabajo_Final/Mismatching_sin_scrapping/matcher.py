# -----------------------------------------------------------
# Código para identificar y clasificar matching/mismatching
# -----------------------------------------------------------

import pandas as pd
from openai import OpenAI
from tqdm import tqdm

# API KEY
client = OpenAI(
    api_key="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"
)


df = pd.read_excel("Base_match_link.xlsx")


df.columns = df.columns.str.strip().str.lower()
df = df.rename(columns={"primer trabajo": "primer_trabajo"})

print("Columnas detectadas:", df.columns)


# -------------------------
# GPT-4.1
# -------------------------


def clasificar_match(carrera, primer_trabajo, empresa):

    prompt = f"""
    Eres un investigador profesional.
    
    Considera la Carrera estudiada por cada individuo. Debes determinar
    si el Primer trabajo del individuo es acorde a la carrera estudiada en 
    cuestión. Si esto es cumple, hay match. Si no se cumple, no hay match.
    Adicionalmente, el cargo debe ser acorde a la calificación del individuo.
    Si el trabajo se encuentra por debajo de la calificación de alguien con 
    un título universitario, es decir, el individuo está sobrecalificado, no 
    hay match.

    Carrera: {carrera}
    Primer trabajo: {primer_trabajo}
    Empresa: {empresa}

    Responde únicamente con:
    1 si es match
    0 si es mismatch
    """

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Eres un experto en clasificación laboral."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


# -------------------------
# GPT-4o-mini
# -------------------------


def clasificar_match_4o(carrera, primer_trabajo, empresa):

    prompt = f"""
    Eres un investigador profesional.
    
    Considera la Carrera estudiada por cada individuo. Debes determinar
    si el Primer trabajo del individuo es acorde a la carrera estudiada en 
    cuestión. Si esto es cumple, hay match. Si no se cumple, no hay match.
    Adicionalmente, el cargo debe ser acorde a la calificación del individuo.
    Si el trabajo se encuentra por debajo de la calificación de alguien con 
    un título universitario, es decir, el individuo está sobrecalificado, no 
    hay match.

    Carrera: {carrera}
    Primer trabajo: {primer_trabajo}
    Empresa: {empresa}

    Responde únicamente con:
    1 si es match
    0 si es mismatch
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un experto en clasificación laboral."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


# Barra de progreso
tqdm.pandas()


# Columna GPT-4.1
df["match(gpt41)"] = df.progress_apply(
    lambda row: clasificar_match(row["carrera"], row["primer_trabajo"], row["empresa"]),
    axis=1,
)


# Columna GPT-4o-mini
df["match(gpt4o)"] = df.progress_apply(
    lambda row: clasificar_match_4o(
        row["carrera"], row["primer_trabajo"], row["empresa"]
    ),
    axis=1,
)


df.to_excel("base_clasificada.xlsx", index=False)

print("Listo. Base guardada como base_clasificada.xlsx")

df.to_excel("base_clasificada.xlsx", index=False)
