

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
        len_txt = len(obj._add_buffer( txt, 20 ) )
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



if __name__ == '__main__':
    print(f'\n' * 10)
    unittest.main()
