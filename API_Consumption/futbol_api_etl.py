import requests
import pandas as pd
import psycopg2

equipo = "Monterrey"
url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={equipo}"

print(f"Conectando a la API para extraer datos del club: {equipo}...\n")

respuesta = requests.get(url)

if respuesta.status_code == 200:
    try:
        datos_json = respuesta.json()
        
        if datos_json.get('teams') is not None:
            lista_equipos = []
            
            for club in datos_json['teams']:
                nombre = club.get('strTeam', 'Desconocido')
                liga = club.get('strLeague', 'Desconocido')
                estadio = club.get('strStadium', 'Desconocido')
                anio = club.get('intFormedYear', 'Desconocido')
                pais = club.get('strCountry', 'Desconocido')
                
                lista_equipos.append({
                    'Club': nombre,
                    'Liga': liga,
                    'Estadio': estadio,
                    'Año_Fundación': anio,
                    'País': pais
                })
            
            df_club = pd.DataFrame(lista_equipos)
            print("✅ ¡Extracción exitosa!\n")
            print(df_club.to_string(index=False))
            
            # ==========================================
            # FASE 4: CARGA A POSTGRESQL
            # ==========================================
            print("\nIniciando carga a la base de datos PostgreSQL...")
            try:
                # Cambia tu_password y osm_analytics por los reales
                conexion = psycopg2.connect(
                    host="localhost",
                    database="OSM_Analytics", 
                    user="postgres",
                    password="Ash39",   
                    port="5432"
                )
                cursor = conexion.cursor()

                # Crea la tabla si no existe
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clubes_api (
                        id SERIAL PRIMARY KEY,
                        nombre_club VARCHAR(100),
                        liga VARCHAR(100),
                        estadio VARCHAR(100),
                        anio_fundacion VARCHAR(10),
                        pais VARCHAR(50)
                    );
                """)

                # Prepara datos y ejecuta inserción
                registros = [tuple(x) for x in df_club.to_numpy()]
                consulta_sql = """
                    INSERT INTO clubes_api (nombre_club, liga, estadio, anio_fundacion, pais)
                    VALUES (%s, %s, %s, %s, %s);
                """
                
                cursor.executemany(consulta_sql, registros)
                conexion.commit()
                print(f"✅ ¡Éxito! Se insertó la información de {cursor.rowcount} club(es) en PostgreSQL.")

            except Exception as e:
                print(f"❌ Ocurrió un error en la base de datos: {e}")

            finally:
                if 'conexion' in locals() and conexion:
                    cursor.close()
                    conexion.close()
                    print("Conexión cerrada. Pipeline API -> PostgreSQL finalizado.")
            
        else:
            print("La API respondió correctamente, pero no encontró información de este equipo.")
            
    except requests.exceptions.JSONDecodeError:
        print("❌ CRÍTICO: El servidor no devolvió un JSON válido.")

else:
    print(f"Error de conexión. Código HTTP: {respuesta.status_code}")