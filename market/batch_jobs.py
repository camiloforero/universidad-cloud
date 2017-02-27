from .models import Diseño

from PIL import Image as Img
from io import BytesIO
from django.core.files import File
from django.core.mail import send_mail


def batch_converter():
    diseños = Diseño.objects.filter(estado=Diseño.EN_PROCESO)
    for diseño in diseños:
        image = Img.open(BytesIO(diseño.archivo_original.read()))
        image.thumbnail((800, 600), Img.ANTIALIAS)
        output = BytesIO()
        image.save(output, format='PNG', quality=75)
        output.seek(0)
        diseño.archivo_procesado = File(output, diseño.archivo_original.name + " - Procesado.png")
        diseño.estado = Diseño.DISPONIBLE
        send_mail(
            "Tu diseño ha sido procesado, %s" % diseño.nombres,
            "Tu diseño ya ha sido procesado y está en nuestra página",
            "ce.forero2551@uniandes.edu.co",
            [diseño.email]
        )
        diseño.save()
        print("Se ha procesado el diseño %s satisfactoriamente" % diseño)
