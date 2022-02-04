

import math
import random
import os
import caracteres as car

CURR_DIR = os.path.dirname(os.path.realpath(__name__))

class Codificar:

    buffer = 50
    limite_bytes = 999000
    pref1 = 'coded='
    len_tail = 10

    # ------------------------------------------------------------------
    def __init__(self, msg_entrada=None):
        self.__msg_entrada = msg_entrada
        self.__len_original = None
        self.__msg_codificada = None
        self.__msg_decodificada = None

    # ------------------------------------------------------------------
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
        
        if len_entrada < 1000:
            ret = (
                f'\n...> Entrada.......: [{self.entrada}] - len:{len_entrada}'
                f'\n...> Decodificado..: [{self.decodificado}] - len:{len_decodificado}'
                f'\n...> Codificado....: [{self.codificado}] - len:{len_codificado}'
                f'\n...> Validade......: [{self.valido}]\n'
            )
        else:
            ret = (
                f'\n...> Representação reduzida <...'
                f'\n...> Entrada.......: [{self.entrada[0:1000]} ...] - len:{len_entrada}'
                f'\n...> Decodificado..: [{self.decodificado[0:1000]} ...] - len:{len_decodificado}'
                f'\n...> Codificado....: [{self.codificado[0:1000]} ...] - len:{len_codificado}'
                f'\n...> Validade......: [{self.valido}]\n'
            )

        return ret
    
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    @entrada.setter
    def entrada(self, valor):
        self.__msg_entrada = valor

    @codificado.setter
    def codificado(self, valor):
        self.__msg_codificada = valor

    @decodificado.setter
    def decodificado(self, valor):
        self.__msg_decodificada = valor


    """
    --------------------------------------------------------------------------------

        Abaixo são os métodos principais que gerenciam todo o processo de 
        embaralhamento e desembaralhamento do texto enviado a eles.

    --------------------------------------------------------------------------------
    """
    def criptografar(self, texto):
        """
            Criptografa o texto de entrada
        """
        ret = ''
        self.entrada = texto

        if self._validar_texto(texto) != True:
            raise ValueError(self._validar_texto(texto))

        buffer = self._calc_buffer(texto)
        pref2 = self._len_msg_str(texto)
        texto = f'{pref2}{texto}'
        texto = self._add_buffer(texto, buffer)

        ret = self._embaralhar(texto)

        ret = f'{self.pref1}{ret}'
        self.codificado = ret
        self.decodificado = self.decriptografar(self.codificado)

        if not self.valido:
            raise ValueError('Não foi possível garantir a integridade da mensagem')

        return ret


    def decriptografar(self, texto):
        """
            Decriptografa o texto de entrada
        """
        ret = ''

        if self.codificado == None:
            self.codificado = texto

        msg = self._remove_coded( texto )

        decode = self._decifrar( msg )

        len_tam_txt = len(str(self.limite_bytes))
        len_msg = decode[ 0 : len_tam_txt ]
        tam_msg = int(len_msg)
        tam_msg_ate = len_tam_txt + tam_msg

        ret = decode[ len_tam_txt : tam_msg_ate ]
        self.decodificado = ret
        return ret


    """
    --------------------------------------------------------------------------------

        Abaixo são os métodos auxiliares que realizam as operações de
        forma individual, cada um com seu propósito.

    --------------------------------------------------------------------------------
    """
    def _validar_texto(self, texto):
        """
            Faz check da entrada de texto e estabelce padrões
        """
        ret = True

        tp = type(texto)
        if tp != str:
            ret = 'O formato de entrada precisa ser string!'

        if (texto == None) or (texto == 0):
            ret = 'Texto para codificação não pode ser vazio'

        if texto[0:6] == self.pref1:
            ret = 'Texto já codificado, use a função decriptografar'
        
        if len(texto) > self.limite_bytes:
            ret = f'Limite de {self.limite_bytes} bytes. Foram enviados: {len(texto)}'

        if self.buffer <= 30:
            ret = f'O buffer precisa ser maior que 30'

        return ret


    def _embaralhar(self, texto):
        """
            Método principal de cirptografia do texto
        """
        ret = ''

        caracteres = car.char
        cifra1 = ''
        idx_tot = len(caracteres) - 1

        ind_texto = 0
        for t in texto:
            if t in caracteres:
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
            else:
                raise ValueError(f'Símbolo não previsto: {t}')


        cifra_alternada = self._cifra_alternada( texto )
        idx_cifra = 0
        ind_texto = 0
        for c in cifra1:
            if c in caracteres:
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
            else:
                raise ValueError(f'Símbolo não previsto: {c}')

        return ret


    def _decifrar(self, texto):
        """
            Método principal para decriptografar texto
        """
        ret = ''

        caracteres = car.char
        idx_tot = len(caracteres) - 1
        total_lista = len(caracteres)
        cifra_alternada = self._cifra_alternada( texto )

        idx_cifra = 0
        decode1 = ''
        for t in texto:
            if t in caracteres:
                idx_t = caracteres.index( t )
                x = cifra_alternada[ idx_cifra - 1 ]
                proposta = idx_t - x
                if proposta < 0:
                    proposta = proposta + total_lista

                decode1 += caracteres[proposta]

                idx_cifra += 1
                if idx_cifra > self.len_tail:
                    idx_cifra = 0
            else:
                raise ValueError(f'Símbolo não previsto: {t}')

        for d in decode1:
            if d in caracteres:
                idx_d = caracteres.index( d )
                ret += caracteres[ idx_d - 1 ]
            else:
                raise ValueError(f'Símbolo não previsto: {d}')

        return ret


    def _cifra_alternada(self, texto):
        """
            Pega os últimos caracteres do texto de acordo com len_tail
            para usar como cifra alternada.
            Baseado nesses caracteres, pega o indice deles de caracteres.py
            para usar na cifra depois.

            Restorna uma lista
        """
        caracteres = car.char
        x = len(texto)
        y = x - self.len_tail
        cifra_alternada_str = texto[y:x]
        cifra_alternada = []
        for s in cifra_alternada_str:
            cifra_alternada.append( caracteres.index(s) )
        
        return cifra_alternada


    def _calc_buffer(self, texto):
        """
            Calcula o tamanho que o texto criptografado deve ter
            de acordo com a variável self.buffer.
        """
        ret = ''

        len_txt = len(texto)
        y = len_txt / self.buffer
        y = math.ceil(y) # arredonda sempra para cima
        res = (y * self.buffer)

        ret = res + self.buffer
        return ret


    def _add_buffer(self, texto, buffer):
        """
            Retorna o centudo do texto + caracteres aleatórios
            A quantidade total do retorno é definida de acordo com buffer 
            que deve ser passado na função

            Os caracteres respeitão a lista em caracteres.py
        """
        ret = ''

        caracteres = car.char
        len_texto = len(texto)
        idx_caracteres = len(caracteres) - 1
        for i in range(buffer):
            if i >= len_texto:
                sorteio = random.randint(0, idx_caracteres)
                ret += caracteres[sorteio]
            else:
                ret += texto[i]

        return ret


    def _len_msg_str(self, msg):
        """
            Restorna o length da msg em um string de 6 posições
        """
        ret = ''

        x = len(str(self.limite_bytes))
        ret = len(msg)
        ret = str(ret).zfill(x)

        return ret


    def _remove_coded(self, txt):
        """
            Recebe um string exemplo: coded=meu nome é vitor
            E retorna o string sem o coded, exemplo: meu nome é vitor
        """
        ret = txt

        if txt[0:6] == self.pref1:
            len_coded = len(self.pref1)
            len_texto = len(txt)
            ret = txt[ len_coded:len_texto ]

        return ret
