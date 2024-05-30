from django.db import models


class Example(models.Model):
    # Liste des champs de la table
    # Plusieurs types de champs sont existent
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        # Méthode appelée lorsqu'on veut afficher l'objet
        return self.name

    def deactivate(self):
        # Méthode personalisé, qui permet de désactiver l'example
        self.is_active = False
        self.save()
