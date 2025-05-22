"""
Enunciado: Crea un script en Python que, haga lo siguiente: 
• Tome una palabra clave de búsqueda (puede ser una variable palabra = "laptop"). 
• Ingrese a la tienda virtual (Puede ser Mercado libre o Amazon) 
• Extraiga los títulos y precios de los primeros 5 productos que coincidan. 
• Permite cambiar la palabra clave fácilmente. 
Consideraciones: 
• Solo impresión en consola. 
• El script debe permitir cambiar fácilmente el término de búsqueda.
"""

# INSTRUCCIONES DE INSTALACIÓN Y EJECUCIÓN:
# 1. Ingresar a la carpeta Nivel Intermedio
#     cd Nivel Intermedio
    
# 2. Instalar las dependencias necesarias:
#    pip install -r requirements.txt

# 3. Ejecutar el script:
#    python buscar_productos.py

# 4. Ingresar la palabra clave cuando se solicite (ejmp: laptop, celular...)
# 5. Para salir del programa, escribir 'salir' cuando se pida la palabra clave

import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def buscar_productos(palabra_clave):
    palabra_codificada = urllib.parse.quote(palabra_clave)
    url = f"https://www.amazon.com.co/s?k={palabra_codificada}"
    
    # peticion HTTP
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-CO,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print(f"Buscando en: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        productos = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        print(f"\nResultados de búsqueda para: {palabra_clave}")
        print("-" * 50)
        
        if not productos:
            print("No se encontraron productos. Verificando la estructura de la página...")
            print("Primeros 500 caracteres del HTML recibido:")
            print(response.text[:500])
            return
        
        for i, producto in enumerate(productos[:5], 1):
            try:
                titulo_element = producto.find('h2')
                if titulo_element:
                    titulo = titulo_element.text.strip()
                else:
                    continue
                
                precio_element = producto.find('span', class_='a-price-whole')
                if precio_element:
                    precio = precio_element.text.strip()
                else:
                    precio = "Precio no disponible"
                
                print(f"\nProducto {i}:")
                print(f"Título: {titulo}")
                print(f"Precio: ${precio}")
                print("-" * 30)
                    
            except Exception as e:
                print(f"Error al procesar el producto {i}: {str(e)}")
                continue
                
    except requests.RequestException as e:
        print(f"Error al realizar la búsqueda: {e}")
        print("Detalles del error:", str(e))

def main():
    while True:
        palabra = input("\nIngrese la palabra clave para buscar (o 'salir' para terminar): ")
        if palabra.lower() == 'salir':
            break
        buscar_productos(palabra)
        #delay  
        time.sleep(1)

if __name__ == "__main__":
    main() 