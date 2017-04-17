from __future__ import print_function, unicode_literals
import boto3
import botocore
from boto3.dynamodb.conditions import Attr
from django.conf import settings

class Tester:
    def __init__(self):
        self.empresas = settings.TABLA_EMPRESAS

    test_item1 = {
        'nombre_empresa': 'La empresa 1',
        'slug_empresa': 'empresaaaaaa',
        'id_usuario': 0,
        'proyectos': [],
    }                 

    test_item2 = {
        'nombre_empresa': 'La empresa 2',
        'slug_empresa': 'empresaaaa',
        'id_usuario': 0,
        'proyectos': [],
    }                 

    proyecto1 = {
        'nombre': 'pagina web',
        'descripcion': 'una página web',
        'valor_estimado': 289000,
        'diseños': []
        }

    def test_add(self):
        try:
            return self.empresas.put_item(
                Item=Tester.test_item1,
                ConditionExpression=Attr('id_usuario').not_exists()&Attr('slug_empresa').not_exists()
            )
        except botocore.exceptions.ClientError as e:
            print(e)
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise

    def add_proyecto(self):
        return self.empresas.update_item(
            Key={'slug_empresa':'empresaaaa'},
            UpdateExpression='SET proyectos = list_append(proyectos, :proyecto)',
            ExpressionAttributeValues={':proyecto': [Tester.proyecto1]}
            )
