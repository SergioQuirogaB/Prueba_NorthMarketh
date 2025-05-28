import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import sys

# --- Configuración y Constantes ---
# Las cuentas de Instagram a simular. Puedes añadir o quitar aquí.
INSTAGRAM_ACCOUNTS = ['elcorteingles', 'mercadona', 'carrefoures']
# Número total de seguidores a simular. Ajusta según la prueba.
NUM_TOTAL_FOLLOWERS = 1500 # Aumentado para dar más "volumen" de datos
# Rango de fechas para simular la creación de perfiles (años).
PROFILE_CREATION_YEAR_RANGE = (2010, datetime.now().year)
# Probabilidad de que un seguidor tenga un número de teléfono publicado
PROB_PHONE_PUBLISHED = 0.35 # Ligeramente ajustado
# Probabilidad de que un seguidor tenga un correo electrónico publicado
PROB_EMAIL_PUBLISHED = 0.45 # Ligeramente ajustado
# Probabilidad de que tenga un segundo número/correo
PROB_SECOND_CONTACT_INFO = 0.1

# --- Funciones Principales ---
def generate_simulated_follower_data(num_followers: int, accounts: list) -> pd.DataFrame:
    """
    Genera datos simulados de seguidores para cuentas de Instagram.
    Este enfoque es utilizado para respetar las políticas de privacidad y los
    términos de servicio de Instagram, ya que la extracción directa de esta
    información es inviable y éticamente incorrecta.

    Args:
        num_followers (int): Número total de seguidores a simular.
        accounts (list): Lista de nombres de cuentas de Instagram a simular.

    Returns:
        pd.DataFrame: DataFrame de pandas con los datos simulados de seguidores.
    """
    fake = Faker('es_ES')  # Generar datos en español para mayor credibilidad
    data = []

    # Distribución equitativa de seguidores por cuenta
    followers_per_account = num_followers // len(accounts)
    remaining_followers = num_followers % len(accounts)

    print(f"Generando {num_followers} seguidores simulados para {len(accounts)} cuentas...")

    for i, account_name in enumerate(accounts):
        current_account_followers = followers_per_account
        if i < remaining_followers:
            current_account_followers += 1

        for _ in range(current_account_followers):
            full_name = fake.name()
            
            # Simulación de número(s) de teléfono
            phone_numbers = []
            if random.random() < PROB_PHONE_PUBLISHED:
                phone_numbers.append(fake.phone_number())
            if random.random() < PROB_SECOND_CONTACT_INFO and phone_numbers: # Solo si ya tiene uno
                phone_numbers.append(fake.phone_number())
            
            # Simulación de dirección(es) de correo electrónico
            emails = []
            if random.random() < PROB_EMAIL_PUBLISHED:
                emails.append(fake.email())
            if random.random() < PROB_SECOND_CONTACT_INFO and emails: # Solo si ya tiene uno
                emails.append(fake.email())

            # Simular fecha de creación del perfil (entre rango definido)
            start_date_year = PROFILE_CREATION_YEAR_RANGE[0]
            end_date_year = PROFILE_CREATION_YEAR_RANGE[1]
            random_year = random.randint(start_date_year, end_date_year)
            # Para asegurar una fecha válida dentro del año elegido
            random_month = random.randint(1, 12)
            random_day = random.randint(1, 28) # Evitar problemas con días de meses
            profile_creation_date = datetime(random_year, random_month, random_day)
            
            data.append({
                'Cuenta de Origen': f'@{account_name}',
                'Nombre Completo': full_name,
                'Numero(s) de Telefono': ', '.join(phone_numbers) if phone_numbers else 'N/A',
                'Direccion(es) de Correo Electronico': ', '.join(emails) if emails else 'N/A',
                'Fecha de Creacion del Perfil': profile_creation_date.strftime('%Y-%m-%d')
            })

    # Mezclar los datos para una distribución más aleatoria en el Excel
    random.shuffle(data)
    
    return pd.DataFrame(data)

def save_to_excel(dataframe: pd.DataFrame, filename: str = "datos_seguidores_simulados.xlsx", output_dir: str = "output"):
    """
    Guarda un DataFrame de pandas en un archivo Excel.

    Args:
        dataframe (pd.DataFrame): DataFrame a guardar.
        filename (str): Nombre del archivo Excel.
        output_dir (str): Directorio donde se guardará el archivo.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)  # Crear el directorio si no existe
        filepath = os.path.join(output_dir, filename)
        dataframe.to_excel(filepath, index=False, engine='openpyxl')
        print(f"\nÉxito: Datos guardados exitosamente en '{filepath}'")
    except Exception as e:
        print(f"\nError al guardar el archivo Excel: {e}", file=sys.stderr)
        sys.exit(1) # Salir con un código de error

# --- Ejecución Principal ---
if __name__ == "__main__":
    print("-----------------------------------------------------")
    print(" Iniciando la generación de datos simulados para la  ")
    print("       prueba técnica de extracción de Instagram     ")
    print("-----------------------------------------------------")
    
    try:
        simulated_data = generate_simulated_follower_data(NUM_TOTAL_FOLLOWERS, INSTAGRAM_ACCOUNTS)
        
        print(f"\nGenerados {len(simulated_data)} registros de seguidores simulados.")
        
        save_to_excel(simulated_data)
        
        print("\nProceso completado. Revisa la carpeta 'output' para el archivo Excel.")
        print("-----------------------------------------------------")
        print(" Recuerda revisar el README.md para la justificación ")
        print("      de la solución y las consideraciones éticas.   ")
        print("-----------------------------------------------------")

    except Exception as e:
        print(f"\n¡Error inesperado durante la ejecución principal: {e}", file=sys.stderr)
        sys.exit(1) # Salir con un código de error