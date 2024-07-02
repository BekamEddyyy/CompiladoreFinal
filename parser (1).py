import re

EPSILON = 'ε'

# Cargar reglas gramaticales desde un archivo
def cargar_reglas(archivo):
    with open(archivo, 'r') as file:
        reglas = [linea.strip() for linea in file if linea.strip()]
    return reglas

# Clasificar símbolos en terminales y no terminales
def clasificar_simbolos(reglas):
    no_terminales = set()
    terminales = set()
    for regla in reglas:
        izq, der = regla.split('->')
        izq = izq.strip()
        no_terminales.add(izq)
        for simbolo in der.split():
            if not simbolo.islower() and simbolo not in ['(', ')', '|', EPSILON]:
                no_terminales.add(simbolo)
            else:
                terminales.add(simbolo)
    return no_terminales, terminales

# Calcular conjuntos FIRST
def obtener_primeros(reglas):
    primeros = {}
    cambio = True

    no_terminales, terminales = clasificar_simbolos(reglas)
    for simbolo in no_terminales.union(terminales):
        primeros[simbolo] = set()
        if simbolo in terminales:
            primeros[simbolo].add(simbolo)

    while cambio:
        cambio = False
        for regla in reglas:
            izq, der = regla.split('->')
            izq = izq.strip()
            der = der.strip().split()

            first_original = primeros[izq].copy()
            puede_ser_vacio = True

            for simbolo in der:
                if not puede_ser_vacio:
                    break

                primeros[izq].update(primeros[simbolo] - {EPSILON})

                if EPSILON not in primeros[simbolo]:
                    puede_ser_vacio = False

            if puede_ser_vacio:
                primeros[izq].add(EPSILON)

            if primeros[izq] != first_original:
                cambio = True

    return primeros

# Calcular conjuntos FOLLOW
def obtener_siguientes(reglas, primeros, simbolo_inicio):
    siguientes = {no_terminal: set() for no_terminal in primeros}
    siguientes[simbolo_inicio].add('$')

    cambio = True
    while cambio:
        cambio = False
        for regla in reglas:
            partes = regla.split('->')
            if len(partes) < 2:
                continue
            izquierda = partes[0].strip()
            derecha = partes[1].strip().split()

            trailer = set(siguientes[izquierda])
            for i in reversed(range(len(derecha))):
                simbolo = derecha[i]
                if simbolo in siguientes:
                    antes_de_actualizar = len(siguientes[simbolo])
                    siguientes[simbolo].update(trailer)
                    if len(siguientes[simbolo]) > antes_de_actualizar:
                        cambio = True
                    if EPSILON in primeros.get(simbolo, set()):
                        trailer.update(x for x in primeros[simbolo] if x != EPSILON)
                    else:
                        trailer = set(primeros.get(simbolo, set()))
                else:
                    if simbolo != EPSILON:
                        trailer = {simbolo}

    return {k: v for k, v in siguientes.items() if v}

# Función principal para cargar las reglas y calcular conjuntos FIRST y FOLLOW
def main():
    archivo_reglas = 'LL1.txt'
    reglas = cargar_reglas(archivo_reglas)
    primeros = obtener_primeros(reglas)
    simbolo_inicio = 'PROGRAMAINICIO'  # Definir el símbolo inicial de la gramática
    siguientes = obtener_siguientes(reglas, primeros, simbolo_inicio)

    print("Conjuntos FIRST:")
    for k, v in primeros.items():
        print(f"{k}: {v}")

    print("\nConjuntos FOLLOW:")
    for k, v in siguientes.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
