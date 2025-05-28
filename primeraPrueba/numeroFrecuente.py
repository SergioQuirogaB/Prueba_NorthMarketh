# Crea una función llamada numero_mas_frecuente(lista) que reciba una lista de números enteros y 
# devuelva el número que más veces se repite. Si hay más de uno con la misma frecuencia, devuelve el menor.

# Solución:

def numero_mas_frecuente(l):
    return sorted(
        ((x, l.count(x)) for x in {*l}),
        key=lambda p: (-p[1], p[0])
    )[0][0]

# Para este primer ejercicio incluí un bloque if __name__ == "__main__" simplemente para poder probar la función de forma directa desde la terminal.
# Esto me permite imprimir un ejemplo y verificar que el resultado sea el esperado, sin que se ejecute nada si en algún momento quisiera importar la función desde otro archivo.
# También traté de salirme un poco de lo común: en lugar de usar Counter o un diccionario, decidí trabajar con comprensión de listas y sorted() con doble criterio (primero por frecuencia descendente y luego por valor ascendente en caso de empate).

if __name__ == "__main__":
    muestra1 = [1, 3, 1, 3, 2, 1]
    print("Resultado esperado: 1")
    print("Resultado obtenido:", numero_mas_frecuente(muestra1))

    muestra2 = [4, 4, 5, 5]
    print("Resultado esperado: 4")
    print("Resultado obtenido:", numero_mas_frecuente(muestra2))
    
#Resultado

# # Resultado esperado: 1
# # Resultado obtenido: 1
# # Resultado esperado: 4
# # Resultado obtenido: 4

# Sergio Alejandro Quiroga