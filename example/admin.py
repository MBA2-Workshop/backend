from django.contrib import admin
from example.models import Example


# Afffiche l'objet Example dans l'admin de Django
admin.site.register(Example)