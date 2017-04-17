from __future__ import absolute_import, unicode_literals
from celery import shared_task
from PIL import ImageDraw, ImageFont, Image as Img
from io import BytesIO
from django.core.files import File
from django.core.files.storage import DefaultStorage
from django.core.mail import send_mail
from datetime import datetime


@shared_task
def convertir_diseño(id_diseño, email, file_name, nombres, apellidos):
    storage = DefaultStorage()
    image = Img.open(storage.open(file_name))
    image.thumbnail((800, 600), Img.ANTIALIAS)
    font = ImageFont.truetype("DejaVuSans.ttf", 18)
    width, height = image.size
    draw = ImageDraw.Draw(image)
    draw.text((30,height-30), "%s %s" % (nombres, apellidos), (255,255,255), font=font)
    draw.text((width/2,height-30), datetime.now().isoformat(), (255,255,255), font=font)
    output = BytesIO()
    image.save(output, format='PNG', quality=75)
    output.seek(0)
    diseño_procesado_nombre = storage.save(file_name + ' - Procesado.png', File(output))

    #send_mail(
    #    "Tu diseño ha sido procesado.", 
    #    "Tu diseño ya ha sido procesado y está en nuestra página",
    #    "ce.forero2551@uniandes.edu.co",
    #    [email],
    #    fail_silently = True,
    #)
