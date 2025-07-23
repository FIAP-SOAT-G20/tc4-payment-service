# language: pt

Funcionalidade: Checkout
  Esquema do Cenário: Resposta da API de checkout deve conter campos esperados
    Quando enviar um pedido ao checkout
    Então a resposta deve conter o campo <campo> no json

    Exemplos:
      | campo   |
      | qr_data |

#  Esquema do Cenário: Credenciais inválidas
#    Dado que ao entrar na página home
#    E que não exista usuário logado
#    Quando tentar efetuar o login com <nome>/<senha>
#    Então nenhum usuário deve estar autenticado
#    E deve abrir uma página com o título "Login" e com o erro "invalid credentials"
#
#    Exemplos:
#      | nome  | senha |
#      | admin | test  |