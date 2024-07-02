import pandas as pd
import graphviz
from tokens import tokensLexer as tokens
from parser import cargar_reglas, obtener_primeros, obtener_siguientes

 
'''
 # Función para calcular conjuntos de primeros y siguientes
def calcular_conjuntos(archivo_reglas):
  reglas = cargar_reglas(archivo_reglas)
  primeros = obtener_primeros(reglas)
  simbolo_inicio = 'PROGRAMAINICIO'  # Definir el símbolo inicial de la gramática
  siguientes = obtener_siguientes(reglas, primeros, simbolo_inicio)
  return primeros, siguientes
'''

'''
# Llamada a la función para calcular conjuntos FIRST y FOLLOW
archivo_reglas = 'LL1.txt'
first_sets, follow_sets = calcular_conjuntos(archivo_reglas)

# Imprimir conjuntos de primeros
print("Conjuntos de primeros:")
for non_terminal, first in first_sets.items():
  print(f"{non_terminal}: {first}")

# Imprimir conjuntos de siguientes
print("\nConjuntos de siguientes:")
for non_terminal, follow in follow_sets.items():
  print(f"{non_terminal}: {follow}")
'''

tokens.append({'type': '$', 'lexeme': '$', 'line': 1})
#tokens.append({'type': '$', 'lexeme': '$', 'line': 0})
print("Tabla sintactica csv:")

syntax_table = pd.read_csv("Tabla.csv", index_col=0)
dot = graphviz.Digraph('hello')

counter = 0


#Crea objetos que representan a los nodos en pila.
class NodeStack:

  def __init__(self, symbol, terminal, val):
    global counter
    self.id = counter
    self.symbol = symbol
    self.terminal = terminal
    self.val = val
    counter += 1


#representar tokens en un programa o texto.
class Token:

  def __init__(self,
               node_st,
               lexeme=None,
               children=[],
               father=None,
               line=None):
    self.node_st = node_st
    self.lexeme = lexeme
    self.line = line
    self.children = children
    self.father = father
#Funcion para insertar los hijos.

  def insert_children(self, val):
    self.children.insert(0, val)


#Buscar nodo en árbol por su valor.Usa pila para recorrer el árbol en el ancho
#verifica si nodo actual coincide con valor buscado y si no tiene hijos
def find_arbol(node, val):
  stack = [node]
  while len(stack) != 0:
    if stack[0].node_st.symbol == val and len(stack[0].children) == 0:
      return stack[0]
    if stack[0].node_st.symbol != val and len(stack[0].children) == 0:
      stack.pop(0)
    if len(stack[0].children) > 0:
      temp = stack[0].children
      stack.pop(0)
      for i in list(reversed(temp)):
        stack.insert(0, i)
  return None



