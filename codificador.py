

import math
import random
import os
import caracteres as car


CURR_DIR = os.path.dirname(os.path.realpath(__name__))

class Codificar:

    cifra = 1
    buffer = 100
    buffer_min = 0.5
    limite_bytes = 999000
    pref1 = 'coded='
    len_tail = 10

    def __init__(self, msg_entrada=None):
        self.__msg_entrada = msg_entrada
        self.__len_original = None
        self.__msg_codificada = None
        self.__msg_decodificada = None

    def __repr__(self):
        ret = ''

        len_entrada = 0
        len_decodificado = 0
        len_codificado = 0

        if self.entrada != None:
            len_entrada = len(self.entrada)

        if self.decodificado != None:
            len_decodificado = len(self.decodificado)

        if self.codificado != None:
            len_codificado = len(self.codificado)

        ret = (
            f'\n\n...> Entrada.......: [{self.entrada}]'
            f' - len:{len_entrada}'

            f'\n\n...> Decodificado..: [{self.decodificado}]'
            f' - len:{len_decodificado}'

            f'\n\n...> Codificado....: [{self.codificado}]'
            f' - len:{len_codificado}'

            f'\n\n...> Validade......: [{self.valido}]\n'
        )

        return ret
    
    @property
    def entrada(self):
        return self.__msg_entrada
    @property
    def codificado(self):
        return self.__msg_codificada
    @property
    def decodificado(self):
        return self.__msg_decodificada
    @property
    def valido(self):
        ret = False
        if self.__msg_entrada == self.__msg_decodificada:
            ret = True
        return ret

    @entrada.setter
    def entrada(self, valor):
        self.__msg_entrada = valor

    @codificado.setter
    def codificado(self, valor):
        self.__msg_codificada = valor

    @decodificado.setter
    def decodificado(self, valor):
        self.__msg_decodificada = valor


    # ------------------------------------------------------------------
    def _embaralhar(self, texto):
        ret = ''

        caracteres = car.char
        cifra1 = ''
        idx_tot = len(caracteres) - 1

        ind_texto = 0
        for t in texto:
            idx_texto = caracteres.index( t )
            len_embaralhar = len(texto) - self.len_tail

            if ind_texto < len_embaralhar:      # não embaralha o final da string
                if idx_texto == idx_tot:
                    cifra1 += caracteres[0]
                else:
                    cifra1 += caracteres[idx_texto + 1]
            else:
                cifra1 += t

            ind_texto += 1
        
        print(f'01 = {cifra1}.')

        cifra_alternada = self._cifra_alternada( texto )
        idx_cifra = 0
        ind_texto = 0
        for c in cifra1:
            idx_texto = caracteres.index( c )
            len_embaralhar = len(texto) - self.len_tail

            if ind_texto < len_embaralhar:      # não embaralha o final da string
                x = cifra_alternada[ idx_cifra - 1]
                proposta = idx_texto + x
                if proposta > idx_tot:
                    proposta = proposta - idx_tot
                    proposta = proposta - 1     # converte em índice da lista
                ret += caracteres[proposta]
            else:
                ret += c

            ind_texto += 1
            idx_cifra += 1
            if idx_cifra > self.len_tail:
                idx_cifra = 0

        print(f'02 = {ret}.')
        return ret

    def _cifra_alternada(self, texto):
        caracteres = car.char
        x = len(texto)
        y = x - self.len_tail
        cifra_alternada_str = texto[y:x]
        cifra_alternada = []
        for s in cifra_alternada_str:
            cifra_alternada.append( caracteres.index(s) )
        
        return cifra_alternada

    def _cifrar(self, byte, par_cifra=0):
        ret = ''

        caracteres = car.char
        tot_idx_lista = len(caracteres) - 1

        if par_cifra == 0:

            if byte in caracteres:
                cif = self.cifra                
                idx_byte = caracteres.index(byte)

                if idx_byte == tot_idx_lista:
                    ret = caracteres[0]
                else:
                    ret = caracteres[idx_byte + cif]
            else:
                raise ValueError(f'Símbolo [{byte}] não previsto')
        else:
            if byte in caracteres:
                idx_byte = caracteres.index(byte)
                cif = 0

                idx_cifrado = idx_byte + par_cifra
                if idx_cifrado > tot_idx_lista:
                    idx_cifrado = idx_cifrado - tot_idx_lista

                ret = caracteres[idx_cifrado]
            else:
                raise ValueError(f'2-Símbolo [{byte}] não previsto')

        return ret

    # ------
    def _decifrar(self, texto):
        ret = ''

        caracteres = car.char
        idx_tot = len(caracteres) - 1
        total_lista = len(caracteres)
        cifra_alternada = self._cifra_alternada( texto )

        idx_cifra = 0
        decode1 = ''
        for t in texto:
            idx_t = caracteres.index( t )
            x = cifra_alternada[ idx_cifra - 1 ]
            proposta = idx_t - x
            if proposta < 0:
                proposta = proposta + total_lista

            decode1 += caracteres[proposta]
            
            idx_cifra += 1
            if idx_cifra > self.len_tail:
                idx_cifra = 0

        print(f'03 = {decode1};')

        for d in decode1:
            idx_d = caracteres.index( d )
            ret += caracteres[ idx_d - 1 ]

        return ret

    # ------
    def _calc_buffer(self, texto):
        ret = ''

        len_txt = len(texto)
        y = len_txt / self.buffer

        if y < self.buffer_min:
            res = self.buffer
        else:
            y = math.ceil(y) # arredonda sempra para cima
            res = (y * self.buffer)
        
        ret = res + self.buffer

        return ret

    # ------
    def _add_buffer(self, texto, buffer):
        ret = ''

        caracteres = car.char
        len_texto = len(texto)
        for i in range(buffer):
            if i >= len_texto:
                idx_caracteres = len(caracteres) - 1
                sorteio = random.randint(0, idx_caracteres)
                ret += caracteres[sorteio]
            else:
                ret += texto[i]

        return ret

    # ------
    def _len_msg_str(self, msg):
        ret = ''

        x = len(str(self.limite_bytes))
        ret = len(msg)
        ret = str(ret).zfill(x)

        return ret

    # ------
    """
    def _len_msg(self, msg):
        ret = ''

        ini = len(self.pref1)
        fim = ini + len(str(self.limite_bytes))
        text = str(msg[ini : fim]) 
        text_decifrado = ''

        for t in text:
            text_decifrado += self._decifrar(t)        
        
        ret = int(text_decifrado)
        return ret
    """

    # ------------------------------------------------------------------
    def validar_texto(self, texto):
        ret = True

        if (texto == None) or (texto == 0):
            ret = 'Texto para codificação não pode ser vazio'

        if texto[0:6] == self.pref1:
            ret = 'Texto já codificado, use a função decriptografar'
        
        if len(texto) > self.limite_bytes:
            ret = f'Limite de {self.limite_bytes} bytes'

        return ret


    def criptografar(self, texto):
        ret = ''
        self.entrada = texto

        if self.validar_texto(texto) != True:
            raise ValueError(self.validar_texto(texto))

        buffer = self._calc_buffer(texto)
        pref2 = self._len_msg_str(texto)
        texto = f'{pref2}{texto}'        
        texto = self._add_buffer(texto, buffer - len(str(self.limite_bytes)) )
        ret = self._embaralhar(texto)        
        ret = f'{self.pref1}{ret}'

        self.codificado = ret
        self.decodificado = self.decriptografar(self.codificado)
        """
        if not self.valido:
            raise ValueError('Não foi possível garantir a integridade da mensagem')
        """

        return ret

    
    def decriptografar(self, texto):
        ret = ''
        len_coded = len(self.pref1)
        len_texto = len(texto)

        msg = texto[ len_coded:len_texto ]
        decode = self._decifrar( msg )

        len_tam_txt = len(str(self.limite_bytes))
        len_msg = decode[ 0 : len_tam_txt ]
        tam_msg = int(len_msg)
        tam_msg_ate = len_tam_txt + tam_msg

        ret = decode[ len_tam_txt : tam_msg_ate ]
        return ret
