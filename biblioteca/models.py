from django.db import models
from django.contrib.auth.models import AbstractUser

class Tenant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=100, unique=True)  # ej: empresa1.com
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)

class Author(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)  # separación por cliente
    nombre_autor = models.CharField(max_length=100)
    apellido_autor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre_autor} {self.apellido_autor}"


class Genero(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    fecha_publicacion = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
