import random
import time

from os import getenv
from dotenv import dotenv_values
from rich.console import Console
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from config.litmos_cursos import cursos_litmos
from config.utils import download_wait, limpia_data_folder
from to_sql import importa_litmos_sql


def dl_reporte_litmos(drver, link, dl_dir, nombre_reporte, web_timeout, dl_timeout):
    console = Console()
    t0 = time.time()
    drver.get(link)
    # clic en el boton descargar informe
    time.sleep(1)
    WebDriverWait(drver, web_timeout).until(expected_conditions.visibility_of_element_located((By.ID, 'open_export'))).click()
    time.sleep(1)
    # espera a que el textfield aparezca
    WebDriverWait(drver, web_timeout).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="title"]')))
    # Limpia y escribe el nombre del reporte
    drver.find_element_by_id('title').clear()
    nombre_exp = nombre_reporte + '_' + str(random.randint(1000, 9999))
    drver.find_element_by_id('title').send_keys(nombre_exp)
    # exporta el reporte
    drver.find_element_by_id('submit_export').click()

    # for que espera a que el nombre del 1er LI coincida por el que generamos, así nos aseguramos
    # de descargar el archivo correcto
    # todo Verificar funcionamiento del for
    timeout = web_timeout
    for seconds in range(timeout):
        # noinspection TryExceptContinue,PyBroadException
        try:
            time.sleep(1)
            seconds += 1
            if drver.find_element_by_xpath('//*[@id="downloads"]/li[1]').text == nombre_exp:
                break
        except Exception:
            if seconds >= timeout - 1:
                raise Exception('timeout: se sobrepaso el tiempo de espera para generacion de exportado')
            continue

    # clic en al nombre del archivo para descargarlo
    drver.find_element_by_xpath('//*[@id="downloads"]/li[1]/a').click()

    # espera a que el archivo termine de bajar en la carpeta data
    download_wait(dl_dir, nombre_exp + '.csv', dl_timeout)
    t1 = time.time()
    console.log(f'{nombre_reporte} - Descarga: {round(t1 - t0, 2)}')
    return dl_dir + '\\' + nombre_exp + '.csv'


# todo agregar verificación de que se ingresó a la web satisfactoriamente con las credenciales
def dl_litmos(driver, download_dir, web_timeout, dl_timeout):
    asesores_link = getenv('ASESORES_LINK')
    limpia_data_folder(download_dir)

    #########################################################################################
    # Login LITMOS                                                                          #
    #########################################################################################
    user_config = dotenv_values('.env')
    usuario = user_config['USUARIO_LITMOS']
    pwd = user_config['PWD_LITMOS']

    driver.get('https://ecx.litmos.com/account/Login')
    driver.find_element_by_id('Username').send_keys(usuario)
    driver.find_element_by_id('Password').send_keys(pwd)
    driver.find_element_by_id('login-button').click()

    for servicio in cursos_litmos:
        if not servicio['activo']:
            continue

        campanha = servicio['servicio']
        # Carga el dashboard del servicio (es necesario para cambiar de campaña)
        driver.get(servicio['link_servicio'])

        #########################################################################################
        # Descarga la base de asesores de litmos que contiene los usuarios de litmos #
        #########################################################################################
        ruta_reporte = dl_reporte_litmos(driver, asesores_link, download_dir, 'asesores' + '_' + campanha, web_timeout, dl_timeout)
        importa_litmos_sql(ruta_reporte, campanha, 'asesor', None, None, None)

        for curso in servicio['cursos']:
            # verifica si el curso está activo
            if not curso['activo']:
                continue

            # Verifica si tiene link de quiz
            tiene_quiz = bool(curso['link_examen'])

            # Descarga el curso
            ruta_reporte = dl_reporte_litmos(driver, curso['link_curso'], download_dir, curso['id_curso'], web_timeout, dl_timeout)
            # console.log(f'Importando "{curso["id_curso"]}" a SQL')
            importa_litmos_sql(ruta_reporte, campanha, 'curso', curso['id_curso'], curso['nombre_curso'], tiene_quiz)

            # Descarga el examen
            if not tiene_quiz:
                continue
            ruta_reporte = dl_reporte_litmos(driver, curso['link_examen'], download_dir, curso['id_curso'] + '_quiz', web_timeout, dl_timeout)
            importa_litmos_sql(ruta_reporte, campanha, 'quiz', curso['id_curso'], curso['nombre_curso'], None)