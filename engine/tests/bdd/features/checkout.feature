# language: pt

Funcionalidade: Checkout
  Esquema do Cenário: Resposta da API de checkout deve conter campos esperados
    Quando enviar um pedido ao checkout
    Então a resposta deve conter o campo <campo> no json

    Exemplos:
      | campo   |
      | qr_data |
