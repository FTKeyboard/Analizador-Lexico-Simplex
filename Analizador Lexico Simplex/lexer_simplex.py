import ply.lex as lex
import os
import tkinter as tk
from tkinter import filedialog

# Definición de las palabras clave (reservadas)
keywords = {
    'if', 'else', 'while', 'for', 'return', 'int', 'float', 'string', 'true', 'false'
}

# Definición de los tokens
tokens = [
    'KEYWORD', 'IDENTIFIER', 'INVALID_IDENTIFIER', 'OPERATOR', 'ASSIGNMENT_OPERATOR',
    'DELIMITER', 'NUMBER', 'STRING', 'COMMENT', 'UNRECOGNIZED_SYMBOL', 'ERROR'
]

# Expresiones regulares para los tokens
t_KEYWORD = r'\b(if|else|while|for|return|int|float|string|true|false)\b'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_INVALID_IDENTIFIER = r'(\d|[@$])[a-zA-Z_][a-zA-Z_0-9]*'
t_OPERATOR = r'\+|\-|\*|\/|\=\=|\>|\<|\='  # Añadido el símbolo de asignación '='
t_ASSIGNMENT_OPERATOR = r'\=\='  # Cambiado para ser exclusivo de comparación
t_DELIMITER = r'\;|\{|\}|\(|\)'
t_NUMBER = r'\d+\.\d+|\d+'
t_STRING = r'\"[^\"]*\"'
t_COMMENT = r'//.*'
t_UNRECOGNIZED_SYMBOL = r'[\$\#]'

# Ignorar espacios, tabulaciones y saltos de línea
t_ignore = ' \t\n'

# Regla para manejar errores léxicos
def t_error(t):
    r'.'
    print(f"Error: Carácter no reconocido '{t.value[0]}' en la línea {t.lineno}, columna {find_column(t, t.lexer.lexdata)}")
    t.lexer.skip(1)  # Salta el carácter no reconocido

# Función para encontrar la columna del token
def find_column(token, lexdata):
    line_start = lexdata.rfind('\n', 0, token.lexpos) + 1
    return token.lexpos - line_start + 1

# Crear el lexer
lexer = lex.lex()

# Función para analizar el archivo de entrada
def analizar_archivo(archivo):
    with open(archivo, 'r') as f:
        data = f.read()
        lexer.input(data)
        tokens_generados = []

        # Depuración: Imprimir el texto que se va a analizar
        print("Texto a analizar:")
        print(data)
        print("-" * 40)

        while True:
            token = lexer.token()
            if not token:
                break
            tokens_generados.append(token)

        # Depuración: Imprimir los tokens generados
        print("Tokens generados:")
        for token in tokens_generados:
            print(f'{token.type}: {token.value} en línea {token.lineno}, columna {find_column(token, data)}')
        print("-" * 40)

        return tokens_generados

# Función para guardar los tokens en un archivo de salida
def guardar_tokens(tokens, archivo_salida):
    with open(archivo_salida, 'w') as f:
        for token in tokens:
            f.write(f'{token.type}: {token.value} en linea {token.lineno}, columna {find_column(token, f.name)}\n')

# Función para seleccionar archivo de entrada con el explorador de archivos
def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    archivo = filedialog.askopenfilename(title="Elige el archivo de entrada que deseas analizar con Simplex", filetypes=[("Archivos de texto", "*.txt")])
    return archivo

# Función principal que gestiona la entrada y salida
def analizar_y_guardar():
    archivo_entrada = seleccionar_archivo()  # Abrir cuadro de diálogo para elegir el archivo

    if not archivo_entrada:
        print("No se seleccionó ningún archivo.")
        return

    print(f"Archivo de entrada seleccionado: {archivo_entrada}")

    tokens = analizar_archivo(archivo_entrada)

    if not tokens:
        print("No se generaron tokens. Verifica el archivo de entrada.")
        return

    # Generar el archivo de salida basado en el nombre del archivo de entrada
    base_nombre = os.path.splitext(os.path.basename(archivo_entrada))[0]
    archivo_salida = f"{base_nombre}_Salida_Tokens.txt"

    guardar_tokens(tokens, archivo_salida)
    print(f"Análisis léxico finalizado. Resultados guardados en {archivo_salida}")

# Ejecutar el análisis de un archivo de prueba
if __name__ == "__main__":
    analizar_y_guardar()
