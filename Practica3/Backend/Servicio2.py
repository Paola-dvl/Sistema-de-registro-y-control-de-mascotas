from flask import Flask, make_response, request
import xmltodict
import json

class Informacion:
    class Animal:
        def __init__(self, edad, raza, nombre):
            self.nombre = nombre
            self.edad = edad
            self.raza = raza

    def __init__(self):
        self.animales = []
        self.perros = 0
        self.conejos = 0
        self.gatos = 0
        
    def agregarAnimal(self, edad, raza, nombre):
        animal = self.Animal(edad, raza, nombre)
        self.animales.append(animal)
        if nombre == "perro": 
            self.perros += 1
        elif nombre == "gato": 
            self.gatos += 1
        else: 
            self.conejos += 1

    def obtenerAnimales(self):
        return {
            "animales": { 
                "perros": {
                    "cantidadTotal": self.perros,
                },
                "gatos": {
                    "cantidadTotal": self.gatos,
                },
                "conejos": {
                    "cantidadTotal": self.conejos,
                }
            }
        }

app = Flask(__name__)
info = Informacion()

def dict_to_xml(data):
    def dict_to_xml_helper(data):
        xml = []
        for key, value in data.items():
            if isinstance(value, dict):
                xml.append('<{0}>{1}</{0}>'.format(key, dict_to_xml_helper(value)))
            else:
                xml.append('<{0}>{1}</{0}>'.format(key, value))
        return ''.join(xml)

    return '<resultados>{0}</resultados>'.format(dict_to_xml_helper(data))

@app.route('/cargarArchivo', methods=['POST'])
def cargarArchivo():
    respuesta = {}
    if 'file' not in request.files:
        respuesta = {'estado': 'error', 'mensaje': 'No se proporcionó ningún archivo XML'}
    else:
        try:
            xml_file = request.files['file']
            xml_content = xml_file.read()
            ingresoAnimales = json.loads(json.dumps(xmltodict.parse(xml_content)))['ingresoAnimales']
            for especie, detalles in ingresoAnimales.items():
                especie = str(especie)
                if especie == "perro" or especie == "gato" or especie == "conejo":
                    for detalle in detalles:
                        if type(detalle) == str:
                            info.agregarAnimal(detalles['edad'], detalles['raza'], especie)
                            break
                        else:
                            info.agregarAnimal(detalle['edad'], detalle['raza'], especie)
            respuesta = {'estado': 'correcto', 'mensaje': 'Animales cargados con éxito'}
        except:
            respuesta = {'estado': 'error', 'mensaje': 'Error al leer el formato del xml'}
    xml_data = dict_to_xml(respuesta)
    response = make_response(xml_data)
    response.headers['Content-Type'] = 'text/xml'
    return response
    
@app.route('/limpiarDatos',  methods=['GET'])
def limpiarDatos():
    global info 
    info = Informacion()
    data = {'estado': 'correcto', 'mensaje': 'Datos limpiados con éxito'}
    xml_data = dict_to_xml(data)
    response = make_response(xml_data)
    response.headers['Content-Type'] = 'text/xml'
    return response

@app.route('/procesarArchivos',  methods=['GET'])
def procesarArchivos():
    data = info.obtenerAnimales()
    xml_data = dict_to_xml(data)
    response = make_response(xml_data)
    response.headers['Content-Type'] = 'text/xml'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8123)  