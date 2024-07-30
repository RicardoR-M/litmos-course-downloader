import time

import pandas as pd
from pymssql import OperationalError
from rich.console import Console
from sqlalchemy import create_engine
from os import getenv


def importa_litmos_sql(ruta_csv, servicio, tipo_reporte, id_curso, nombre_curso, tiene_quiz):
    console = Console()
    t0 = time.time()
    db_conn = getenv('DB_CONN')
    engine = create_engine(db_conn + 'CLARO_LITMOS')
    df = pd.read_csv(ruta_csv, encoding='utf8')

    if tipo_reporte == 'asesor':
        tabla_sql = 'TEMP_ASESORES'
        df['Servicio'] = servicio
        stored_proc = 'PROCESA_ASESORES'
    elif tipo_reporte == 'curso':
        tabla_sql = 'TEMP_CURSOS'
        df['tiene_quiz'] = tiene_quiz
        df['Servicio'] = servicio
        df['id_curso'] = id_curso
        df['nombre_curso'] = nombre_curso
        stored_proc = 'PROCESA_CURSOS'
    elif tipo_reporte == 'quiz':
        tabla_sql = 'TEMP_QUIZZES'
        df['Servicio'] = servicio
        df['id_curso'] = id_curso
        df['nombre_curso'] = nombre_curso
        stored_proc = 'PROCESA_QUIZZES'
    else:
        raise ValueError('importaSQL(tipo_reporte...) - NO VÁLIDO')

    df.to_sql(tabla_sql, con=engine, if_exists='replace', index=False)

    # Ejecuta SP en el servidor MSSQL
    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()
        cursor.callproc(stored_proc)
        cursor.close()
        connection.commit()
    except OperationalError as e:
        print(f'Problema con el SP: {stored_proc} - {e.args}')
    finally:
        connection.close()
    t1 = time.time()
    console.log(f'{id_curso} - SQL: {round(t1 - t0, 2)}')