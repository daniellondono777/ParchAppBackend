from django.db import models

class TipoPlan(models.TextChoices):
    RUMBITA = 'RU', 'Rumba'
    CINE = 'CI', 'Cine'
    BIBLIOTECA = 'BI', 'Biblioteca'
    COMIDA = 'CO', 'Comida'
    NATURAL = 'NA', 'Natural'

class TipoDocumento(models.TextChoices):
    CEDULACIUDADANIA = 'CC', 'Cedula_Ciudadania'
    CEDULAEXTRANJERIA = 'CE', 'Cedula_Extranjeria'
    TARJETAIDENTIDAD = 'TI', 'Tarjeta_Identidad'
    PASAPORTE = 'PP', 'Pasaporte'

class TipoSub(models.TextChoices):
    STANDARD = 'ST', 'Standard'
    PREMIUM = 'PR', 'Premium'

class Usuario(models.Model):
    username = models.CharField(max_length=20)
    nombre = models.TextField(max_length=50)
    password = models.CharField(max_length=20)
    correo = models.CharField(max_length=50)
    fechaNacimiento = models.DateField()

    class Meta:
        abstract = True

class Grupo(models.Model):
    nombre = models.TextField(max_length=50)
    imagen = models.URLField(blank=True, default="")
    balance = models.FloatField()

    def __str__(self):
        return f"Grupo {self.id}"

class Plan(models.Model):
    nombre = models.TextField(max_length=50, blank=True)
    descripcion = models.TextField(max_length=300, blank=True)
    presupuesto = models.FloatField()
    horaInicia = models.DateTimeField()
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    lugar = models.ForeignKey('Lugar', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    evento = models.ForeignKey('Evento', on_delete=models.SET_NULL, default=None, null=True, blank=True)

    def __str__(self):
        return f"Plan {self.id}"

class Cliente(Usuario):
    telefono = models.CharField(max_length=30)
    imagen = models.URLField(blank=True, default="")
    grupos = models.ManyToManyField(Grupo, default=None, null=True, blank=True)
    planes = models.ManyToManyField(Plan, default=None, null=True, blank=True)
    amigos = models.ManyToManyField('self', default=None, null=True, blank=True)
    favoritos = models.ManyToManyField('Lugar', default=None, null=True, blank=True)
    intereses = models.ManyToManyField('Interes', default=None, null=True, blank=True)

    def __str__(self):
        return f"Cliente {self.id}"

class Calendario(models.Model):
    nombre = models.TextField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f"Calendario {self.id}"

class Lugar(models.Model):
    nombre = models.TextField(max_length=100)
    precio = models.FloatField()
    direccion = models.TextField(max_length=100)
    tipo = models.CharField(max_length=2, choices=TipoPlan.choices, default=TipoPlan.RUMBITA)
    horaApertura = models.DateTimeField()
    horaCierre = models.DateTimeField()
    calificacion = models.FloatField()
    imagen = models.URLField(blank=True, default="")
    latitud = models.CharField(max_length=100, default=0)
    longitud = models.CharField(max_length=100, default=0)
    
    def __str__(self):
        return f"Lugar {self.id}"

class Evento(models.Model):
    nombre = models.TextField(max_length=50)
    fecha = models.DateTimeField()
    duracion = models.IntegerField()
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f"Evento {self.id}"

class Interes(models.Model):
    tipo = models.CharField(max_length=2, choices=TipoPlan.choices, default=TipoPlan.RUMBITA)
    
    def __str__(self):
        return f"Interes {self.id}"

class RepresentanteLocal(Usuario):
    numeroDocumento = models.CharField(max_length=15)
    tipoDocumento = models.CharField(max_length=2, choices=TipoDocumento.choices, default=TipoDocumento.CEDULACIUDADANIA)
    cargo = models.CharField(max_length=40)
    fechaExpDocumento = models.DateField()
    imagen = models.URLField(blank=True, default="")
    lugar = models.OneToOneField(Lugar, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    partner = models.ForeignKey('Partner', on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f"Representante {self.id}"

class Partner(models.Model):
    tipoSuscripcion = models.CharField(max_length=2, choices=TipoSub.choices, default=TipoSub.STANDARD)
    fechaFin = models.DateField()
    fechaInicio = models.DateField()
    duracion = models.CharField(max_length=40)
    
    def __str__(self):
        return f"Partner {self.id}"

class Post(models.Model):
    titulo = models.TextField(max_length=80)
    descripcion = models.TextField(max_length=500)
    calificacion = models.FloatField()
    anuncio = models.BooleanField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=None, null=True, blank=True)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, default=None, null=True, blank=True)
    representante = models.ForeignKey(RepresentanteLocal, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f"Post {self.id}"