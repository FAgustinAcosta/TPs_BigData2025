import pandas as pd
from pathlib import Path


def generate_manual_list():
    """
    Genera un padrón maestro de universidades argentinas categorizadas.
    Fuente combinada: Centro Interuniversitario Nacional (CIN), Consejo de Rectores de Universidades Privadas (CRUP), y contrastando con la Base de Títulos Universitarios de la Dirección Nacional de Gestión Universitaria.
    """

    # Se configura la ruta a bases de datos
    repo_root = Path.cwd()  # asume que el kernel se lanzó desde la raíz del repo
    data_dir = (
        repo_root / "Datasets"
    )  # subcarpeta 'Datasets' del Trabajo_Final del repo

    universidades = [
        # --- UNIVERSIDADES NACIONALES ---
        "Universidad Nacional del Alto Uruguay",
        "Universidad Nacional de las Artes",
        "Universidad Nacional Arturo Jauretche",
        "Universidad Autónoma de Entre Ríos",
        "Universidad Nacional de Avellaneda",
        "Universidad de Buenos Aires",
        "Universidad Nacional de Catamarca",
        "Universidad Nacional del Centro de la Provincia de Buenos Aires",
        "Universidad Nacional del Chaco Austral",
        "Universidad Nacional de Chilecito",
        "Universidad del Chubut",
        "Universidad de la Ciudad de Buenos Aires",
        "Universidad Nacional del Comahue",
        "Universidad Nacional de los Comechingones",
        "universidad Nacional de Córdoba",
        "Universidad Provincial de Córdoba",
        "Universidad Nacional de Cuyo",
        "Universidad de la Defensa Nacional",
        "Universidad Nacional del Delta",
        "Universidad Nacional de Entre Ríos",
        "Universidad Provincial de Ezeiza",
        "Universidad Nacional de Formosa",
        "Universidad Nacional de General Sarmiento",
        "Universidad Nacional Guillermo Brown",
        "Universidad Nacional de Hurlingham",
        "Instituto Universitario de la Gendarmería Nacional Argentina",
        "Instituto Universitario de la Policía Federal Argentina",
        "Instituto Universitario Policial Provincial Juan Vucetich",
        "Instituto Universitario Provincial de Seguridad",
        "Instituto Universitario de Seguridad de la Ciudad",
        "Instituto Universitario de Seguridad Marítima",
        "Instituto Universitario Patagónico de las Artes",
        "Universidad Nacional de José C. Paz",
        "Universidad Nacional de Jujuy",
        "Universidad Provincial de Laguna Blanca",
        "Universidad Nacional de La Matanza",
        "Universidad Nacional de La Pampa",
        "Universidad Nacional de La Rioja",
        "Universidad Nacional de Lanús",
        "Universidad Nacional del Litoral",
        "Universidad Nacional de Lomas de Zamora",
        "Universidad Nacional de Luján",
        "Universidad Nacional Madres de Plaza de Mayo",
        "Universidad Nacional de Mar del Plata",
        "Universidad Nacional de Misiones",
        "Universidad Nacional de Moreno",
        "Universidad Nacional del Nordeste",
        "Universidad Nacional del Noroeste de la Provincia de Buenos Aires",
        "Universidad Nacional del Oeste",
        "Universidad Nacional de la Patagonia San Juan Bosco",
        "Universidad Nacional de la Patagonia Austral",
        "Universidad Pedagógica Nacional",
        "Universidad Nacional del Pilar",
        "Universidad Nacional de Quilmes",
        "Universidad Nacional de Rafaela",
        "Universidad Nacional Raúl Scalabrini Ortiz",
        "Universidad Nacional de Río Cuarto",
        "Universidad Nacional de Río Negro",
        "Universidad Nacional de Río Tercero",
        "Universidad Nacional de Rosario",
        "Universidad Nacional de Salta",
        "Universidad Nacional de San Antonio de Areco",
        "Universidad Nacional de San Juan",
        "Universidad Nacional de San Martín",
        "Universidad Nacional de Santiago del Estero",
        "Universidad Provincial del Sudoeste",
        "Universidad Nacional del Sur",
        "Universidad Tecnológica Nacional",
        "Universidad Nacional de Tierra del Fuego",
        "Universidad Nacional de Tucumán",
        "Universidad Nacional de Villa María",
        "Universidad Nacional de Villa Mercedes",
        # --- UNIVERSIDADES PRIVADAS ---
        "Universidad de la Integración Sudamericana",
        "Instituto Universitario del Agua y el Saneamiento",
        "Instituto Universitario CIAS",
        "Universidad Patagonia Argentina",
        "Universidad Evangélica",
        "Instituto Universitario Isaac Abarbanel",
        "Instituto Universitario de Ciencias Empresariales",
        "Instituto Universitario Para el Desarrollo Productivo y Tecnológico Empresarial de la Argentina",
        "Universidad Metropolitana para la Educación y el Trabajo",
        "Instituto Universitario CEMIC",
        "Instituto Universitario 'Escuela de Medicina del Hospital Italiano'",
        "Instituto Tecnológico de Buenos Aires",
        "Universidad del Gran Rosario",
        "Instituto Universitario de Salud Mental",
        "Instituto Universitario de Ciencias de la Salud 'Fundación H. A. Barceló'",
        "Universidad Salesiana",
        "Universidad Católica de las Misiones",
        "Universidad de San Isidro 'Dr. Plácido Marín'",
        "Instituto Universitario YMCA",
        "Instituto Universitario ESEADE",
        "Instituto Universitario Italiano de Rosario",
        "Escuela Universitaria de Teología",
        "Instituto Universitario de Ciencias Biomédicas de Córdoba",
        "Universidad Escuela Argentina de Negocios",
        "Instituto Universitario River Plate",
        "Universidad del Este",
        "Universidad Gastón Dachary",
        "Universidad de San Pablo-T",
        "Universidad Favaloro",
        "Universidad del CEMA",
        "Universidad Abierta Interamericana",
        "Universidad de Congreso",
        "Universidad de la Cuenca del Plata",
        "Universidad de Flores",
        "Universidad Atlántida Argentina",
        "Universidad del Cine",
        "Universidad del Centro Educativo Latinoamericano",
        "Universidad del Norte Santo Tomás de Aquino",
        "Universidad Torcuato Di Tella",
        "Universidad Blas Pascal",
        "Universidad Maimónides",
        "Universidad de Palermo",
        "Universidad de Ciencias Empresariales y Sociales",
        "Universidad Champagnat",
        "Universidad Austral",
        "Universidad Adventista del Plata",
        "Universidad Notarial Argentina",
        "Universidad Juan Agustín Maza",
        "Universidad ISALUD",
        "Universidad de la Marina Mercante",
        "Universidad del Salvador",
        "Universidad del Museo Social Argentino",
        "Universidad del Aconcagua",
        "Universidad de Morón",
        "Universidad de Mendoza",
        "Universidad de Concepción del Uruguay",
        "Universidad de Belgrano",
        "Universidad Católica de Santiago del Estero",
        "Universidad Católica de Santa Fe",
        "Universidad Católica de La Plata",
        "Universidad Católica de Cuyo",
        "Universidad Católica de Córdoba",
        "Universidad Argentina John F. Kennedy",
        "Universidad Argentina de la Empresa",
        "Pontificia Universidad Católica Argentina",
        "Universidad CAECE",
        "Universidad Católica de Salta",
        "Universidad FASTA",
        "Universidad Siglo 21",
        "Universidad de San Andrés",
    ]

    # Creamos el DataFrame
    df = pd.DataFrame(universidades, columns=["institution"])

    # Limpieza
    df["institution"] = df["institution"].str.strip()
    df = df.drop_duplicates().sort_values("institution")

    # Guardamos en la subcarpeta
    df.to_csv(
        data_dir / "lista_universidades_arg.csv", index=False, encoding="utf-8-sig"
    )

    print(f"--- ¡Padrón Definitivo Generado! ---")
    print(f"Total instituciones: {len(df)}")
    print(f"Archivo guardado en: {data_dir}")


if __name__ == "__main__":
    generate_manual_list()
