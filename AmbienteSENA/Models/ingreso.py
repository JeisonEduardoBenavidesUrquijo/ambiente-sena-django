from django.db import models
from .ambiente import Ambiente
from .instructor import Instructor

class Ingreso(models.Model):
    fechaHoraEntrada = models.DateTimeField(auto_now_add=True)
    fechaHoraSalida = models.DateTimeField(null=True, blank=True)
    observacion = models.TextField(blank=True, null=True)
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'ingreso'
