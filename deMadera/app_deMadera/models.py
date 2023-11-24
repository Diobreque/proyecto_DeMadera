from django.db import models

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50)


class Articulos(models.Model):
    id_articulo = models.AutoField(primary_key=True)
    nombre_articulo = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    

class Desk(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='desk_tops/')  # Asegúrate de configurar MEDIA_URL y MEDIA_ROOT

    def __str__(self):
        return self.name

class Leg(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='desk_legs/')

    def __str__(self):
        return self.name

