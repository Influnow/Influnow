<<<<<<< HEAD
import sqlite3

try:
    # Conectar a la base de datos
    conn = sqlite3.connect('influnet.db')
    cursor = conn.cursor()

    # Ejecutar el comando PRAGMA para obtener la información de la tabla
    cursor.execute("PRAGMA table_info(usuarios);")
    table_info = cursor.fetchall()

    # Si no hay datos, muestra un mensaje
    if not table_info:
        print("La tabla 'usuarios' no existe o no contiene columnas.")
    else:
        # Mostrar la información de la tabla
        for column in table_info:
            print(column)

except sqlite3.Error as e:
    print(f"Error al acceder a la base de datos: {e}")

finally:
    # Cerrar la conexión
    if conn:
        conn.close()
=======
import sqlite3

try:
    # Conectar a la base de datos
    conn = sqlite3.connect('influnet.db')
    cursor = conn.cursor()

    # Ejecutar el comando PRAGMA para obtener la información de la tabla
    cursor.execute("PRAGMA table_info(usuarios);")
    table_info = cursor.fetchall()

    # Si no hay datos, muestra un mensaje
    if not table_info:
        print("La tabla 'usuarios' no existe o no contiene columnas.")
    else:
        # Mostrar la información de la tabla
        for column in table_info:
            print(column)

except sqlite3.Error as e:
    print(f"Error al acceder a la base de datos: {e}")

finally:
    # Cerrar la conexión
    if conn:
        conn.close()
>>>>>>> e744c4f819a1f3e70f49504c9a12526cc6f697f6