##Analizador Sintactico
stack = []
#Crear y manipular objetos NodeStack y Token llamando a NodeStack
node_E = NodeStack("PROGRAMAINICIO", False, 'A')
node_dolar = NodeStack("$", True, '')
stack = [node_E, node_dolar]
#Se crea el nodo raíz de un árbol de tokens.
root = Token(node_E, children=[])
dot.node(str(node_E.id), node_E.symbol)
while True:
  if tokens[0]["type"] != stack[0].symbol:
    print("COMPARACIÓN DE TOKENS")
    print(f"Token actual: {tokens[0]['type']}")
    print(f"Símbolo en stack: {stack[0].symbol}")
    print(f"Resultado: Diferentes")
    print("------------------------------")
  else:
    print("COMPARACIÓN DE TOKENS")
    print(f"Token actual: {tokens[0]['type']}")
    print(f"Símbolo en stack: {stack[0].symbol}")
    print(f"Resultado: Iguales, es terminal")
    print("------------------------------")

  print("estado actual del stack")
  for i in stack:
    print(f"  - {i.symbol}")
  print("-----------------------------------------------------------")

  if stack[0].symbol == '$' and tokens[0]["type"] == '$':
    print("La string es aceptada por la gramatica")
    break

  if stack[0].terminal:
    print("******************************")
    print(f"Terminal encontrado: {stack[0].symbol}")
    print(f"Eliminando con token: {tokens[0]['type']}")
    print("******************************")

    if stack[0].symbol == tokens[0]["type"]:
      stack.pop(0)
      tokens.pop(0)
    elif stack[0].symbol == 'ε':
      stack.pop(0)
    else:
      print("Error Sintactico")
      break


  else:
    production = syntax_table.loc[stack[0].symbol][tokens[0]["type"]]
    x = float('NaN')
    isNaN = pd.isna(x)
    if production == x:
      print("Error Sintactico2")
      break
    else:
      find = find_arbol(root, stack[0].symbol)
      stack.pop(0)
      production_str = str(production)
      elementos = production_str.split(" ")

      for i in list(reversed(elementos)):
        if i != '':
          #print("Hijo: ", i)
          bool = i.isupper()
          node = NodeStack(i, not bool, '')
          linea = 0
          lexema = ''
          if i == 'ε':
            lexema = 'ε'
          else:
            for j in tokens:
              if j['type'] == i:
                lexema = j['lexeme']
                linea = j['line']
                break
          tk = Token(node, father=find, children=[], lexeme=lexema, line=linea)
          find.insert_children(tk)
          stack.insert(0, node)




#Grafica el arbol
def get_graphviz_tree(node):
  dot = graphviz.Digraph()
  add_graphviz_node_recursive(node, dot)
  return dot.source


#Grafica el arbolx2
def add_graphviz_node_recursive(node, dot):
  if node.node_st.terminal:
    label = node.node_st.symbol + ": " + node.lexeme
    dot.node(str(node.node_st.id), label=label)
  else:
    dot.node(str(node.node_st.id), label="{}".format(node.node_st.symbol))
#Grafica el arbolx3
  for child in node.children:
    add_graphviz_node_recursive(child, dot)
    dot.edge(str(node.node_st.id), str(child.node_st.id))


# Uso de la función con el `root`
graphviz_code = get_graphviz_tree(root)
#Graphviz archivo

# genera

with open("Arbol.dot", "w") as f:
  f.write(graphviz_code)
#Funcion que obtiene las terminales, lexemas
#Funcion nos ayuda a obtener los nodos terminales (lexemas), y nos retorna.
def get_leaves(node):
  if not node.children:
    return [node.lexeme]
  leaves = []
  for child in node.children:
    leaves.extend(get_leaves(child))
  return leaves


#Devuelve en que scope fue creado una variable
def find_father_assig(root):
  if root.node_st.symbol == 'PROGRAMAINICIO' and root.father == None:
    return 'GLOBAL'
  if root.node_st.symbol == 'FUNCION':
    return root.children[1].children[0].children[0].lexeme
  if root.node_st.symbol == 'CONDICIONALIF':
    return 'CODIGO IF'
  if root.node_st.symbol == 'CODIGOELSE':
    return 'CODIGO ELSE'
  if root.node_st.symbol == 'CODIGOWHILE':
    return 'WHILE'
  if root.node_st.symbol == 'CODIGOMIENTRAS':
    return 'MIENTRAS'

  if root.father:
    return find_father_assig(root.father)


#Encuentra y elimina asignaciones
def find_and_delete_assg_si(root):
  global stackScope
  if root.node_st.symbol == 'ASIGNACION':
    stackScope = [
      item for item in stackScope
      if item['lexeme'] != root.children[1].children[0].lexeme
    ]
    print("Variable {} eliminada".format(
      root.children[1].children[0].lexeme))

  if root.children:
    for i in root.children:
      find_and_delete_assg_si(i)


