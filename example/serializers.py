from rest_framework import serializers
from example.models import Example


class ExampleSerializer(serializers.ModelSerializer):
    # Le serializer permet de convertir les données de la base de données en JSON
    class Meta:
        # Modèle à utiliser
        model = Example
        # Liste de champs
        fields = '__all__'
