from flask import Flask, request, jsonify
from datetime import datetime

# Clase Operación segun el diagrama
class Operacion:
    def __init__(self, numero_destino, fecha, valor):
        self.numero_destino = numero_destino
        self.fecha = fecha
        self.valor = valor
        
# Clase Cuenta segun el diagrma
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
            operacion = Operacion(destino, datetime.now().strftime('%d/%m/%Y'), -valor)  
            self.operaciones.append(operacion)
            return True
        else:
            return False

    def recibir_pago(self, origen, valor):
        self.saldo += valor
        operacion = Operacion(origen, datetime.now().strftime('%d/%m/%Y'), valor)  
        self.operaciones.append(operacion)

    def obtener_contactos(self):
        return self.contactos

    def obtener_historial(self):
        historial = {
            "Saldo": self.saldo,
            "Operaciones": [{
                "NumeroDestino": operacion.numero_destino,
                "Fecha": operacion.fecha,
                "Valor": operacion.valor
            } for operacion in self.operaciones]
        }
        return historial

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
            nombres_contactos = {contacto: obtener_nombre_contacto(contacto) for contacto in contactos}
            return jsonify(nombres_contactos)
    return "Número de cuenta no encontrado", 404

# funcion extra para obtener el nombre de un contacto por su número de cuenta
def obtener_nombre_contacto(numero_contacto):
    for cuenta in BD:
        if cuenta.numero == numero_contacto:
            return cuenta.nombre
    return "Contacto no encontrado"


@app.route('/billetera/pagar', methods=['POST'])
def realizar_pago():
    num_cuenta = request.args.get('minumero')
    num_destino = request.args.get('numerodestino')
    valor = request.args.get('valor')

    # Verificar si el número de destino está presente
    if num_destino is None:
        return "Parámetros inválidos - numerodestino es obligatorio", 400

    valor = int(valor) if valor is not None else None  # Convertir a entero si es posible

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
            nombre_cuenta = next((cuenta.nombre for cuenta in BD if cuenta.numero == num_cuenta), "Cuenta no encontrada")
            historial_str = f"Saldo de {nombre_cuenta}: {historial['Saldo']}\nOperaciones de {nombre_cuenta}:\n"
            for operacion in historial['Operaciones']:
                historial_str += f"{obtener_tipo_operacion(operacion)} de {abs(operacion['Valor'])} de {obtener_nombre_cuenta(operacion['NumeroDestino'])} - Fecha: {operacion['Fecha']}\n"

            return historial_str
    return "Número de cuenta no encontrado", 404


# funcion extra de historial para obtener el tipo de operación
def obtener_tipo_operacion(operacion):
    if operacion['Valor'] > 0:
        return "Pago recibido"
    else:
        return "Pago realizado"

# funcion extra de historial para obtener el nombre de cuenta
def obtener_nombre_cuenta(numero_cuenta):
    for cuenta in BD:
        if cuenta.numero == numero_cuenta:
            return cuenta.nombre
    return "Cuenta no encontrada"


if __name__ == '__main__':
    app.run(debug=True)
    