#Verifica el tipo de dato
def tipo(cad):
  type = ''
  flag = False
  if cad.isdigit():
    type = 'int'
  elif cad.replace('.', '', 1).isdigit():
    type = 'float'
  elif cad[0] == '"':
    type = 'string'
  else:
    for i in stackScope:
      if i["lexeme"] == cad:
        flag = True
        type = i["tipo"]
        break
    if not flag:
      type = "ERROR"
  return type


def get_type(arr):

  type = tipo(arr[0])

  for i in range(0, len(arr), 2):
    elemento = tipo(arr[i])

    if type == 'int':
      if elemento != type:
        return "ERROR"

    if type == 'float':
      if elemento != 'float':
        if elemento != 'int':
          return "ERROR"

    if type == 'string':
      if elemento != type:
        return 'ERROR'
  return type


stackScope = []
flag = True


#Todo lo que es el scope.
def scope(root):
  global flag
  #(flag)
  global stackScope
  if root.node_st.symbol == 'IDENTIFICADOR':
    if root.father.node_st.symbol == 'PARAMETRO1':
      stackScope.append({
        'lexeme':
        root.children[0].lexeme,
        'valor':
        None,
        'tipo':
        'Parametro1',
        'padre':
        root.father.father.children[1].children[0].children[0].lexeme
      })
    elif root.father.node_st.symbol == 'PARAMETROSFUNCION':
      stackScope.append({
        'lexeme':
        root.children[0].lexeme,
        'valor':
        None,
        'tipo':
        'ParametroFunion',
        'padre':
        root.father.father.father.children[1].children[0].children[0].lexeme
      })
    elif root.father.node_st.symbol == 'NOMBREFUNCION':
      if root.children[0].lexeme not in [
          item['lexeme'] for item in stackScope
      ]:
        print("La Variable {} creada en ámbito global".format(
          root.children[0].lexeme))
        stackScope.append({
          'lexeme': root.children[0].lexeme,
          'valor': None,
          'tipo': 'Funcion',
          'padre': 'GLOBAL'
        })
      else:
        print("La Variable {} ya tiene una asignacion".format(
          root.children[0].lexeme))
        flag = False

      print(stackScope)
    elif root.father.node_st.symbol == 'ASIGNACION':
      if root.children[0].lexeme in [item['lexeme'] for item in stackScope]:
        print("La Variable {} ya tiene una asignacion".format(
          root.children[0].lexeme))
        flag = False
        return
      father = find_father_assig(root)
      print("La Variable {} creada en scope {}".format(root.children[0].lexeme,
                                                      father))
      linea = root.children[0].line
      valor = get_leaves(root.father)
      tipo_arr = get_type(valor[3:-1])
      type = 'ERROR'

      if tipo_arr != valor[0]:
        print("ERROR DE ASIGNACION DE DATO ,ASIGNACION INCOMPATIBLE")
        flag = False
      else:
        type = tipo_arr

      stackScope.append({
        'lexeme': root.children[0].lexeme,
        'valor': valor[3:-1],
        'tipo': type,
        'padre': father,
        'line': linea
      })
    elif root.father.node_st.symbol == 'PARA':
      stackScope.append({
        'lexeme': root.children[0].lexeme,
        'valor': '',
        'tipo': 'variable',
        'padre': 'para'
      })
    elif root.father.node_st.symbol == 'ELEMENTO2':
      lexeme = root.children[0].lexeme
      if lexeme in [item['lexeme'] for item in stackScope]:
        print("La variable {} fue utilizada".format(lexeme))
      else:
        print("La variable {} no fue declarada en este scope".format(lexeme))
        flag = False
    elif root.father.father.node_st.symbol == 'CODIGOFUNCION':
      lexeme = root.children[0].lexeme
      if lexeme in [item['lexeme'] for item in stackScope]:
        print("La variable {} fue utilizada".format(lexeme))
      else:
        print("La variable {} no fue declarada en este scope".format(lexeme))
        flag = False

  #Eliminacion de scope
  if root.lexeme == '}':
    if root.father.father.node_st.symbol == 'FUNCION':
      stackScope = [
        item for item in stackScope if item['padre'] !=
        root.father.father.children[1].children[0].children[0].lexeme
      ]
    elif root.father.node_st.symbol in ['CODIGOELSE', 'CODIGOMIENTRAS']:
      find_and_delete_assg_si(root.father)
    elif root.father.node_st.symbol == 'CODIGOWHILE':
      stackScope = [
        item for item in stackScope
        if item['lexeme'] != root.father.father.children[1].children[0].lexeme
      ]
      find_and_delete_assg_si(root.father)
    elif root.father.node_st.symbol == 'CODIGOIF':
      find_and_delete_assg_si(root.father.children[1])

  if flag:
    for i in root.children:
      scope(i)
  else:
    return


