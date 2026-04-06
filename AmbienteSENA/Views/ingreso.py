from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from ..Models import Ingreso, Instructor, Ambiente

def RegistrarIngreso(request):
    if request.method == "POST":
            try:
                instructor_id = request.POST.get("instructor")
                ambiente_id = request.POST.get("ambiente")
                observacion = request.POST.get("observacion")

                instructor = get_object_or_404(Instructor, id=instructor_id)
                ambiente = get_object_or_404(Ambiente, id=ambiente_id)

                ingreso = Ingreso.objects.create(
                    instructor=instructor,
                    ambiente=ambiente,
                    observacion=observacion
                )
                ingreso.save()
                messages.success(request, "Ingreso registrado correctamente")
            except Exception as e:
                messages.error(request, f'Ocurrio un error en el sistema { e }')
            return redirect("/Ingreso/ListarIngresos")

    instructores = Instructor.objects.all()
    ambientes = Ambiente.objects.all()
    return render(request, "Ingreso/RegistrarIngreso.html", {"instructores": instructores, "ambientes": ambientes})

def ListarIngresos(request):
    ingresos = Ingreso.objects.filter(fechaHoraSalida__isnull=True).select_related("instructor", "ambiente").all()
    return render(request, "Ingreso/ListarIngresos.html", {"ingresos": ingresos})


def ActualizarIngreso(request):
    
    if request.method == "POST":
        ingreso = get_object_or_404(Ingreso, id= request.POST.get('id'))
        ingreso.fechaHoraSalida = timezone.now()
        ingreso.save()
        messages.success(request, "Ingreso eliminado correctamente")
        return redirect("/Ingreso/ListarIngresos")

    instructores = Instructor.objects.all()
    ambientes = Ambiente.objects.all()
    return render(request, "Ingreso/ActualizarIngreso.html", {"ingreso": ingreso, "instructores": instructores, "ambientes": ambientes})
