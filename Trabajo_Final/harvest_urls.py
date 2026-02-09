# harvest_urls.py - VERSIÓN BING (CERO CAPTCHAS)
import time
import pandas as pd
import random
import sys
import io
from pathlib import Path
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from config_carreras import get_search_queries

# --- FIX DE CODIFICACIÓN (Para ver mensajes en tiempo real) ---
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

# --- RUTAS ---
REPO_ROOT = Path.cwd()
DATA_DIR = REPO_ROOT / "Datasets"
INPUT_FILE = DATA_DIR / "lista_universidades_arg.csv"
OUTPUT_FILE = DATA_DIR / "dataset_urls_linkedin.csv"
CHECKPOINT_FILE = DATA_DIR / "checkpoint_urls.csv"

# Crear carpeta de datasets si no existe
DATA_DIR.mkdir(parents=True, exist_ok=True)


def setup_driver():
    """Configura Chrome Indetectable"""
    options = uc.ChromeOptions()
    options.add_argument("--no-first-run")
    options.add_argument("--password-store=basic")
    # options.add_argument("--headless") # Descomentar si quieres ocultar la ventana

    print(">>> Iniciando Motor de Búsqueda (Modo Bing)...")
    try:
        # Usamos versión 144 o la que detecte automática
        driver = uc.Chrome(options=options, version_main=144)
        return driver
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def get_bing_links(driver, query):
    """
    Versión FINAL BLINDADA:
    Solo acepta enlaces que contengan 'linkedin.com/in/'.
    Rechaza explícitamente a Copilot, Bing y basura.
    """
    links = set()
    base_url = "https://www.bing.com/search?q={}"

    try:
        driver.get(base_url.format(query))
        time.sleep(random.uniform(3, 5))

        # 1. Traemos TODOS los links de la página
        anchors = driver.find_elements(By.TAG_NAME, "a")

        for a in anchors:
            try:
                href = a.get_attribute("href")

                # --- FILTRO 1: EXISTENCIA ---
                if not href:
                    continue

                # --- FILTRO 2: LA REGLA DE ORO ---
                # Si no dice "linkedin.com/in/", NO ES UN PERFIL.
                # Esto mata al link de Copilot inmediatamente.
                if "linkedin.com/in/" not in href:
                    continue

                # --- FILTRO 3: SEGURIDAD EXTRA ---
                # Por si acaso algún link raro de publicidad se disfraza
                if "bing.com" in href or "google.com" in href:
                    continue

                # Si llegamos aquí, ES UN PERFIL REAL
                clean_link = href.split("?")[0].split("&")[0]
                links.add(clean_link)

            except:
                continue

    except Exception as e:
        print(f"Error en búsqueda: {e}")

    return list(links)


def main():
    print("--- INICIANDO COSECHA DE PERFILES (VÍA BING) ---")

    if not INPUT_FILE.exists():
        print(f"ERROR: No encuentro {INPUT_FILE}")
        return

    # 1. Cargar Universidades
    df_univ = pd.read_csv(INPUT_FILE)
    universities = df_univ["institution"].tolist()

    # 2. Verificar Checkpoint (Resume)
    start_index = 0
    # Si quieres retomar, podrías implementar lógica aquí,
    # por ahora empieza de cero o sobreescribe.

    # 3. Iniciar Navegador
    driver = setup_driver()
    all_data = []

    try:
        # Loop Principal
        for i, univ in enumerate(universities):
            print(f"\n[{i+1}/{len(universities)}] 🏛️  {univ}")

            queries = get_search_queries(univ)

            for q_data in queries:
                area = q_data["area_estudio"]
                query = q_data["query_string"]

                print(f"   🔎 Buscando: {area}...", end=" ")

                # Usamos la función de BING
                urls = get_bing_links(driver, query)

                if urls:
                    print(f"✅ {len(urls)} resultados.")
                    for url in urls:
                        all_data.append(
                            {
                                "university_query": univ,
                                "career_area": area,
                                "profile_url": url,
                            }
                        )
                else:
                    print("❌ 0 resultados.")

            # Guardado parcial cada 1 universidad (Más seguro)
            if all_data:
                pd.DataFrame(all_data).to_csv(CHECKPOINT_FILE, index=False)

    except KeyboardInterrupt:
        print("\n🛑 Interrupción manual.")

    finally:
        if driver:
            driver.quit()

        if all_data:
            df = pd.DataFrame(all_data)
            # Eliminamos duplicados antes de guardar final
            df = df.drop_duplicates(subset=["profile_url"])
            df.to_csv(OUTPUT_FILE, index=False)
            print(f"\n--- ✅ FINALIZADO ---")
            print(f"Total perfiles: {len(df)}")
            print(f"Archivo guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