#(stackScope)
scope(root)

if flag:
  for i in stackScope:
    print(i)
else:
  print("Error semantico")




# Definición de variables globales para el ensamblador en .asm
cabecera = ".data\n"
cuerpo = ".text\nmain:\n"

# Función para definir una variable en el ensamblador .asm
def definir_variable(variable):
    global cabecera
    cabecera += "  var_" + variable + ": .word    0:1\n"

# Función para escribir el ensamblador en .asm
def escribir_assembler(cabecera, cuerpo):
    with open("output.asm", "w") as f:
        f.write(cabecera + "\n")
        f.write(cuerpo + "\n")
    print("Código assembler generado en output.asm")

# Función para generar una asignación en el ensamblador .asm
def generar_asignacion(variable, valor):
    global cuerpo
    if isinstance(valor, int):
        cuerpo += "    li $t0, {}\n".format(valor)
    elif isinstance(valor, str):
        cuerpo += '    la $t0, var_{}\n'.format(valor)
        cuerpo += '    lw $t0, 0($t0)\n'
    cuerpo += '    sw $t0, var_{}\n'.format(variable)

# Función recursiva para recorrer el árbol y generar código en .asm
def recorrer_arbol(node):
    global cuerpo
    if node.node_st.symbol == "ASIGNACION":
        # Asignaciones
        variable = node.children[0].children[0].lexeme
        definir_variable(variable)
        # Asignar valor a variable
        valor = node.children[1].children[0].lexeme
        generar_asignacion(variable, valor)
    elif node.node_st.symbol == "CONDICIONAL":
        # Condicionales if-else
        cond_expr = node.children[0]
        if_expr = node.children[1]
        else_expr = node.children[2]
        # Obtener los valores y variables involucradas en la condición
        a_lexeme = cond_expr.children[0].lexeme
        b_lexeme = cond_expr.children[2].lexeme
        if_operator = cond_expr.children[1].lexeme
        # Generar código para evaluar la condición
        cuerpo += '# Comparación (a {} b)\n'.format(if_operator)
        cuerpo += 'la $t0, var_{}\n'.format(a_lexeme)
        cuerpo += 'lw $t1, 0($t0)\n'
        cuerpo += 'la $t2, var_{}\n'.format(b_lexeme)
        cuerpo += 'lw $t3, 0($t2)\n'
        # Realizar la comparación y saltar a la etiqueta correspondiente
        if if_operator == ">":
            cuerpo += 'sub $t4, $t1, $t3\n'
            cuerpo += 'bgtz $t4, if_true\n'
        elif if_operator == "<":
            cuerpo += 'sub $t4, $t1, $t3\n'
            cuerpo += 'bltz $t4, if_true\n'
        # Generar código para el bloque "if"
        cuerpo += '# Código del bloque "if"\n'
        # Recorrer el árbol del bloque "if"
        recorrer_arbol(if_expr)
        # Saltar a la etiqueta de fin del condicional
        cuerpo += 'j if_end\n'
        # Generar código para el bloque "else"
        cuerpo += 'if_true:\n'
        cuerpo += '# Código del bloque "else"\n'
        # Recorrer el árbol del bloque "else"
        recorrer_arbol(else_expr)
        # Etiqueta de fin del condicional
        cuerpo += 'if_end:\n'
    else:
        # Recorrer los nodos hijos del nodo actual
        for child in node.children:
            recorrer_arbol(child)


