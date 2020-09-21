


ALFABETO_ESPAÑOL = "abcdefghijklmnñopqrstuvwxyz"

class StringInputError(Exception):
    """Something wrong with the input string"""
    pass

# create a function generator for maping and reusability
def __desplazar_function_generator(desplazamiento:int = 0) -> str:

    def desplazar(char:str) -> str:

        # check edge cases
        if char and len(char) is 1:
            index_absoluto = (ALFABETO_ESPAÑOL.index(char) + desplazamiento) % len(ALFABETO_ESPAÑOL)
            return ALFABETO_ESPAÑOL[index_absoluto]

    return desplazar

def cifrar_string(mensaje:str, desplazamiento:int) -> str:

    """
        Dado un texto, por cada una de las letras del texto, añadirle un desplazamiento
        para conseguir una nueva letra diferente de la original. Ejemplo:

        cifrar_string("abc", 3) -> "def"
        
    """
    # check edge cases
    if mensaje and desplazamiento:
        if " " in mensaje:
            raise StringInputError("Wrong input character: ' '")
        
        # normalize and use the map function to encrypt
        mensaje = mensaje.lower()
        return "".join(list(map(__desplazar_function_generator(desplazamiento), mensaje)))
        