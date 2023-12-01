import unittest
from code_fuente import app

class TestPagos(unittest.TestCase):

    # Caso de éxito: Pago exitoso
    def test_pago_exitoso(self):
        tester = app.test_client(self)
        response = tester.post('/billetera/pagar?minumero=123&numerodestino=456&valor=50')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Transacción realizada", response.data.decode("utf-8"))

    # Caso de error: Saldo insuficiente
    def test_saldo_insuficiente(self):
        tester = app.test_client(self)
        response = tester.post('/billetera/pagar?minumero=123&numerodestino=456&valor=500')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Saldo insuficiente para realizar la transacci\xc3\xb3n", response.data)


    # Caso de error: Cuenta no encontrada
    def test_cuenta_no_encontrada(self):
        tester = app.test_client(self)
        response = tester.post('/billetera/pagar?minumero=999&numerodestino=456&valor=50')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Cuenta de origen o destino no encontrada", response.data)

  # Caso de error: Parámetros inválidos (falta 'numerodestino')
    def test_parametros_invalidos(self):
        tester = app.test_client(self)
        response = tester.post('/billetera/pagar?minumero=123&valor=50')  # Falta el 'numerodestino'
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Par\xc3\xa1metros inv\xc3\xa1lidos - numerodestino es obligatorio", response.data)



if __name__ == '__main__':
    unittest.main()
