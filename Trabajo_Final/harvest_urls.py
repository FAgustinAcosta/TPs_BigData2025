import time
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Importamos la configuración que acabamos de crear
from config_carreras import get_search_queries

# Archivos
INPUT_FILE = "lista_universidades_arg.csv"
OUTPUT_FILE = "targets_master_list.csv"
CHECKPOINT_FILE = "targets_checkpoint.csv"


def setup_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    return driver


def get_google_links(driver, query):
    links = set()
    base_url = "https://www.google.com/search?q={}"
    try:
        driver.get(base_url.format(query))
        time.sleep(random.uniform(3, 6))  # Pausa
        anchors = driver.find_elements(By.CSS_SELECTOR, "div.g a")
        for a in anchors:
            href = a.get_attribute("href")
            if href and "linkedin.com/in/" in href:
                # Limpieza extra para sacar parámetros de Google si quedan
                clean_url = href.split("&")[0]
                links.add(clean_url)
    except Exception as e:
        print(f"Error: {e}")
    return list(links)


def main():
    print("--- Iniciando Recolección Inteligente ---")

    # 1. Cargar Universidades
    try:
        df_univ = pd.read_csv(INPUT_FILE)
        universities = df_univ["institution"].tolist()
    except FileNotFoundError:
        print("Falta el archivo de universidades.")
        return

    driver = setup_driver()
    all_data = []
    counter = 0

    try:
        for univ in universities:
            # Obtenemos las queries inteligentes desde nuestro config
            queries = get_search_queries(univ)

            for q_obj in queries:
                career_cat = q_obj["career_category"]
                query_text = q_obj["query"]

                print(f"[{counter}] Buscando: {univ} -> {career_cat}")

                links = get_google_links(driver, query_text)

                for link in links:
                    all_data.append(
                        {
                            "institution_input": univ,
                            "career_category": career_cat,  # Guardamos la categoría general (ej: Economía)
                            "search_query": query_text,
                            "profile_url": link,
                        }
                    )

                print(f"   -> URLs: {len(links)}")
                counter += 1

                # Checkpoint
                if counter % 10 == 0:
                    pd.DataFrame(all_data).to_csv(CHECKPOINT_FILE, index=False)

                time.sleep(random.uniform(6, 10))

    except KeyboardInterrupt:
        print("\n--- Stop Manual ---")

    finally:
        driver.quit()
        if all_data:
            df = pd.DataFrame(all_data)
            df = df.drop_duplicates(subset=["profile_url"])
            df.to_csv(OUTPUT_FILE, index=False)
            print(f"Finalizado. Total URLs: {len(df)}")


if __name__ == "__main__":
    main()
