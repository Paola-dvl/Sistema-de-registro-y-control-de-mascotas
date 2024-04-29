from django.shortcuts import render
from django.http import JsonResponse
import requests
import xmltodict
import json
from django.views.decorators.http import require_http_methods


def api_call(url):
    response = requests.get(url)
    print(response)
    return response

def inicio(request):
    return render(request, 'inicio.html')

@require_http_methods(["POST"])
def cargarArchivo(request):
    if request.method == 'POST' and request.FILES.get('xml_file'):
        xml_file = request.FILES['xml_file']
        files = {'file': xml_file}
        response = requests.post('http://localhost:8123/cargarArchivo', files=files)
        xml_data = response.text
        print(xml_data)
        data = json.loads(json.dumps(xmltodict.parse(xml_data)))
        if not 'estado' in data["resultados"]:
            data = {'resultados': {'xml': xml_data, 'json': data}}
        return JsonResponse(data=data, status=200)
    return JsonResponse(data={'data':{"estado": "Error", "mensaje": "Debe de cargar un archivo"}}, status=200)

@require_http_methods(["GET"])
def limpiarDatos(request):
    response = requests.get('http://localhost:8123/limpiarDatos')
    xml_data = response.text
    print(xml_data)
    return JsonResponse(data=json.loads(json.dumps(xmltodict.parse(xml_data))), status=200)

@require_http_methods(["GET"])
def procesarArchivos(request):
    response = requests.get('http://localhost:8123/procesarArchivos')
    xml_data = response.text
    print(xml_data)
    return JsonResponse(data={'xml': xml_data}, status=200)