from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfileInfo(models.Model):

    # Aca lo que hacemos es agregar funcionalidad al USER por defecto
    # este tiene cosas como nombre,appelido,email password
    # NO LO HEREDA, despues de esto le agregamos mas cosa que queremos
    # nosotros como el portafolio, etc
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    portfolio_site = models.URLField(blank=True,)

    # profile_pics es una subcarpeta de la carpeta de MEDIA

    # PARA TRABAJAR CON IMAGENES NECESITAMOS LA LIBRERIA PILLOW
    # conda install pillow
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username  # username es un atributo por defecto
