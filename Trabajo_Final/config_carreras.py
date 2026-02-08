# config_carreras.py

# Diccionario de Búsqueda:
# Clave: Nombre genérico (para tu archivo)
# Valor: Lista de keywords que se usarán en Google


def get_search_queries(university):
    """
    Genera queries para las carreras más pobladas y representativas de Argentina.
    Cubrimos: Salud, Derecho, Ingeniería, Económicas, Sociales y Tecnología.
    """

    carreras_target = {
        # --- BLOQUE 1: MATRÍCULA MASIVA (Tradicionales) ---
        "Derecho": ["Abogacía", "Abogado", "Derecho", "Lawyer", "Legal", "Leyes"],
        "Psicologia": ["Psicología", "Psychology", "Psicólogo", "Salud Mental"],
        "Medicina": ["Medicina", "Médico", "Medicine", "Doctor", "Salud"],
        "Contador": ["Contador Público", "Audit", "Impuestos", "Taxes", "Contabilidad"],
        # --- BLOQUE 2: NEGOCIOS Y ECONOMÍA ---
        "Administracion": [
            "Administración de Empresas",
            "Business Administration",
            "Management",
            "MBA",
        ],
        "Marketing": ["Marketing", "Publicidad"],
        "Recursos_Humanos": [
            "Recursos Humanos",
            "Human Resources",
            "RRHH",
            "Relaciones Laborales",
        ],
        "Economia": [
            "Economía",
            "Economics",
            "Licenciado en Economía",
            "Economista",
        ],
        # --- BLOQUE 3: STEM (Ingeniería y Tech) ---
        "Sistemas_Informatica": [
            "Sistemas",
            "Computación",
            "Informática",
            "Computer Science",
            "Programador",
            "Developer",
            "Software",
        ],
        "Ingenieria_General": [  # Agrupamos las industriales/civiles que son masivas
            "Ingeniería Industrial",
            "Ingeniería Civil",
            "Ingeniero",
            "Engineering",
        ],
        "Arquitectura": ["Arquitectura", "Arquitecto", "Architecture", "Architect"],
        # --- BLOQUE 4: CIENCIAS SOCIALES Y HUMANAS ---
        "Comunicacion": [
            "Comunicación Social",
            "Periodismo",
            "Communication",
        ],
    }

    queries = []

    for area, keywords in carreras_target.items():
        # Construimos el OR string: ("Term1" OR "Term2")
        # Esto le dice a Google: "Dame cualquiera de estos títulos asociado a esta Universidad"
        or_group = " OR ".join([f'"{k}"' for k in keywords])

        # Query final: site:ar.linkedin.com/in/ "Universidad X" ("Abogado" OR "Lawyer"...)
        full_query = f'site:ar.linkedin.com/in/ "{university}" ({or_group})'

        queries.append({"area_estudio": area, "query_string": full_query})

    return queries
