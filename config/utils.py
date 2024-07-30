import glob
import os
import time


def download_wait(path_to_downloads, filename, timeout):
    secs = 0
    dl_wait = True
    while dl_wait and secs <= timeout:
        time.sleep(1)
        for fname in os.listdir(path_to_downloads):
            if fname == filename:
                dl_wait = False
                break
        secs += 1
    if secs > timeout:
        raise TimeoutError(f'Se supero el tiempo de espera para la descarga del archivo {filename}')
    return secs


def download_wait_ext(path_to_downloads, extension, timeout):
    secs = 0
    dl_wait = True

    while dl_wait and secs < timeout:
        time.sleep(1)
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.' + extension):
                dl_wait = False
                break
        secs += 1
    if secs > timeout:
        raise TimeoutError(f'Se supero el tiempo de espera para la descarga del archivo en la carpeta {path_to_downloads}')
    return secs


def limpia_data_folder(data_folder):
    data_folder += '\\*'
    files = glob.glob(data_folder)
    for file in files:
        os.remove(file)


# retorna el path completo del archivo
def get_file_name(data_folder, extension):
    data_folder += '\\*.' + extension
    files = glob.glob(data_folder)
    for file in files:
        return file
    raise FileNotFoundError(f'func: get_file_name - No se encontro archivo con la estensión {extension}')
