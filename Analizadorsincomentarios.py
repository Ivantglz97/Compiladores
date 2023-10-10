#Autor:Trejo Gonzalez Ivan //Compiladores
import sys


print()
print("Analizador Lexico")
print()

# Verificamos si se proporcionó un argumento en la línea de comandos
if len(sys.argv) != 2:
    sys.exit(1)

archivo_entrada = sys.argv[1]

# Abrir el archivo 
with open(archivo_entrada, 'r') as file:


#Diccionarios
    identificadores = {}
    identificadores_key = identificadores.keys()

    palabras_reservadas = {'and' : 'AND', 'else' : 'ELSE', 'false' : 'FALSE', 'for' : 'FOR',
                        'fun' : 'FUN', 'if' : 'IF', 'null' : 'NULL',
                        'or' : 'OR', 'print' : 'PRINT', 'return' : 'RETURN',
                        'true' : 'TRUE', 'var' : 'VAR', 'while': 'WHILE'}
    palabras_reservadas_key = palabras_reservadas.keys()

    cadenas = {}
    cadenas_key = cadenas.keys()

    simbolos1C = {
                '+' : 'PLUS', '-' : 'MINUS','*' : 'STAR', '/' : 'SLASH', '{' : 'LEFT_BRACE', '}' : 'RIGHT_BRACE',
                '(' : 'LEFT_PAREN', ')' : 'RIGHT_PARENT', ',' : 'COMMA', '.' : 'DOT', ';' : 'SEMICOLON' }
    simbolos1C_key = simbolos1C.keys()

    simbolos2C = {'!' : 'BANG','!=' : 'BANG_EQUAL', '=' : 'EQUAL','==' : 'EQUAL_EQUAL','>' : 'GREATER','>=' : 'GREATER_EQUAL',
                '<' : 'LESS ','<=' : 'LESS_EQUAL'}
    simbolos2C_key = simbolos2C.keys()

    #Leemos el archivo
    a = file.read()
    count = 0


    #Dividimos el archivo.
    program = a.split("\n")
    for line in program:
        count = count + 1
        #print("Linea #",count ,'\n',line)

        if not line.strip():
            continue  #Ignoramos lineas vacias
    # Verificamos si la línea comienza con '//'
        if line.strip().startswith('//'):
            continue  # Ignoramos la línea y pasamos a la siguiente
        if line.strip().startswith('/*'):
            continue  #Ignoramos el inicio de comentario
        if line.strip().endswith('*/'):
            continue  #Ignoramos el fin de comentario


        def tokenize(line):
            tokens = []                # Lista para almacenar los tokens
            current_token = ""         # Variable para construir el token actual
            state = "inicio"           # Estado inicial

            for char in line:
                if state == "inicio":
                    # Si el carácter es una comilla doble, cambiamos al estado "entre_comillas".
                    if char == '"':
                        current_token += char
                        state = "entre_comillas"
                    # Si el carácter es una letra, un guion bajo o un dígito, cambiamos al estado "palabra".
                    elif char.isalpha() or char == '_':
                        current_token += char
                        state = "palabra"
                    # Si el carácter es uno de los operadores <, >, = o !, cambiamos al estado "operador".
                    elif char in "<>=!":
                        current_token += char
                        state = "operador"
                    # Si el carácter es un dígito o un signo negativo, cambiamos al estado "numero".
                    elif char.isdigit() or char == '-':
                        current_token += char
                        state = "numero"
                    else:
                        # Si el carácter no coincide con ninguno de los casos anteriores, lo agregamos directamente a la lista de tokens.
                        tokens.append(char)
                elif state == "entre_comillas":
                    # Si estamos en el estado "entre_comillas" y encontramos otra comilla doble, cerramos el token y volvemos al estado "inicio".
                    if char == '"':
                        current_token += char
                        tokens.append(current_token)
                        current_token = ""
                        state = "inicio"
                    else:
                        # Si no es una comilla doble, simplemente agregamos el carácter al token actual.
                        current_token += char
                elif state == "palabra":
                    # Si estamos en el estado "palabra" y encontramos un carácter válido para una palabra, lo agregamos al token actual.
                    if char.isalnum() or char == '_':
                        current_token += char
                    else:
                        # Si encontramos un carácter que no es válido para una palabra, cerramos el token y volvemos al estado "inicio".
                        tokens.append(current_token)
                        current_token = ""
                        state = "inicio"
                        if char == '"':
                            current_token += char
                            state = "entre_comillas"
                        elif char in "<>=!":
                            current_token += char
                            state = "operador"
                        else:
                            tokens.append(char)
                elif state == "operador":
                    # Si estamos en el estado "operador" y encontramos un carácter válido para un operador (= o !), lo agregamos al token actual.
                    if char in "=!":
                        current_token += char
                    else:
                        # Si encontramos un carácter que no es válido para un operador, cerramos el token y volvemos al estado "inicio".
                        tokens.append(current_token)
                        current_token = ""
                        state = "inicio"
                        if char in "<>=":
                            current_token += char
                        else:
                            tokens.append(char)
                elif state == "numero":
                    # Si estamos en el estado "numero" y encontramos un dígito o un punto decimal, lo agregamos al token actual.
                    if char.isdigit() or char == '.':
                        current_token += char
                    else:
                        # Si encontramos un carácter que no es válido para un número, cerramos el token y volvemos al estado "inicio".
                        tokens.append(current_token)
                        current_token = ""
                        state = "inicio"
                        if char == '"':
                            current_token += char
                            state = "entre_comillas"
                        elif char.isalpha() or char == '_':
                            current_token += char
                            state = "palabra"
                        elif char in "<>=!":
                            current_token += char
                            state = "operador"
                        else:
                            tokens.append(char)

            # Agregamos el token actual a la lista de tokens si todavía está abierto.
            if current_token:
                tokens.append(current_token)

            return tokens
        tokens = tokenize(line)
        for token in tokens:
            # Tokens de un caracter
            if token in simbolos1C_key:
                continue
            # Tokens de uno o dos caracteres
            elif token in simbolos2C_key:
                continue
            # Cadena encerrada en comillas
            elif token.startswith('"') and token.endswith('"'):
                cadena_sin_comillas = token[1:-1]  # Elimina las comillas del principio y el final
                cadenas[token] = cadena_sin_comillas
                continue
            # Palabras Clave
            elif token in palabras_reservadas_key:
                continue
            # Identificadores
            elif token.isidentifier():
                continue
            # Números 
            elif token.replace(".", "", 1).isdigit():
                continue
            # Identifica los espacios
            elif token.startswith(' '):
                continue
            # Maneja los tokens desconocidos (Agrega esta condición)
            else:
                 print("Error el Linea", count , "Caracter no Valido")
                 sys.exit(1) #Error por caracter no valido y se detiene el systema

       # print("................................................")
            