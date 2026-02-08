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
        # ==========================================
        # BLOQUE 1: PROFESIONES REGULADAS - MATRÍCULA (Tradicionales)
        # ==========================================
        "Derecho": [
            "Abogacía",
            "Derecho",
            "Abogado",
            "Derecho",
            "Lawyer",
            "Legal",
            "Leyes",
            "Ciencias Jurídicas",
            "Escribanía",
            "Notariado",
            "Procurador",
        ],
        "Psicologia": [
            "Licenciatura en Psicología",
            "Psicología",
            "Psychology",
            "Psicólogo",
            "Salud Mental",
            "Terapeuta Psicológico",
        ],
        "Salud_Medicina": [
            "Medicina",
            "Médico",
            "Medicine",
            "Doctor",
            "Salud",
            "Cirujano",
            "Clínica",
        ],
        "Salud_Otras": [
            "Kinesiología",
            "Fisiatría",
            "Nutrición",
            "Odontología",
            "Farmacia",
            "Bioquímica",
            "Fonoaudiología",
            "Enfermería",
            "Veterinaria",
            "Medicina Veterinaria"
        ],
        "Contador": [
            "Contador Público",
            "Contador Público Nacional",
            "Audit",
            "Impuestos",
            "Taxes",
            "Contabilidad",
            "Auditoría",
            "Impuestos",
        ],
        # ==========================================
        # BLOQUE 2: NEGOCIOS, ECONOMÍA Y GESTIÓN
        # ==========================================
        "Administracion": [
            "Licenciatura en Administración",
            "Administración de Empresas",
            "Business Administration",
            "Management",
            "Economía Empresarial",
            "Actuario",
            "Licenciatura en Administración Pública",
            "Licenciatura en Administración Hotelera",
            ""
        ],
        "Marketing": [
            "Marketing",
            "Comercialización",
            "Mercadotecnia",
            "Publicidad"
        ],
        "Recursos_Humanos": [
            "Licenciatura en Administración de Recursos Humanos",
            "Recursos Humanos",
            "Human Resources",
            "RRHH",
            "Relaciones del Trabajo",
            "Relaciones Laborales",
        ],
        "Economia": [
            "Economía",
            "Economics",
            "Licenciado en Economía",
            "Economista",
            "Economist"
        ],
        # --- BLOQUE 3: STEM (Ingeniería y Tech) ---
        "Sistemas_Informática": [
            "Ingeniería en Sistemas",
            "Ingeniería de Sistemas",
            "Ingeniería en Sistemas de Información",
            "Ingeniería Informática",
            "Ingeniería en Informática",
            "Ciencias de la Computación",
            "Licenciatura en Sistemas",
            "Analista de Sistemas",
            "Sistemas",
            "Computación",
            "Informática",
            "Computer Science",
            "Programación",
            "Programador",
            "Developer",
            "Software",
            "Ingeniería en Computación",
            "Ingeniería en Ciencia de Datos",
            "Ingeniería en Telecomunicaciones",
            "Ingeniería en Transporte"
        ],
        "Ingenierias": [
            "Ingeniería",
            "Engeneering",
            "Bioingeniería",
            "Ingeniería Industrial",
            "Organización Industrial",
            "Ingeniería Civil",
            "Ingeniería Mecánica",
            "Ingeniería Electrónica",
            "Ingeniería en Electrónica",
            "Ingeniería Eléctrica",
            "Ingeniería Electromecánica",
            "Ingeniería Química",
            "Ingeniería en Petróleo",
            "Ingeniería Aeronáutica",
            "Bioingeniería",
            "Ingeniería Matemática",
            "Ingeniería en Inteligencia Artificial",
            "Ingeniería Nuclear",
            "Matemática",
            "Física",
        ],
        "Arquitectura": [
            "Arquitectura",
            "Arquitecto",
            "Architecture",
            "Architect",
            "Diseño",
            "Urbanismo",
        ],
        "Agro": [
            "Ingeniería Agronómica",
            "Agronomía",
            "Ingeniería Ambiental",
            "Ingeniería Zootecnista",
            "Ingeniería en Alimentos",
            "Ingeniería en Recursos Naturales",
            "Ingeniería Forestal"
            "Ingeniería en Agrimensura",
            "Licenciatura en Geología"
            "Geología",
            "Licenciatura en Ciencias Geológicas",
            "Licenciatura en Administración Rural"
        ]
        # --- BLOQUE 4: CIENCIAS SOCIALES Y HUMANAS ---
        "Humanidades": [
            "Licenciatura en Antropología",
            "Licenciatura en Ciencias Sociales",
            "Licenciatura en Sociología",
            "Licenciatura en Filosofía",
            "Filosofía",
            "Licenciatura en Historia",
            "Historia",
            "Licenciatura en Geografía",
            "Geografía"
        ],
        "Comunicación": [
            "Licenciatura en Comunicación Social",
            "Comunicación Social",
            "Periodismo",
            "Communication",
            "Profesorado"
        ],
        "Ciencias_Politicas": [
            "Ciencia Política",
            "Ciencias Políticas",
            "Relaciones Internacionales",
            "Diplomacia",
            "Gobierno y Relaciones Internacionales",
            "Comercio Exterior",
            "Comercio Internacional",
            "Licenciatura en Comercio",
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
