import pandas as pd
import psycopg2

# ==========================================
# FASE 1: EXTRACCIÓN (Simulando un CSV sucio)
# ==========================================
datos_sucios = [
    {'nombre': '  guido Pizarro  ', 'valoracion': 81, 'id_equipo': 3}, # Espacios extra y minúsculas
    {'nombre': 'javier AQUINO', 'valoracion': None, 'id_equipo': 3}, # Le falta la valoración (Nulo)
    {'nombre': '  JULIAN quiñones ', 'valoracion': '85', 'id_equipo': 4}, # Valoración escrita como texto
    {'nombre': 'álvaro fidalgo', 'valoracion': 84, 'id_equipo': 4}
]

# Convertimos la lista cruda en un DataFrame (la tabla virtual de Pandas)
df = pd.DataFrame(datos_sucios)
print("--- DATOS ORIGINALES (SUCIOS) ---")
print(df)


# ==========================================
# FASE 2: TRANSFORMACIÓN (Limpieza con Pandas)
# ==========================================
# a) Limpiar Nombres: Quitar espacios accidentales (.strip) y poner formato Título (.title)
df['nombre'] = df['nombre'].str.strip().str.title()

# b) Manejar Nulos (NaN): Si falta la valoración, le asignamos un 75 por defecto
df['valoracion'] = df['valoracion'].fillna(75)

# c) Estandarizar Tipos de Datos: Forzar a que toda la columna de valoración sea número entero
df['valoracion'] = df['valoracion'].astype(int)

print("\n--- DATOS TRANSFORMADOS (LIMPIOS) ---")
print(df)

# Convertimos el DataFrame limpio a una lista de tuplas para que PostgreSQL lo entienda
registros_limpios = list(df.itertuples(index=False, name=None))


# ==========================================
# FASE 3: CARGA (Inyección a PostgreSQL)
# ==========================================
try:
    conexion = psycopg2.connect(
        host="localhost",
        database="OSM_Analytics",
        user="postgres",
        password="Ash39" 
    )
    cursor = conexion.cursor()
    
    consulta_sql = """
        INSERT INTO Jugadores (nombre, valoracion, id_equipo) 
        VALUES (%s, %s, %s);
    """
    
    # Inyectamos la lista que Pandas acaba de limpiar
    cursor.executemany(consulta_sql, registros_limpios)
    conexion.commit() 
    
    print(f"\n¡Éxito! Se inyectaron {cursor.rowcount} jugadores limpios a la base de datos.")

except Exception as e:
    print(f"\nOcurrió un error en la base de datos: {e}")

finally:
    if 'conexion' in locals() and conexion:
        cursor.close()
        conexion.close()