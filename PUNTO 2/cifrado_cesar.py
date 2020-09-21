


ALFABETO_ESPAÑOL = "abcdefghijklmnñopqrstuvwxyz"

class InputError(Exception):
    """Something wrong with the input"""
    pass


def cifrar_string(mensaje:str, desplazamiento:int) -> str:

    """
        Dado un texto, por cada una de las letras del texto, añadirle un desplazamiento
        para conseguir una nueva letra diferente de la original. Ejemplo:

        cifrar_string("abc", 3) -> "def"
        
    """
    # check edge cases
    if type(mensaje) is not str:
        raise InputError("Wrong input 'mensaje', expected str not ", type(mensaje))
    elif type(desplazamiento) is not int:
        raise InputError("Wrong input 'desplazamiento', expected int not ", type(mensaje))
    elif " " in mensaje:
        raise InputError("Wrong input character: ' '")

    mensaje = mensaje.lower()

    # create a mapper function to generate the ne characters
    mapper_function = lambda char: ALFABETO_ESPAÑOL[
        (ALFABETO_ESPAÑOL.index(char) + desplazamiento) % len(ALFABETO_ESPAÑOL)
    ]

    # normalize and use the map function to encrypt
    return "".join(list(map(mapper_function, mensaje)))
        