# harvest_urls.py - VERSIÓN ESCÁNER (REGEX)
import time
import pandas as pd
import random
import sys
import io
import re  # <--- IMPORTANTE: Nueva librería para buscar patrones
from pathlib import Path
from urllib.parse import quote  # Para encodear URLs correctamente
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from config_carreras import get_search_queries

# --- 1. CONFIGURACIÓN DE CONSOLA ---
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

# --- 2. RUTAS ---
REPO_ROOT = Path.cwd()
DATA_DIR = REPO_ROOT / "Datasets"
INPUT_FILE = DATA_DIR / "lista_universidades_arg.csv"
OUTPUT_FILE = DATA_DIR / "dataset_urls_linkedin.csv"
CHECKPOINT_FILE = DATA_DIR / "checkpoint_urls.csv"
DEBUG_DIR = DATA_DIR / "Debug_Screenshots"

# Crear carpetas
DATA_DIR.mkdir(parents=True, exist_ok=True)
DEBUG_DIR.mkdir(parents=True, exist_ok=True)


def setup_driver():
    """Configura Chrome Indetectable con headers realistas y anti-detección avanzada"""
    options = uc.ChromeOptions()

    # --- Argumentos para eludir detección ---
    options.add_argument("--no-first-run")
    options.add_argument("--password-store=basic")
    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )  # Oculta que es automatizado
    options.add_argument("--disable-web-resources")
    options.add_argument("--disable-default-apps")

    # Anti-detección adicional
    options.add_argument("--start-maximized")  # Ventana maximizada
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")  # No cargar imágenes (más rápido)
    options.add_argument("--disable-notifications")

    # User-Agent aleatorio (varía cada ejecución)
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    ]
    user_agent = random.choice(user_agents)
    options.add_argument(f"user-agent={user_agent}")

    # Headers para parecer humano
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.images": 2,  # No cargar imágenes
    }
    options.add_experimental_option("prefs", prefs)

    print(
        ">>> Iniciando Motor de Búsqueda (Modo Bing) con protección anti-detección..."
    )
    try:
        driver = uc.Chrome(options=options, version_main=144, no_sandbox=True)

        # Inyectar JavaScript para ocultar que es automatizado
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['es-AR', 'es'],
                });
            """
            },
        )

        # Agregar headers adicionales
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {
                "userAgent": user_agent,
                "platform": "Win32",
                "platformVersion": "10.0",
            },
        )

        return driver
    except Exception as e:
        print(f"ERROR CRÍTICO: {e}")
        sys.exit(1)


def is_valid_linkedin_profile(profile_id):
    """Valida que sea un perfil real de LinkedIn, no basura"""
    profile_lower = profile_id.lower()

    # ❌ PALABRAS CLAVE DE BASURA
    spam_keywords = [
        "dir",
        "jobs",
        "company",
        "pulse",
        "login",
        "help",
        "talent",
        "recruiter",
        "jobs",
        "feed",
        "messaging",
        "notification",
        "home",
        "mynetwork",
        "learning",
        "legal",
        "shop",
        "contact",
        "api",
        "redirect",
        "account",
        "search",
        "in-",
        "callback",
        "privacy",
        "terms",
    ]

    # Si contiene palabras de spam
    if any(bad in profile_lower for bad in spam_keywords):
        return False

    # Debe tener al menos 3 caracteres
    if len(profile_id) < 3:
        return False

    # No debe ser solo números
    if profile_id.isdigit():
        return False

    # Debe contener al menos una letra
    if not any(c.isalpha() for c in profile_id):
        return False

    # No debe tener patrones sospechosos (muchos guiones, muchos caracteres especiales)
    special_count = sum(1 for c in profile_id if c in "%-")
    if special_count > 3:
        return False

    return True


def get_bing_links(driver, query, univ_name, career_area):
    """
    ESTRATEGIA: Calentar sesión en Bing, luego usar Google.
    Bing calienta la sesión, Google obtiene los resultados.
    """
    links = set()

    # --- PASO 1: CALENTAR EN BING ---
    try:
        bing_url = "https://www.bing.com/search?q=linkedin"
        driver.get(bing_url)
        time.sleep(random.uniform(1.5, 2.5))
    except:
        pass

    # --- PASO 2: USAR GOOGLE PARA LAS BÚSQUEDAS REALES ---
    try:
        search_query = f"site:linkedin.com/in {query}"
        encoded_query = quote(search_query)
        google_url = f"https://www.google.com/search?q={encoded_query}"

        driver.get(google_url)

        print("      ⏳ Google (6s)...", end="", flush=True)
        time.sleep(6)
        print(" ✅")

        # Scroll para parecer humano
        for _ in range(random.randint(2, 3)):
            driver.execute_script(f"window.scrollBy(0, {random.randint(100, 300)});")
            time.sleep(random.uniform(0.5, 1))

        # Buscar resultados en Google
        results_blocks = driver.find_elements(By.XPATH, "//div[@class='g']")

        if not results_blocks:
            results_blocks = driver.find_elements(
                By.XPATH, "//div[contains(@class, 'yuRUbf')]"
            )

        if not results_blocks:
            results_blocks = driver.find_elements(
                By.XPATH, "//div[contains(@class, 'Gx5Zad')]"
            )

        for block in results_blocks:
            try:
                time.sleep(random.uniform(0.2, 0.5))
                block_html = block.get_attribute("outerHTML")
                match = re.search(r"linkedin\.com/in/([a-zA-Z0-9%-]+)", block_html)

                if match:
                    profile_id = match.group(1)
                    if is_valid_linkedin_profile(profile_id):
                        links.add(f"https://www.linkedin.com/in/{profile_id}")

            except Exception:
                continue

    except Exception as e:
        print(f"      ❌ Error: {str(e)[:30]}")

    # Debug si no hay resultados
    if len(links) == 0 and "Teología" not in univ_name:
        try:
            safe_name = f"ERROR_{univ_name[:10]}_{career_area}.png".replace(" ", "")
            driver.save_screenshot(str(DEBUG_DIR / safe_name))
            print(f"      📸 Foto: {safe_name}")
        except:
            pass

    return list(links)


def main():
    print("--- INICIANDO COSECHA (BING→GOOGLE) ---")

    if not INPUT_FILE.exists():
        print(f"ERROR: No encuentro {INPUT_FILE}")
        return

    df_univ = pd.read_csv(INPUT_FILE)
    universities = df_univ["institution"].tolist()

    driver = setup_driver()
    all_data = []

    try:
        for i, univ in enumerate(universities):
            print(f"\n[{i+1}/{len(universities)}] 🏛️  {univ}")

            queries = get_search_queries(univ)

            # En la primera búsqueda, calentar la sesión
            if i == 0:
                print("   🔥 Calentando sesión en Bing (12s)...")
                try:
                    driver.get("https://www.bing.com/search?q=linkedin university")
                    time.sleep(12)
                    print("      ✅ Sesión lista. Cambiando a Google...")
                except:
                    pass

            for q_data in queries:
                area = q_data["area_estudio"]
                query = q_data["query_string"]

                print(f"   🔎 Buscando: {area}...", end=" ")

                urls = get_bing_links(driver, query, univ, area)

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

                # Pausa entre búsquedas
                pausa_busqueda = random.uniform(2, 5)
                time.sleep(pausa_busqueda)

            if all_data:
                pd.DataFrame(all_data).to_csv(CHECKPOINT_FILE, index=False)

            # Pausa mayor entre universidades
            if i < len(universities) - 1:
                pausa = random.uniform(5, 12)
                print(f"   ⏳ Pausa {pausa:.0f}s...")
                time.sleep(pausa)

                # Cada 5 universidades, pausa extra
                if (i + 1) % 5 == 0:
                    pausa_larga = random.uniform(15, 30)
                    print(f"   ⏳ Pausa extra {pausa_larga:.0f}s")
                    time.sleep(pausa_larga)

    except KeyboardInterrupt:
        print("\n🛑 Interrupción manual.")

    finally:
        if driver:
            driver.quit()

        if all_data:
            df = pd.DataFrame(all_data)
            df = df.drop_duplicates(subset=["profile_url"])
            df.to_csv(OUTPUT_FILE, index=False)
            print(f"\n--- ✅ FINALIZADO ---")
            print(f"Total recolectado: {len(df)}")


if __name__ == "__main__":
    main()
