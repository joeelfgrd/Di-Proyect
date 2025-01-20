#styles.py
def load_stylesheet():

    '''

    :return: boolean
    Carga y devuelve el contenido del archivo style.css como una cadena

    '''

    with open('styles.qss', 'r') as style_file:
        return style_file.read()