# Definición de variables globales para el ensamblador en .txt
cabecera_txt = ".data\n"
cuerpo_txt = ".text\nmain:\n"

# Función para definir una variable en el ensamblador .txt
def definir_variable_txt(variable):
    global cabecera_txt
    cabecera_txt += "  var_" + variable + ": .word 0\n"

# Función para escribir el ensamblador en .txt
def escribir_assembler_txt():
    with open("ensamblador.txt", "w") as f:
        f.write(cabecera_txt + "\n")
        f.write(cuerpo_txt + "\n")
    print("Código assembler generado en ensamblador.txt")

# Función para generar una asignación en el ensamblador .txt
def generar_asignacion_txt(variable, valor):
    global cuerpo_txt
    if isinstance(valor, int):
        cuerpo_txt += f"  li $t0, {valor}\n"
    elif isinstance(valor, str):
        cuerpo_txt += f"  la $t0, var_{valor}\n"
        cuerpo_txt += f"  lw $t0, 0($t0)\n"
    cuerpo_txt += f"  sw $t0, var_{variable}\n"

# Función recursiva para recorrer el árbol y generar código en .txt
def recorrer_arbol_txt(node):
    global cuerpo_txt
    if node.node_st.symbol == "ASIGNACION":
        # Asignaciones
        variable = node.children[0].children[0].lexeme
        definir_variable_txt(variable)
        # Asignar valor a variable
        valor = node.children[1].children[0].lexeme
        generar_asignacion_txt(variable, valor)
    elif node.node_st.symbol == "CONDICIONAL":
        # Condicionales if-else
        cond_expr = node.children[0]
        if_expr = node.children[1]
        else_expr = node.children[2]
        # Obtener los valores y variables involucradas en la condición
        a_lexeme = cond_expr.children[0].lexeme
        b_lexeme = cond_expr.children[2].lexeme
        if_operator = cond_expr.children[1].lexeme
        # Generar código para evaluar la condición
        cuerpo_txt += f"# Comparación (a {if_operator} b)\n"
        cuerpo_txt += f"  la $t0, var_{a_lexeme}\n"
        cuerpo_txt += f"  lw $t1, 0($t0)\n"
        cuerpo_txt += f"  la $t2, var_{b_lexeme}\n"
        cuerpo_txt += f"  lw $t3, 0($t2)\n"
        # Realizar la comparación y saltar a la etiqueta correspondiente
        if if_operator == ">":
            cuerpo_txt += "  sub $t4, $t1, $t3\n"
            cuerpo_txt += "  bgtz $t4, if_true\n"
        elif if_operator == "<":
            cuerpo_txt += "  sub $t4, $t1, $t3\n"
            cuerpo_txt += "  bltz $t4, if_true\n"
        # Generar código para el bloque "if"
        cuerpo_txt += "# Código del bloque 'if'\n"
        # Recorrer el árbol del bloque "if"
        recorrer_arbol_txt(if_expr)
        # Saltar a la etiqueta de fin del condicional
        cuerpo_txt += "  j if_end\n"
        # Generar código para el bloque "else"
        cuerpo_txt += "if_true:\n"
        cuerpo_txt += "# Código del bloque 'else'\n"
        # Recorrer el árbol del bloque "else"
        recorrer_arbol_txt(else_expr)
        # Etiqueta de fin del condicional
        cuerpo_txt += "if_end:\n"
    else:
        # Recorrer los nodos hijos del nodo actual
        for child in node.children:
            recorrer_arbol_txt(child)



# Ejemplo de uso:
# Suponiendo que `root` es el nodo raíz del árbol sintáctico generado
recorrer_arbol(root)
escribir_assembler(cabecera, cuerpo)
recorrer_arbol_txt(root)
escribir_assembler_txt()
