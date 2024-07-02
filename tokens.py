import ply.lex as lex

reserved = {
  'If': 'If',
  'in': 'in',
  'rango': 'rango',
  'Else': 'Else',
  'While': 'While',
  'For': 'For',
  'int': 'int',
  'float': 'float',
  'string': 'string',
  'And': 'And',
  'Or': 'Or',
  'imprimir': 'imprimir',
  'TipoFuncion': 'TipoFuncion',
  'return': 'return',
  'numeroflotante': 'numeroflotante',
  'numeroentero': 'numeroentero',
  'True': 'True',
  'False': 'False',
  'class': 'class',
  'break': 'break',
  'not': 'not',
}

# List of token names.   This is always required
tokens = [
  'identificador', 'Suma', 'Resta', 'Mult', 'Div', 'Asignacion', 'iguaQue',
  'mayor_que', 'maIgual_que', 'meIgual_que', 'menor_que', 'comentarios', 'texto',
  'parentesisIZQ', 'parentesisDER', 'llaveIZQ', 'llaveDER', 'dot', 'comma', 'pcoma'
  #'operincremento'  #, 'comillas'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_Suma = r'\+'
t_Resta = r'\-'
t_Mult = r'\*'
t_Div = r'/'
t_Asignacion = r'\='
t_iguaQue = r'\=='
t_mayor_que = r'\>='
t_menor_que = r'\<='
t_maIgual_que = r'\>'
t_meIgual_que = r'\<'
t_parentesisDER = r'\)'
t_parentesisIZQ = r'\('
t_llaveIZQ = r'\{'
t_llaveDER = r'\}'
t_dot = r'\.'
t_comma = r'\,'
t_pcoma = r'\;' #punto y coma no te confundas bkm

def t_flotante_numero(t):
  r'[0-9]*\.[0-9]+'
  t.type = reserved.get(t.value,
                        'numeroflotante')  # guardamos el valor del lexema
  #print("se reconocio el numero"), por que lo comentaste. Nose . XD
  return t


def t_entero_numero(t):
  r'[0-9]+'
  t.type = reserved.get(t.value,
                        'numeroentero')  # guardamos el valor del lexema
  #print("se reconocio el numero")
  return t


def t_t_identificador(t):
  r'[a-zA-Z]+([a-zA-Z0-9]*)'
  t.type = reserved.get(t.value, 'identificador')  # Check for reserved words
  return t


def t_texto(t):
  r'"[a-zA-Z0-9 !@#$%^&()-+=/\|_.,;:<>?{}\[\]`~ ]+"'
  t.type = reserved.get(t.value, 'texto')  # guardamos el valor del lexema
  #print("se reconocio el numero")
  return t


def t_comentarios(t):
  r'//[a-zA-Z0-9 !@#$%^&()-+=/\|_.,;:<>?{}\[\]`~ ]+'
  t.type = reserved.get(t.value,
                        'comentarios')  # guardamos el valor del lexema
  #print("se reconocio el numero")
  return t


# Define a rule so we can track line numbers
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule


def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Test it out
f = open('input.txt', 'r')
data = f.read()
# Give the lexer some input
lexer.input(data)
tokensLexer = []

# Traenis la informacion de un txt
while True:
  tok = lexer.token()
  if not tok:
    break  # No more input

  tokensLexer.append({
    'type': tok.type,
    'lexeme': tok.value,
    'line': tok.lineno,
    'used': False,
  })
  #print(tok.type, tok.value, tok.lineno, tok.lexpos)
f.close()
