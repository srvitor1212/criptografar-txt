

from codificador import Codificar
import testes


"""
    Usando o objeto dentro de um programa
"""
obj = Codificar()
obj.criptografar('Mensagem que desejo criptografar!')
print(obj)

texto_codificado = obj.codificado
obj2 = Codificar()
decodificado = obj2.decriptografar(texto_codificado)
print(f'[{decodificado}]')
