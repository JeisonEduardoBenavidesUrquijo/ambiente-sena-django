from django.db import DatabaseError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.serializers import serialize
from django.http import HttpResponse
from ..Models.instructor import Instructor
from ..Models.elemento import Elemento
from ..Models.cuentadante import Cuentadante

def RegistrarCuentadante(request):
    if request.method == 'POST':
        instructor_id = request.POST.get('instructor')
        elementos_id = request.POST.getlist('elementos[]')
        observacion = request.POST.get('observacion')
        
        try:
            ###VERIFICAR SI EXISTE EL INSTRUCTOR###
            instructor = get_object_or_404(Instructor, id = instructor_id)
            
            ###VERIFICAR SI EL USUARIO SELECCIONO AL MENOS UN ELEMENTO###
            if not elementos_id:
                messages.error(request, 'Debe Seleccionar al Menos Un Elemento')
                return redirect('/Cuentadante/RegistrarCuentadante')
            ###Recorremos los elementos###
            for elemento_id in elementos_id:
                ###VERIFICAR SI EXISTE EL ELEMENTO_ID###
                elemento = get_object_or_404(Elemento, id = elemento_id)
                ###EVITAR DUPLICADOS###
                if Cuentadante.objects.filter(instructor = instructor, elemento = elemento).exists():
                    messages.warning(request, f"El elemento: '{elemento.Nombre}' Ya esta asginado al instructor: '{instructor.NombreCompleto}'")
                    continue
                ###CREAR LOS OBJETOS CUENTADANTE###
                cuentadante = Cuentadante(
                    instructor = instructor,
                    elemento = elemento,
                    observacion = observacion
                )
                ###GUARDAR LAS DATOS EN LA BASE DA DATOS###
                cuentadante.save()
            messages.success(request, 'Asignacion de elementos Realizada correctamente')
            return redirect('/Cuentadante/ListarCuentadante')
        except Exception as e:
            messages.error(request,f'Ocurrio un error { e }')
            return redirect('/Cuentadante/RegistrarCuentadante')
        
    else:
        listadoInstructores = Instructor.objects.all().order_by('NombreCompleto')
        listadoElementos = Elemento.objects.all().order_by('Nombre')
        return render(request,"Cuentadante/RegistrarCuentadante.html", 
        {'instructores':listadoInstructores, 'elementos':listadoElementos})
        
###LISTAR LOS CUENTADANTES###
def ListarCuentadantes(request):
    listadoElementos = Elemento.objects.all().order_by('Nombre')
    listadoInstructores = Instructor.objects.all().order_by('NombreCompleto')
    listadoCuentadantes = Cuentadante.objects.select_related('instructor', 'elemento').all().order_by('instructor__NombreCompleto','elemento__Nombre')
    return render(request, 'Cuentadante/ListarCuentadante.html', {'cuentadantes': listadoCuentadantes, 'elementos': listadoElementos, 'instructores': listadoInstructores})

###ELIMINAR CUENTADANTE###
def EliminarCuentadante(request):
    if request.method == 'POST' and request.POST.get('id'):
        try:
            cuentadante = Cuentadante.objects.get(id = request.POST.get('id'))
            cuentadante.delete()
            messages.success(request, "Cuentadante Eliminado Correctamente")
            
        except DatabaseError as e:
            messages.error(request, f"Ocurrio un error en el sistema { e }")
    return redirect('/Cuentadante/ListarCuentadantes')

def APIConsultarCuentadante(request, id_cuentadante):
    unCuentadante = Cuentadante.objects.filter(id = id_cuentadante)
    cuentadante_json = serialize('json', unCuentadante)
    return HttpResponse(cuentadante_json, content_type='application/json')

def ActualizarCuentadante(request):
    if request.method == 'POST':
        if request.POST.get('instructor') and request.POST.get('elementos') and request.POST.get('observacion'):
            try:
                cuentadante = Cuentadante.objects.get(id = request.POST.get('id_cuentadante'))
                cuentadante.observacion = request.POST.get('observacion')
                cuentadante.elemento_id = request.POST.get('elementos')
                cuentadante.instructor_id = request.POST.get('instructor')
                cuentadante.save()
                messages.success(request, 'Cuentadante actualizado correctamente')
            except Exception as e:
                messages.error(request, f'Ocurrio un error en el sistema { e }')
        else:
            messages.warning(request, 'Debes deligenciar todos los campos')
        return redirect('/Cuentadante/ListarCuentadantes')
    else:
        return redirect('/Cuentadante/ListarCuentadantes')