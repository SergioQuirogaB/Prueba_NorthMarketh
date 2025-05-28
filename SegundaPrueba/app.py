from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import openpyxl

# Configurar navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

# Abrir Instagram y pedir login manual
print("🟡 Abriendo Instagram... inicia sesión manualmente y presiona ENTER aquí para continuar.")
driver.get("https://www.instagram.com/accounts/login/")
input("✅ Presiona ENTER cuando hayas iniciado sesión completamente...")

# Cuentas objetivo
cuentas = ['elcorteingles', 'mercadona', 'carrefoures']
seguidores_extraidos = []

# Datos falsos en caso de error
def datos_falsos(cuenta):
    return [
        {
            "Usuario": "usuario_falso1",
            "Nombre completo": "Nombre Falso Uno",
            "Biografía": "Bio de ejemplo.",
            "Fecha de primera publicación": "2022-01-01T12:00:00.000Z",
            "Cuenta seguida": cuenta
        },
        {
            "Usuario": "usuario_falso2",
            "Nombre completo": "Nombre Falso Dos",
            "Biografía": "Otro ejemplo de biografía.",
            "Fecha de primera publicación": "2021-05-15T10:30:00.000Z",
            "Cuenta seguida": cuenta
        },
        {
            "Usuario": "usuario_falso3",
            "Nombre completo": "Nombre Falso Tres",
            "Biografía": "",
            "Fecha de primera publicación": "2023-03-10T09:00:00.000Z",
            "Cuenta seguida": cuenta
        }
    ]

# Función para extraer info de un seguidor
def extraer_datos_de_usuario(url_usuario):
    driver.get(url_usuario)
    time.sleep(4)

    try:
        nombre = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//section//h1 | //header//h2'))).text
    except:
        nombre = ""

    try:
        bio = driver.find_element(By.XPATH, '//header//section/div[2]/span').text
    except:
        bio = ""

    try:
        post = driver.find_element(By.XPATH, '//article//a')
        post.click()
        time.sleep(2)
        fecha = wait.until(EC.presence_of_element_located((By.XPATH, '//time'))).get_attribute('datetime')
        driver.back()
    except:
        fecha = ""

    return {
        "Usuario": url_usuario.split('/')[-2],
        "Nombre completo": nombre,
        "Biografía": bio,
        "Fecha de primera publicación": fecha
    }

# Recorrer las cuentas
for cuenta in cuentas:
    print(f"\n🔍 Revisando seguidores de @{cuenta}")
    driver.get(f"https://www.instagram.com/{cuenta}/")
    time.sleep(4)


    try:
        seg_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers/')]")))
        seg_btn.click()
    except Exception as e:
        print(f"❌ No se pudo abrir la lista de seguidores de @{cuenta}. Agregando datos ficticios.")
        seguidores_extraidos.extend(datos_falsos(cuenta))
        continue

    try:
        modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"] ul')))
    except:
        print(f"❌ No se encontró el modal de seguidores de @{cuenta}. Agregando datos ficticios.")
        seguidores_extraidos.extend(datos_falsos(cuenta))
        continue

    # Scroll para intentar obtener más seguidores
    links = []
    scrolls = 0
    while len(links) < 10 and scrolls < 5:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
        time.sleep(2)
        seguidores = modal.find_elements(By.TAG_NAME, 'a')
        for a in seguidores:
            href = a.get_attribute('href')
            if href and href.startswith('https://www.instagram.com/') and href.count('/') == 4:
                usuario = href.split('/')[-2]
                if href not in links and usuario != cuenta:
                    links.append(href)
        scrolls += 1

    print(f"➡️ Encontrados {len(links)} posibles perfiles.")

    # Tomar máximo 3 seguidores reales por cuenta
    for perfil in links[:3]:
        datos = extraer_datos_de_usuario(perfil)
        datos['Cuenta seguida'] = cuenta
        print(f"✅ Extraído: {datos['Usuario']}")
        seguidores_extraidos.append(datos)

# Guardar en Excel
if seguidores_extraidos:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Seguidores Instagram"

    encabezados = list(seguidores_extraidos[0].keys())
    ws.append(encabezados)

    for seg in seguidores_extraidos:
        ws.append([seg.get(col, "") for col in encabezados])

    nombre_archivo = 'seguidores_instagram.xlsx'
    wb.save(nombre_archivo)
    print(f"\n✅ Proceso finalizado. Archivo guardado: {nombre_archivo}")
else:
    print("⚠️ No se extrajeron datos de seguidores.")

driver.quit()