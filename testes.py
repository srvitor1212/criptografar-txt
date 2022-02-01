

import unittest


from codificador import Codificar

class CodificadorTestes(unittest.TestCase):


    def test_remove_coded(self):
        obj = Codificar()
        
        txt = 'coded=uma string'
        self.assertEqual(
            obj._remove_coded(txt),
            'uma string'
        )

        txt = 'xcoded=uma string'
        self.assertEqual(
            obj._remove_coded(txt),
            'xcoded=uma string'
        )


    def test_len_msg_str(self):
        obj = Codificar()

        txt = 'vitor'
        self.assertEqual(
            obj._len_msg_str(txt),
            '000005'
        )


    def test_add_buffer(self):
        obj = Codificar()

        txt = 'Teste buffer'
        self.assertEqual(
            obj._add_buffer(txt, 12),
            'Teste buffer'
        )

        txt = 'Teste buffer'
        self.assertEqual(
            len( obj._add_buffer( txt, 20 ) ),
            20
        )

    
    def test_calc_buffer(self):
        obj = Codificar()

        txt = '010_xxxxxx'
        self.assertEqual(
            obj._calc_buffer( txt ),
            obj.buffer * 2
        )

        txt = '200_xxxxxx123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890200_xxxxxx123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
        self.assertEqual(
            obj._calc_buffer( txt ),
            200 + obj.buffer
        )


    def test_cifra_alternada(self):
        obj = Codificar()

        txt = '1234567890'
        self.assertEqual(
            obj._cifra_alternada( txt ),
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        )

        txt = "texto qualquer }| é,.!'()"
        self.assertEqual(
            obj._cifra_alternada( txt ),
            [75, 76, 77, 78, 79, 80, 81, 82, 83, 84]
        )


    """

        Teste dos dois métodos principais do programa
        
    """
    cript_decrip_entrada = "}| é,.!'() texto para criptografar }| é,.!'()"
    cript_decrip_obj = Codificar()        
    cript_decrip_obj.criptografar(cript_decrip_entrada)
    cript_decrip_processado = cript_decrip_obj.decodificado

    def test_criptografar(self):
        self.assertEqual(
            self.cript_decrip_processado,
            self.cript_decrip_entrada
        )


    def test_decriptografar(self):
        obj = Codificar()

        self.assertEqual(
            obj.decriptografar(self.cript_decrip_obj.codificado),
            self.cript_decrip_entrada
        )


if __name__ == '__main__':
    print(f'\n' * 10)
    print(f'*** Iniciando testes ***\n')
    unittest.main()
