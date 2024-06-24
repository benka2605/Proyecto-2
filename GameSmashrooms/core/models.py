from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Genero(models.Model):
    descripcion = models.CharField(max_length=20)
    def __str__(self):
        return self.descripcion

class Categoria(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Plan(models.Model):
    name= models.CharField(max_length=12)

    def __str__(self):
        return self.name

class Voucher(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)    
    fecha_voucher = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return f"Voucher de {self.usuario.username} ({self.fecha_voucher})"

class Periodista(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=70)
    apellido = models.CharField(max_length=70)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Noticia(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    periodista = models.ForeignKey(Periodista, on_delete=models.CASCADE)
    fecha_noticia= models.DateTimeField(auto_now_add=True)
    ubicacion = models.CharField(max_length=255)
    categoria= models.ForeignKey(Categoria, on_delete=models.CASCADE)
    estado = models.BooleanField(default=False)
    razon = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class Imagen(models.Model):
    noticia = models.ForeignKey(Noticia, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image')
    
    def __str__(self):
        return f"Imagen for {self.noticia.titulo}"

"""class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
"""