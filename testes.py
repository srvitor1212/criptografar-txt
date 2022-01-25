

import unittest


from codificador import Codificar

class CodificadorTestes(unittest.TestCase):

    def test_len_msg_str(self):
        obj = Codificar()
        self.assertEqual(
            obj._len_msg_str('Mensagem'),
            '000008'
        )

    def test_len_msg(self):
        obj = Codificar()
        self.assertEqual(
            obj._len_msg('coded=222333kkklll'),
            111222
        )

    def test_entrada(self):
        text = 'Um mensagem qualquer! '
        obj = Codificar(text)
        self.assertEqual(
            obj.entrada,
            text
        )

    def test_saida(self):
        text = 'Um mensagem qualquer! '
        obj = Codificar(text)
        self.assertNotEqual(
            obj.criptografar(text),
            text
        )

    def test_descriptografar(self):
        text = 'Um mensagem qualquer! '
        obj = Codificar(text)
        obj.criptografar(text)
        self.assertEqual(
            obj.decriptografar(obj.codificado),
            text
        )


if __name__ == '__main__':
    print(f'\n' * 10)
    unittest.main()


def teste_completo():
    unittest.main()
