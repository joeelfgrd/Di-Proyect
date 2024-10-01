#styles.py
def load_stylesheet():
    '''

    return: boolean
    carga y devuelve el contenido de styles.qss como una cadena de texto

    '''

    with open('styles.qss',"r") as style_file:
        return style_file.read()