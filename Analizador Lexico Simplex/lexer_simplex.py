import ply.lex as lex
import os
import tkinter as tk
from tkinter import filedialog

# Definición de las palabras clave (reservadas)
keywords = {
    'if', 'else', 'while', 'for', 'return', 'int', 'float', 'string', 'true', 'false', 'then'
}

# Definición de los tokens
tokens = [
    'KEYWORD', 'IDENTIFIER', 'INVALID_IDENTIFIER', 'OPERATOR', 'ASSIGNMENT_OPERATOR',
    'DELIMITER', 'NUMBER', 'STRING', 'COMMENT', 'UNRECOGNIZED_SYMBOL', 'ERROR'
]

# Expresiones regulares para los tokens
t_KEYWORD = r'\b(if|else|while|for|return|int|float|string|true|false|then)\b'
t_IDENTIFIER = r'[a-zA-Z_áéíóúÁÉÍÓÚ][a-zA-Z_0-9áéíóúÁÉÍÓÚ]*'  # Identificadores válidos
t_INVALID_IDENTIFIER = r'(\d|[@$-])[a-zA-Z_áéíóúÁÉÍÓÚ][a-zA-Z_0-9áéíóúÁÉÍÓÚ]*'  # Identificadores inválidos
t_OPERATOR = r'\+|\-|\*|\/|\=\=|\>|\<|\='  # Operadores matemáticos y de comparación
t_ASSIGNMENT_OPERATOR = r'\='  # Operador de asignación
t_DELIMITER = r'\;|\{|\}|\(|\)'  # Delimitadores
t_NUMBER = r'\d+\.\d+|\d+'  # Números, con o sin decimales
t_STRING = r'\"[^\"]*\"'  # Cadenas entre comillas
t_COMMENT = r'//.*'  # Comentarios de una sola línea
t_UNRECOGNIZED_SYMBOL = r'[\$\#]'  # Símbolos no reconocidos

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
    with open(archivo, 'r', encoding='utf-8') as f:  # Se especifica la codificación 'utf-8'
        data = f.read()
        
        # Verificación del contenido leído
        print("Contenido del archivo:")
        print(data)
        print("-" * 40)
        
        lexer.input(data)
        tokens_generados = []
        errores = []

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

        # Procesar errores
        if errores:
            print("Lista de errores:")
            for error in errores:
                print(f"Error en línea {error['line']}, columna {error['col']}: Símbolo no reconocido '{error['symbol']}'")

        print("-" * 40)

        return tokens_generados

# Función para guardar los tokens en un archivo de salida
def guardar_tokens(tokens, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as f:  # Se especifica la codificación 'utf-8' para la salida también
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
