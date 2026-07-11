from config import PLANES, GENEROS_FIJOS
import random

def escoger_plan():
    '''Escoge el tipo de plan (free, premium, familiar)'''
    numero = random.randint(0,2) 
    return PLANES[numero]

def escoger_genero():
    '''Escoge un genero entre el catalogo disponible'''
    return random.choice(GENEROS_FIJOS)