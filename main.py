

import codificador as cod
import testes

#msg_entrada = str(input('Mensagem: '))
#msg_entrada = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
#msg_entrada = "Lorem Ipsum is simply dummy text of the printing and typesetting."
#msg_entrada = "Teste"
#msg_entrada = ""
msg_entrada = ")(ABCDEFG ''2023"

x = cod.Codificar()
x.criptografar(msg_entrada)
print(x)

y = ''
y = x.codificado
obj = cod.Codificar()
obj.decriptografar(y)
print(obj)


testar = testes.teste_completo() 