from datetime import datetime
from flask import Flask, request, jsonify

class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.operaciones = []

    def realizar_pago(self, destino, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            self.operaciones.append(f"Pago realizado de {valor} a {destino} - Realizado en {datetime.now().strftime('%d/%m/%Y')}")
            return True
        else:
            return False

    def recibir_pago(self, origen, valor):
        self.saldo += valor
        self.operaciones.append(f"Pago recibido de {valor} de {origen} - Realizado en {datetime.now().strftime('%d/%m/%Y')}")

    def obtener_contactos(self):
        return self.contactos

    def obtener_historial(self):
        return {
            "Saldo": self.saldo,
            "Operaciones": self.operaciones
        }

# DESARROLLO DE ENDPOINTS
app = Flask(__name__)

BD = [
    Cuenta("21345", "Arnaldo", 200, ["123", "456"]),
    Cuenta("123", "Luisa", 400, ["456"]),
    Cuenta("456", "Andrea", 300, ["21345"])
]

# endpoint para contactos:
@app.route('/billetera/contactos', methods=['GET'])
def obtener_contactos():
    num_cuenta = request.args.get('minumero')
    for cuenta in BD:
        if cuenta.numero == num_cuenta:
            contactos = cuenta.obtener_contactos()
            return jsonify({contacto: BD[int(contacto)].nombre for contacto in contactos})
    return "Número de cuenta no encontrado", 404


# endpoint para pagar: 
@app.route('/billetera/pagar', methods=['POST'])
def realizar_pago():
    num_cuenta = request.args.get('minumero')
    num_destino = request.args.get('numerodestino')
    valor = int(request.args.get('valor'))

    cuenta_origen = next((cuenta for cuenta in BD if cuenta.numero == num_cuenta), None)
    cuenta_destino = next((cuenta for cuenta in BD if cuenta.numero == num_destino), None)

    if cuenta_origen and cuenta_destino:
        if cuenta_origen.realizar_pago(num_destino, valor):
            cuenta_destino.recibir_pago(num_cuenta, valor)
            return f"Transacción realizada - Realizado en {datetime.now().strftime('%d/%m/%Y')}"
        else:
            return "Saldo insuficiente para realizar la transacción", 400
    else:
        return "Cuenta de origen o destino no encontrada", 404


# endpoint para historial
@app.route('/billetera/historial', methods=['GET'])
def obtener_historial():
    num_cuenta = request.args.get('minumero')
    for cuenta in BD:
        if cuenta.numero == num_cuenta:
            historial = cuenta.obtener_historial()
            return jsonify(historial)
    return "Número de cuenta no encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)
