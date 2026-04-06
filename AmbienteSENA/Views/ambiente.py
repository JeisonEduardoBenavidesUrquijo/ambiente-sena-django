from django.contrib import messages
from django.db import connection
from django.shortcuts import render, redirect

from AmbienteSENA.Models.ambiente import Ambiente

def RegistarAmbiente(request):
    if request.method == 'POST':
        ###Validacion de datos del frontend###
        if request.POST.get('nombre') and request.POST.get('tipo') and request.POST.get('observacion'):
            ###DEFINICION VARIABLES###
            nombre = request.POST.get('nombre')
            tipo = request.POST.get('tipo')
            observacion = request.POST.get('observacion')
            ###CONEXION A BASE DE DATOS###
            try:
                ambiente = Ambiente()
                ambiente.NombreAmbiente = nombre
                ambiente.TipoAmbiente = tipo
                ambiente.Observaciones = observacion
                ambiente.save()
                messages.success(request, "Ambiente de Formacion registrado correctamente.")
            except Exception as e:
                messages.error(request, "ERROR: No se pudo registrar Ambiente. Por favor, intentelo mas tarde.")
            return render(request, 'Ambientes/ListarAmbientes.html')
    else:
        return render(request,'Ambientes/RegistrarAmbiente.html')
    
###CONSULTAR AMBIENTES DE FORMACION###
def ListarAmbientes(request):
    try:
        listadoAmbientes = Ambiente.objects.all()
    except Exception as e:
        messages.error(request, "ERROR: No se pudo cargar el listado de Ambientes. Por favor, intentelo mas tarde.")
        return render(request, 'Ambientes/ListarAmbientes.html')  
    return render(request, 'Ambientes/ListarAmbientes.html',
                      {'ambientes': listadoAmbientes})
    
##ELIMINAR UN AMBIENTE DE FORMACION EN EL SISTEMA##
def EliminarAmbiente(request):
    if request.method == 'POST':
        try:
            ambiente = Ambiente.objects.filter(id = request.POST.get('id'))
            ambiente.delete()
            messages.success(request, "Ambiente de Formacion eliminado correctamente")
        except Exception as e:
            messages.error(request, f"ERROR: {{ e }}")
        return redirect('/Ambientes/ListarAmbientes')
    
###EDITAR UN AMBIENTE DE FORMACION EN EL SISTEMA###
def ActualizarAmbiente(request, id_ambiente):
    if request.method == 'POST':
        try:
            ambiente = Ambiente.objects.get(id = id_ambiente)
            ambiente.NombreAmbiente = request.POST.get('nombre')
            ambiente.TipoAmbiente = request.POST.get('tipo')
            ambiente.Observaciones = request.POST.get('observacion')
            ambiente.save()
            messages.success(request, "Ambiente actualizado correctamente")
        except Exception as e:
            messages.error(request, f"ERROR: No se pudo actualizar el Ambiente. Por favor, intentalo mas tarde")
        return redirect('/Ambientes/ListarAmbientes')
    else:
        try:
            ambiente = Ambiente.objects.filter(id = id_ambiente)
            return render(request,'Ambientes/ActualizarAmbiente.html',{'ambiente': ambiente})
        except Exception as e:
            messages.error(request,"Error en el sistema")
            return redirect('/Ambientes/ListarAmbientes')
        