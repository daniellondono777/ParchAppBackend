from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

from .models import *

def todatetime(fecha):
    return datetime.strptime(fecha, '%d-%m-%Y %H:%M')

def todate(fecha):
    return datetime.strptime(fecha, '%d-%m-%Y')

def tohora(hora):
    return datetime.strptime(hora, '%H:%M')

#Login Cliente
@csrf_exempt
def login_cliente(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('username', '') and data.get('password', ''):
            cliente = Cliente.objects.filter(username = data.get('username', '')).first()
            if cliente and data.get('password', '') == cliente.password:
                clientejson = serializers.serialize('json', [cliente])
                return HttpResponse(clientejson, 'application/json')
            else:
                return HttpResponse('Usuario o contrasena incorrectos', status=400)
        else :
            return HttpResponse('Parametros invalidos', status=400)
    else:
        return HttpResponse('This should be a POST request', status=400)

#Login Representante
@csrf_exempt
def login_representante(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('username', '') and data.get('password', ''):
            representante = RepresentanteLocal.objects.filter(username = data.get('username', '')).first()
            if representante and data.get('password', '') == representante.password:
                representantejson = serializers.serialize('json', [representante])
                return HttpResponse(representantejson, 'application/json')
            else:
                return HttpResponse('Usuario o contrasena incorrectos', status=400)
        else :
            return HttpResponse('Parametros invalidos', status=400)
    else:
        return HttpResponse('This should be a POST request', status=400)

#CRUD del modelo 'Grupo'
@csrf_exempt
def grupos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('nombre', '') and data.get('imagen', '') and data.get('balance', ''):
            nombre = data.get('nombre', '')
            imagen = data.get('imagen', '')
            balance = data.get('balance', '')
            grupo = Grupo.objects.create(nombre = nombre, imagen = imagen, balance = balance)
            grupo.save()
            grupojson = serializers.serialize('json', [grupo])
            return HttpResponse(grupojson, 'application/json')
        else:
            return HttpResponse('Parametros invalidos', status=400)

    grupos = Grupo.objects.all()
    grupojson = serializers.serialize('json', grupos)
    return HttpResponse(grupojson, 'application/json')

@csrf_exempt
def grupoId(request, id):

    grupo = Grupo.objects.filter(pk = id).first()

    if not grupo:
        return HttpResponse(f'No existe un grupo con el id {id}', status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('nombre', '') and data.get('imagen', '') and data.get('balance', ''):
            grupo.nombre = data.get('nombre', '')
            grupo.imagen = data.get('imagen', '')
            grupo.balance = data.get('balance', '')
            grupo.save()
            grupojson = serializers.serialize('json', [grupo])
            return HttpResponse(grupojson, 'application/json')
        else:
            return HttpResponse('Parametros invalidos', status=400)

    if request.method == 'DELETE':
        grupo.delete()
        return HttpResponse(f'Grupo {id} eliminado correctamente', status=204)
    
    grupojson = serializers.serialize('json', [grupo])
    return HttpResponse(grupojson, 'application/json')

#GET planes de un grupo
def planes_grupo(request, id):
    if not Grupo.objects.filter(pk = id).first():
        return HttpResponse(f'No existe un grupo con el id {id}', status=404)

    planes = Plan.objects.filter(grupo = id)
    planesjson = serializers.serialize('json', planes)
    return HttpResponse(planesjson, 'application/json')

#GET Clientes de un grupo
def clientes_grupo(request, id):
    grupo = Grupo.objects.filter(pk = id).first()
    if not grupo:
        return HttpResponse(f'No existe un grupo con el id {id}', status=404)
    
    clientes = grupo.cliente_set.all()
    clientesjson = serializers.serialize('json', clientes)
    return HttpResponse(clientesjson, 'application/json')

#CRUD del modelo 'Plan'
@csrf_exempt
def planes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('nombre', '') and data.get('descripcion', '') and data.get('presupuesto', '') and data.get('horaInicia', '') and (data.get('grupo', '') or data.get('grupo', '') == None) and (data.get('lugar', '') or data.get('lugar', '') == None) and (data.get('evento', '') or data.get('evento', '') == None):
            nombre = data.get('nombre', '')
            descripcion = data.get('descripcion', '')
            presupuesto = data.get('presupuesto', '')
            horaInicia = tohora(data.get('horaInicia', ''))
            grupo = data.get('grupo', '')
            lugar = data.get('lugar', '')
            evento = data.get('evento', '')
            if grupo != None and not Grupo.objects.filter(pk = grupo).first():
                return HttpResponse(f'No existe un grupo con el id {grupo}', status=404)
            grupo = Grupo.objects.filter(pk = grupo).first()
            if lugar != None and not Lugar.objects.filter(pk = lugar).first():
                return HttpResponse(f'No existe un lugar con el id {lugar}', status=404)
            lugar = Lugar.objects.filter(pk = lugar).first()
            if evento != None and not Evento.objects.filter(pk = evento).first():
                return HttpResponse(f'No existe un evento con el id {evento}', status=404)
            evento = Evento.objects.filter(pk = evento).first()
            plan = Plan.objects.create(nombre = nombre, descripcion = descripcion, presupuesto = presupuesto, horaInicia = horaInicia, grupo = grupo, lugar = lugar, evento = evento)
            plan.save()
            planjson = serializers.serialize('json', [plan])
            return HttpResponse(planjson, 'application/json')
        return HttpResponse('Parametros invalidos', status=400)

    planes = Plan.objects.all()
    planesjson = serializers.serialize('json', planes)
    return HttpResponse(planesjson, 'application/json')

@csrf_exempt
def planId(request, id):

    plan = Plan.objects.filter(pk = id).first()

    if not plan:
        return HttpResponse(f'No existe un plan con el id {id}', status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('nombre', '') and data.get('descripcion', '') and data.get('presupuesto', '') and data.get('horaInicia', '') and (data.get('grupo', '') or data.get('grupo', '') == None) and (data.get('lugar', '') or data.get('lugar', '') == None) and (data.get('evento', '') or data.get('evento', '') == None):
            plan.nombre = data.get('nombre', '')
            plan.descripcion = data.get('descripcion', '')
            plan.presupuesto = data.get('presupuesto', '')
            plan.horaInicia = tohora(data.get('horaInicia', ''))
            grupo = data.get('grupo', '')
            lugar = data.get('lugar', '')
            evento = data.get('evento', '')
            if grupo != None and not Grupo.objects.filter(pk = grupo).first():
                return HttpResponse(f'No existe un grupo con el id {grupo}', status=404)
            grupo = Grupo.objects.filter(pk = grupo).first()
            if lugar != None and not Lugar.objects.filter(pk = lugar).first():
                return HttpResponse(f'No existe un lugar con el id {lugar}', status=404)
            lugar = Lugar.objects.filter(pk = lugar).first()
            if evento != None and not Evento.objects.filter(pk = evento).first():
                return HttpResponse(f'No existe un evento con el id {evento}', status=404)
            evento = Evento.objects.filter(pk = evento).first()
            plan.grupo = grupo
            plan.lugar = lugar
            plan.evento = evento
            plan.save()
            planjson = serializers.serialize('json', [plan])
            return HttpResponse(planjson, 'application/json')
        return HttpResponse('Parametros invalidos', status=400)

    if request.method == 'DELETE':
        plan.delete()
        return HttpResponse(f'Plan {id} eliminado correctamente', status=204)
    
    planjson = serializers.serialize('json', [plan])
    return HttpResponse(planjson, 'application/json')

#GET Clientes de un plan
def clientes_plan(request, id):
    plan = Plan.objects.filter(pk = id).first()
    if not plan:
        return HttpResponse('No existe un plan con ese id', status=404)

    clientes = plan.cliente_set.all()
    clientesjson = serializers.serialize('json', clientes)
    return HttpResponse(clientesjson, 'application/json')

#CRUD del modelo 'Cliente'
@csrf_exempt
def clientes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('username', '') and data.get('nombre', '') and data.get('password', '') and data.get('correo', '') and data.get('fechaNacimiento', '') and data.get('telefono', '') and data.get('imagen', '') and data.get('grupos', '') != None and data.get('planes', '') != None and data.get('amigos', '') != None and data.get('favoritos', '') != None and data.get('intereses', '') != None:
            #Del modelo 'Usuario'
            username = data.get('username', '')
            nombre = data.get('nombre', '')
            password = data.get('password', '')
            correo = data.get('correo', '')
            fechaNacimiento = todate(data.get('fechaNacimiento', ''))
            #Del modelo 'Cliente'
            telefono = data.get('telefono', '')
            imagen = data.get('imagen', '')
            grupos = data.get('grupos', '')
            planes = data.get('planes', '')
            amigos = data.get('amigos', '')
            favoritos = data.get('favoritos', '')
            intereses = data.get('intereses', '')
            if grupos != []:
                for i in grupos:
                    if not Grupo.objects.filter(pk = i).first():
                        return HttpResponse(f'No existe un grupo con el id {i}', status=404)
            if planes != []:
                for i in planes:
                    if not Plan.objects.filter(pk = i).first():
                        return HttpResponse(f'No existe un plan con el id {i}', status=404)
            if amigos != []:
                for i in amigos:
                    if not Cliente.objects.filter(pk = i).first():
                        return HttpResponse(f'No existe un cliente con el id {i}', status=404)
                    elif i == id:
                        return HttpResponse('No puedes asignarte a ti mismo como amigo', status=400)
            if favoritos != []:
                for i in favoritos:
                    if not Lugar.objects.filter(pk = i).first():
                        return HttpResponse(f'No existe un lugar con el id {i}', status=404)
            if intereses != []:
                for i in intereses:
                    if not Interes.objects.filter(pk = i).first():
                        return HttpResponse(f'No existe un interes con el id {i}', status=404)
            if Cliente.objects.filter(username = username).first() != None or Cliente.objects.filter(correo = correo).first() != None:
                return HttpResponse('Ya existe un usuario con ese username o correo', status=400)
            cliente = Cliente.objects.create(username = username, nombre = nombre, password = password, correo = correo, fechaNacimiento = fechaNacimiento, telefono = telefono, imagen = imagen)
            cliente.grupos.set(grupos)
            cliente.planes.set(planes)
            cliente.amigos.set(amigos)
            cliente.favoritos.set(favoritos)
            cliente.intereses.set(intereses)
            cliente.save()
            clientejson = serializers.serialize('json', [cliente])
            return HttpResponse(clientejson, 'application/json')
        return HttpResponse(f'Parametros invalidos', status=400)

    clientes = Cliente.objects.all()
    clientesjson = serializers.serialize('json', clientes)
    return HttpResponse(clientesjson, 'application/json')

@csrf_exempt
def clienteId(request, id):

    cliente = Cliente.objects.filter(pk = id).first()

    if not cliente:
        return HttpResponse(f'No existe un cliente con el id {id}', status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('username', '') and data.get('nombre', '') and data.get('password', '') and data.get('correo', '') and data.get('fechaNacimiento', '') and data.get('telefono', '') and data.get('imagen', '') and data.get('grupos', '') != None and data.get('planes', '') != None and data.get('amigos', '') != None and data.get('favoritos', '') != None and data.get('intereses', '') != None:
            #Del modelo 'Usuario'
            cliente.username = data.get('username', '')
            cliente.nombre = data.get('nombre', '')
            cliente.password = data.get('password', '')
            cliente.correo = data.get('correo', '')
            cliente.fechaNacimiento = todate(data.get('fechaNacimiento', ''))
            #Del modelo 'Cliente'
            cliente.telefono = data.get('telefono', '')
            cliente.imagen = data.get('imagen', '')
            grupos = data.get('grupos', '')
            planes = data.get('planes', '')
            amigos = data.get('amigos', '')
            favoritos = data.get('favoritos', '')
            intereses = data.get('intereses', '')
            if grupos != []:
                for i in grupos:
                    if not Grupo.objects.filter(pk = i).first():
                        return HttpResponse(f'No existe un grupo con el id {i}', status=404)
            if planes != []:
                for i in planes:
                    if not Plan.objects.filter(pk = i).first():
                        return HttpResponse(f'No existe un plan con el id {i}', status=404)
            if amigos != []:
                for i in amigos:
                    if not Cliente.objects.filter(pk = i).first():
                        return HttpResponse(f'No existe un cliente con el id {i}', status=404)
                    elif i == id:
                        return HttpResponse('No puedes asignarte a ti mismo como amigo', status=400)
            if favoritos != []:
                for i in favoritos:
                    if not Lugar.objects.filter(pk = i).first():
                        return HttpResponse(f'No existe un lugar con el id {i}', status=404)
            if intereses != []:
                for i in intereses:
                    if not Interes.objects.filter(pk = i).first():
                        return HttpResponse(f'No existe un interes con el id {i}', status=404)
            if cliente.username != data.get('username', ''):
                if Cliente.objects.filter(username = data.get('username', '')).first():
                    return HttpResponse('Ya existe un usuario con ese username', status=400)
            if cliente.correo != data.get('correo', ''):
                if Cliente.objects.filter(correo = data.get('correo', '')).first() != None:
                    return HttpResponse('Ya existe un usuario con ese correo', status=400)
            cliente.grupos.set(grupos)
            cliente.planes.set(planes)
            cliente.amigos.set(amigos)
            cliente.favoritos.set(favoritos)
            cliente.intereses.set(intereses)
            cliente.save()
            clientejson = serializers.serialize('json', [cliente])
            return HttpResponse(clientejson, 'application/json')
        return HttpResponse(f'Parametros invalidos', status=400)

    if request.method == 'DELETE':
        cliente.delete()
        return HttpResponse(f'Cliente {id} eliminado correctamente', status=204)
    
    clientejson = serializers.serialize('json', [cliente])
    return HttpResponse(clientejson, 'application/json')

#GET grupos de un cliente
def grupos_cliente(request, id):
    cliente = Cliente.objects.filter(pk = id).first()
    if not cliente:
        return HttpResponse('No existe un cliente con ese id', status=404)
    
    grupos = cliente.grupos.all()
    gruposjson = serializers.serialize('json', grupos)
    return HttpResponse(gruposjson, 'application/json')

#GET planes de un cliente
def planes_cliente(request, id):
    cliente = Cliente.objects.filter(pk = id).first()
    if not cliente:
        return HttpResponse('No existe un cliente con ese id', status=404)

    planes = cliente.planes.all()
    planesjson = serializers.serialize('json', planes)
    return HttpResponse(planesjson, 'application/json')

#GET amigos de un cliente
def amigos_cliente(request, id):
    cliente = Cliente.objects.filter(pk = id).first()
    if not cliente:
        return HttpResponse('No existe un cliente con ese id', status=404)

    amigos = cliente.amigos.all()
    amigosjson = serializers.serialize('json', amigos)
    return HttpResponse(amigosjson, 'application/json')

#GET Calendarios de un cliente
def calendarios_cliente(request, id):
    if not Cliente.objects.filter(pk = id).first():
        return HttpResponse('No existe un cliente con ese id', status=404)
    
    calendarios = Calendario.objects.filter(cliente = id)
    calendariosjson = serializers.serialize('json', calendarios)
    return HttpResponse(calendariosjson, 'application/json')

#GET Lugares favoritos de un cliente
def lugares_cliente(request, id):
    cliente = Cliente.objects.filter(pk = id).first()
    if not cliente:
        return HttpResponse('No existe un cliente con ese id', status=404)
    
    lugares = cliente.favoritos.all()
    lugaresjson = serializers.serialize('json', lugares)
    return HttpResponse(lugaresjson, 'application/json')

#GET Intereses de un cliente
def intereses_cliente(request, id):
    cliente = Cliente.objects.filter(pk = id).first()
    if not cliente:
        return HttpResponse('No existe un cliente con ese id', status=404)
    
    intereses = cliente.intereses.all()
    interesesjson = serializers.serialize('json', intereses)
    return HttpResponse(interesesjson, 'application/json')

#GET Posts de un cliente
def posts_cliente(request, id):
    cliente = Cliente.objects.filter(pk = id).first()
    if not cliente:
        return HttpResponse('No existe un cliente con ese id', status=404)
    
    posts = Post.objects.filter(cliente = id)
    postsjson = serializers.serialize('json', posts)
    return HttpResponse(postsjson, 'application/json')


#CRUD del modelo 'Calendario'
@csrf_exempt
def calendario(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('nombre', '') and (data.get('cliente', '') or data.get('cliente', '') == None):
            nombre = data.get('nombre', '')
            cliente = data.get('cliente', '')
            if cliente != None and not Cliente.objects.filter(pk = cliente).first():
                return HttpResponse(f'No existe un cliente con el id {cliente}', status=404)
            cliente = Cliente.objects.filter(pk = cliente).first()
            calendario = Calendario.objects.create(nombre = nombre, cliente = cliente)
            calendario.save()
            calendariojson = serializers.serialize('json', [calendario])
            return HttpResponse(calendariojson, 'application/json')
        return HttpResponse('Parametros invalidos', status=400)

    calendarios = Calendario.objects.all()
    calendariosjson = serializers.serialize('json', calendarios)
    return HttpResponse(calendariosjson, 'application/json')

@csrf_exempt
def calendarioId(request, id):

    calendario = Calendario.objects.filter(pk = id).first()

    if not calendario:
        return HttpResponse(f'No existe un calendario con el id {id}', status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('nombre', '') and (data.get('cliente', '') or data.get('cliente', '') == None):
            calendario.nombre = data.get('nombre', '')
            cliente = data.get('cliente', '')
            if cliente != None and not Cliente.objects.filter(pk = cliente).first():
                return HttpResponse(f'No existe un cliente con el id {cliente}', status=404)
            cliente = Cliente.objects.filter(pk = cliente).first()
            calendario.cliente = cliente
            calendario.save()
            calendariojson = serializers.serialize('json', [calendario])
            return HttpResponse(calendariojson, 'application/json')
        return HttpResponse('Parametros invalidos', status=400)

    if request.method == 'DELETE':
        calendario.delete()
        return HttpResponse(f'Calendario {id} eliminado correctamente', status=204)

    calendariojson = serializers.serialize('json', [calendario])
    return HttpResponse(calendariojson, 'application/json')

#CRUD del modelo 'Lugar'
@csrf_exempt
def lugares(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('nombre', '') and data.get('precio', '') and data.get('direccion', '') and data.get('tipo', '') and data.get('horaApertura', '') and data.get('horaCierre', '') and data.get('calificacion', '') and data.get('imagen', '') and data.get('latitud', '') and data.get('longitud', ''):
            nombre = data.get('nombre', '')
            precio = data.get('precio', '')
            direccion = data.get('direccion', '')
            tipo = data.get('tipo', '')
            horaApertura = tohora(data.get('horaApertura', ''))
            horaCierre = tohora(data.get('horaCierre', ''))
            calificacion = data.get('calificacion', '')
            imagen = data.get('imagen', '')
            latitud = data.get('latitud', '')
            longitud = data.get('longitud', '')
            lugar = Lugar.objects.create(nombre = nombre, precio = precio, direccion = direccion, 
                                        tipo = tipo, horaApertura = horaApertura, horaCierre = horaCierre,
                                        calificacion = calificacion, imagen = imagen, latitud = latitud,
                                        longitud = longitud)
            lugar.save()
            lugarjson = serializers.serialize('json', [lugar])
            return HttpResponse(lugarjson, 'application/json')
        return HttpResponse('Parametros invalidos', status=400)

    lugares = Lugar.objects.all()
    lugaresjson = serializers.serialize('json', lugares)
    return HttpResponse(lugaresjson, 'application/json')

@csrf_exempt
def lugarId(request, id):

    lugar = Lugar.objects.filter(pk = id).first()

    if not lugar:
        return HttpResponse(f'No existe un lugar con el id {id}', status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('nombre', '') and data.get('precio', '') and data.get('direccion', '') and data.get('tipo', '') and data.get('horaApertura', '') and data.get('horaCierre', '') and data.get('calificacion', '') and data.get('imagen', '') and data.get('latitud', '') and data.get('longitud', ''):
            lugar.nombre = data.get('nombre', '')
            lugar.precio = data.get('precio', '')
            lugar.direccion = data.get('direccion', '')
            lugar.tipo = data.get('tipo', '')
            lugar.horaApertura = tohora(data.get('horaApertura', ''))
            lugar.horaCierre = tohora(data.get('horaCierre', ''))
            lugar.calificacion = data.get('calificacion', '')
            lugar.imagen = data.get('imagen', '')
            lugar.latitud = data.get('latitud', '')
            lugar.longitud = data.get('longitud', '')
            lugar.save()
            lugarjson = serializers.serialize('json', [lugar])
            return HttpResponse(lugarjson, 'application/json')
        return HttpResponse('Parametros invalidos', status=400)
    
    if request.method == 'DELETE':
        lugar.delete()
        return HttpResponse(f'Lugar {id} eliminado correctamente', status=204)
    
    lugarjson = serializers.serialize('json', [lugar])
    return HttpResponse(lugarjson, 'application/json')

#GET Clientes que tienen como favorito un lugar
def clientes_lugar(request, id):
    lugar = Lugar.objects.filter(pk = id).first()
    if not lugar:
        return HttpResponse('No existe un lugar con ese id', status=404)
    
    clientes = lugar.cliente_set.all()
    clientesjson = serializers.serialize('json', clientes)
    return HttpResponse(clientesjson, 'application/json')

#GET Eventos de un lugar
def eventos_lugar(request, id):
    if not Lugar.objects.filter(pk = id).first():
        return HttpResponse('No existe un lugar con ese id', status=404)

    eventos = Evento.objects.filter(lugar = id)
    eventosjson = serializers.serialize('json', eventos)
    return HttpResponse(eventosjson, 'application/json')

#GET Planes de un lugar
def planes_lugar(request, id):
    if not Lugar.objects.filter(pk = id).first():
        return HttpResponse('No existe un lugar con ese id', status=404)

    planes = Plan.objects.filter(lugar = id)
    planesjson = serializers.serialize('json', planes)
    return HttpResponse(planesjson, 'application/json')

#GET Posts de un lugar
def posts_lugar(request, id):
    if not Lugar.objects.filter(pk = id).first():
        return HttpResponse('No existe un lugar con ese id', status=404)

    posts = Post.objects.filter(lugar = id)
    postsjson = serializers.serialize('json', posts)
    return HttpResponse(postsjson, 'application/json')

#CRUD del modelo 'Evento'
@csrf_exempt
def eventos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('nombre', '') and data.get('fecha', '') and data.get('duracion', '') and (data.get('lugar', '') or data.get('lugar', '') == None):
            nombre = data.get('nombre', '')
            fecha = todatetime(data.get('fecha', ''))
            duracion = data.get('duracion', '')
            lugar = data.get('lugar', '')
            if lugar != None and Lugar.objects.filter(pk = lugar).first() == None:
                return HttpResponse(f'No existe un lugar con el id {lugar}', status=404)
            lugar = Lugar.objects.filter(pk = lugar).first()
            evento = Evento.objects.create(nombre = nombre, fecha = fecha, duracion = duracion, lugar = lugar)
            evento.save()
            eventojson = serializers.serialize('json', [evento])
            return HttpResponse(eventojson, 'application/json')
        return HttpResponse('Parametros invalidos', status=400)

    eventos = Evento.objects.all()
    eventojson = serializers.serialize('json', eventos)
    return HttpResponse(eventojson, 'application/json')

@csrf_exempt
def eventoId(request, id):

    evento = Evento.objects.filter(pk = id).first()

    if not evento:
        return HttpResponse(f'No existe un evento con el id {id}', status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('nombre', '') and data.get('fecha', '') and data.get('duracion', '') and (data.get('lugar', '') or data.get('lugar', '') == None):
            evento.nombre = data.get('nombre', '')
            evento.fecha = todatetime(data.get('fecha', ''))
            evento.duracion = data.get('duracion', '')
            lugar = data.get('lugar', '')
            if lugar != None and Lugar.objects.filter(pk = lugar).first() == None:
                return HttpResponse(f'No existe un lugar con el id {lugar}', status=404)
            evento.lugar = Lugar.objects.filter(pk = lugar).first()
            evento.save()
            eventojson = serializers.serialize('json', [evento])
            return HttpResponse(eventojson, 'application/json')
        return HttpResponse('Parametros invalidos', status=400)

    if request.method == 'DELETE':
        evento.delete()
        return HttpResponse(f'Evento {id} eliminado correctamente', status=204)
    
    eventojson = serializers.serialize('json', [evento])
    return HttpResponse(eventojson, 'application/json')

#GET Planes asociados a un evento
def planes_evento(request, id):
    if not Evento.objects.filter(pk = id).first():
        return HttpResponse('No existe un evento con ese id', status=404)

    planes = Plan.objects.filter(evento = id)
    planesjson = serializers.serialize('json', planes)
    return HttpResponse(planesjson, 'application/json')

#CRUD del modelo 'Interes'
@csrf_exempt
def intereses(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('tipo', ''):
            tipo = data.get('tipo', '')
            interes = Interes.objects.create(tipo = tipo)
            interes.save()
            interesjson = serializers.serialize('json', [interes])
            return HttpResponse(interesjson, 'application/json')
        return HttpResponse('Parametros invalidos', status=400)

    intereses = Interes.objects.all()
    interesesjson = serializers.serialize('json', intereses)
    return HttpResponse(interesesjson, 'application/json')

@csrf_exempt
def interesId(request, id):

    interes = Interes.objects.filter(pk = id).first()

    if not interes:
        return HttpResponse(f'No existe un interes con el id {id}', status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('tipo', ''):
            interes.tipo = data.get('tipo', '')
            interes.save()
            interesjson = serializers.serialize('json', [interes])
            return HttpResponse(interesjson, 'application/json')
        return HttpResponse('Parametros invalidos', status=400)
    
    if request.method == 'DELETE': 
        interes.delete()
        return HttpResponse(f'Interes {id} eliminado correctamente', status=204)
    
    interesjson = serializers.serialize('json', [interes])
    return HttpResponse(interesjson, 'application/json')

#GET Clientes interesados en un tipo de plan
def clientes_interes(request, id):
    interes = Interes.objects.filter(pk = id).first()
    if not interes:
        return HttpResponse('No existe un interes con ese id', status=404)

    clientes = interes.cliente_set.all()
    clientesjson = serializers.serialize('json', clientes)
    return HttpResponse(clientesjson, 'application/json')

#CRUD del modelo 'RepresentanteLocal'
@csrf_exempt
def representantes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('username', '') and data.get('nombre', '') and data.get('password', '') and data.get('correo', '') and data.get('fechaNacimiento', '') and data.get('numeroDocumento', '') and data.get('tipoDocumento', '') and data.get('cargo', '') and data.get('fechaExpDocumento', '') and data.get('imagen', '') and (data.get('lugar', '') or data.get('lugar', '') == None) and (data.get('partner', '') or data.get('partner', '') == None):
            #Del modelo 'Usuario'
            username = data.get('username', '')
            nombre = data.get('nombre', '')
            password = data.get('password', '')
            correo = data.get('correo', '')
            fechaNacimiento = todate(data.get('fechaNacimiento', ''))
            #Del modelo 'RepresentanteLocal'
            numeroDocumento = data.get('numeroDocumento', '')
            tipoDocumento = data.get('tipoDocumento', '')
            cargo = data.get('cargo', '')
            fechaExpDocumento = todate(data.get('fechaExpDocumento', ''))
            imagen = data.get('imagen', '')
            lugar = data.get('lugar', '')
            partner = data.get('partner', '')
            if lugar != None and not Lugar.objects.filter(pk = lugar).first():
                return HttpResponse(f'No existe un lugar con el id {lugar}', status=404)
            lugar = Lugar.objects.filter(pk = lugar).first()
            if partner != None and not Partner.objects.filter(pk = partner).first():
                return HttpResponse(f'No existe un partner con el id {partner}', status=404)
            partner = Partner.objects.filter(pk = partner).first()
            representante = RepresentanteLocal.objects.create(username = username, nombre = nombre, password = password, correo = correo, 
                                                            fechaNacimiento = fechaNacimiento, numeroDocumento = numeroDocumento, tipoDocumento = tipoDocumento, 
                                                            cargo = cargo, fechaExpDocumento = fechaExpDocumento, imagen = imagen, lugar = lugar, partner = partner)
            representante.save()
            representantejson = serializers.serialize('json', [representante])
            return HttpResponse(representantejson, 'application/json')
        return HttpResponse(f'Parametros invalidos', status=400)

    representantes = RepresentanteLocal.objects.all()
    representantesjson = serializers.serialize('json', representantes)
    return HttpResponse(representantesjson, 'application/json')

@csrf_exempt
def representanteId(request, id):

    representante = RepresentanteLocal.objects.filter(pk = id).first()

    if not representante:
        return HttpResponse(f'No existe un representante con el id {id}', status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('username', '') and data.get('nombre', '') and data.get('password', '') and data.get('correo', '') and data.get('fechaNacimiento', '') and data.get('numeroDocumento', '') and data.get('tipoDocumento', '') and data.get('cargo', '') and data.get('fechaExpDocumento', '') and data.get('imagen', '') and (data.get('lugar', '') or data.get('lugar', '') == None) and (data.get('partner', '') or data.get('partner', '') == None):
            #Del modelo 'Usuario'
            representante.username = data.get('username', '')
            representante.nombre = data.get('nombre', '')
            representante.password = data.get('password', '')
            representante.correo = data.get('correo', '')
            representante.fechaNacimiento = todate(data.get('fechaNacimiento', ''))
            #Del modelo 'RepresentanteLocal'
            representante.numeroDocumento = data.get('numeroDocumento', '')
            representante.tipoDocumento = data.get('tipoDocumento', '')
            representante.cargo = data.get('cargo', '')
            representante.fechaExpDocumento = todate(data.get('fechaExpDocumento', ''))
            representante.imagen = data.get('imagen', '')
            lugar = data.get('lugar', '')
            partner = data.get('partner', '')
            if lugar != None and Lugar.objects.filter(pk = lugar).first() == None:
                return HttpResponse(f'No existe un lugar con el id {lugar}', status=404)
            representante.lugar = Lugar.objects.filter(pk = lugar).first()
            if partner != None and not Partner.objects.filter(pk = partner).first():
                return HttpResponse(f'No existe un partner con el id {partner}', status=404)
            representante.partner = Partner.objects.filter(pk = partner).first()
            representante.save()
            representantejson = serializers.serialize('json', [representante])
            return HttpResponse(representantejson, 'application/json')
        return HttpResponse(f'Parametros invalidos', status=400)
    
    if request.method == 'DELETE':
        representante.delete()
        return HttpResponse(f'Representante {id} eliminado correctamente', status=204)
    
    representantejson = serializers.serialize('json', [representante])
    return HttpResponse(representantejson, 'application/json')

#GET Posts de un representante
def posts_representante(request, id):
    representante = RepresentanteLocal.objects.filter(pk = id).first()
    if not representante:
        return HttpResponse('No existe un representante con ese id', status=404)

    posts = Post.objects.filter(representante = id)
    postsjson = serializers.serialize('json', posts)
    return HttpResponse(postsjson, 'application/json')

#CRUD del modelo 'Partner'
@csrf_exempt
def partners(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('tipoSuscripcion', '') and data.get('fechaFin', '') and data.get('fechaInicio', '') and data.get('duracion', ''):
            tipoSuscripcion = data.get('tipoSuscripcion', '')
            fechaFin = todate(data.get('fechaFin', ''))
            fechaInicio = todate(data.get('fechaInicio', ''))
            duracion = data.get('duracion', '')
            partner = Partner.objects.create(tipoSuscripcion = tipoSuscripcion, fechaFin = fechaFin, fechaInicio = fechaInicio, duracion = duracion)
            partner.save()
            partnerjson = serializers.serialize('json', [partner])
            return HttpResponse(partnerjson, 'application/json')
        return HttpResponse(f'Parametros invalidos', status=400)

    partners = Partner.objects.all()
    partnersjson = serializers.serialize('json', partners)
    return HttpResponse(partnersjson, 'application/json')

@csrf_exempt
def partnerId(request, id):

    partner = Partner.objects.filter(pk = id).first()

    if not partner:
        return HttpResponse(f'No existe un partner con el id {id}', status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('tipoSuscripcion', '') and data.get('fechaFin', '') and data.get('fechaInicio', '') and data.get('duracion', ''):
            partner.tipoSuscripcion = data.get('tipoSuscripcion', '')
            partner.fechaFin = todate(data.get('fechaFin', ''))
            partner.fechaInicio = todate(data.get('fechaInicio', ''))
            partner.duracion = data.get('duracion', '')
            partner.save()
            partnerjson = serializers.serialize('json', [partner])
            return HttpResponse(partnerjson, 'application/json')
        return HttpResponse(f'Parametros invalidos', status=400)
    
    if request.method == 'DELETE':
        partner.delete()
        return HttpResponse(f'Partner {id} eliminado correctamente', status=204)
    
    partnerjson = serializers.serialize('json', [partner])
    return HttpResponse(partnerjson, 'application/json')

#CRUD del modelo 'Post'
@csrf_exempt
def posts(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('titulo', '') and data.get('descripcion', '') and data.get('calificacion', '') and (data.get('anuncio', '') != None) and (data.get('cliente', '') or data.get('cliente', '') == None) and (data.get('lugar', '') or data.get('lugar', '') == None) and (data.get('representante', '') or data.get('representante', '') == None):
            titulo = data.get('titulo', '')
            descripcion = data.get('descripcion', '')
            calificacion = data.get('calificacion', '')
            anuncio = data.get('anuncio', '')
            cliente = data.get('cliente', '')
            lugar = data.get('lugar', '')
            representante = data.get('representante', '')
            if cliente != None and not Cliente.objects.filter(pk=cliente).first():
                return HttpResponse(f'No existe un cliente con el id {cliente}', status=404)
            cliente = Cliente.objects.filter(pk = cliente).first()
            if lugar != None and not Lugar.objects.filter(pk = lugar).first():
                return HttpResponse(f'No existe un lugar con el id {lugar}', status=404)
            lugar = Lugar.objects.filter(pk = lugar).first()
            if representante != None and not RepresentanteLocal.objects.filter(pk = representante).first():
                return HttpResponse(f'No existe un representante con el id {representante}', status=404)
            representante = RepresentanteLocal.objects.filter(pk = representante).first()
            post = Post.objects.create(titulo = titulo, descripcion = descripcion, calificacion = calificacion, anuncio = anuncio, cliente = cliente, lugar = lugar, representante = representante)
            post.save()
            postjson = serializers.serialize('json', [post])
            return HttpResponse(postjson, 'application/json')
        return HttpResponse(f'Parametros invalidos.', status=400)

    posts = Post.objects.all()
    postsjson = serializers.serialize('json', posts)
    return HttpResponse(postsjson, 'application/json')

@csrf_exempt
def postId(request, id):

    post = Post.objects.filter(pk = id).first()

    if not post:
        return HttpResponse(f'No existe un post con el id {id}', status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('titulo', '') and data.get('descripcion', '') and data.get('calificacion', '') and (data.get('anuncio', '') != None) and (data.get('cliente', '') or data.get('cliente', '') == None) and (data.get('lugar', '') or data.get('lugar', '') == None) and (data.get('representante', '') or data.get('representante', '') == None):
            post.titulo = data.get('titulo', '')
            post.descripcion = data.get('descripcion', '')
            post.calificacion = data.get('calificacion', '')
            post.anuncio = data.get('anuncio', '')
            cliente = data.get('cliente', '')
            lugar = data.get('lugar', '')
            representante = data.get('representante', '')
            if cliente != None and not Cliente.objects.filter(pk=cliente).first():
                return HttpResponse(f'No existe un cliente con el id {cliente}', status=404)
            post.cliente = Cliente.objects.filter(pk = cliente).first()
            if lugar != None and not Lugar.objects.filter(pk = lugar).first():
                return HttpResponse(f'No existe un lugar con el id {lugar}', status=404)
            post.lugar = Lugar.objects.filter(pk = lugar).first()
            if representante != None and not RepresentanteLocal.objects.filter(pk = representante).first():
                return HttpResponse(f'No existe un representante con el id {representante}', status=404)
            post.representante = RepresentanteLocal.objects.filter(pk = representante).first()
            post.save()
            postjson = serializers.serialize('json', [post])
            return HttpResponse(postjson, 'application/json')
        return HttpResponse(f'Parametros invalidos', status=400)
    
    if request.method == 'DELETE':
        post.delete()
        return HttpResponse(f'Post {id} eliminado correctamente', status=204)

    postjson = serializers.serialize('json', [post])
    return HttpResponse(postjson, 'application/json')