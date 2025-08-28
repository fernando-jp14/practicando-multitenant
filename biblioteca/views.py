from django.views.generic import ListView
from .models import Libro

class LibroListView(ListView):
    model = Libro
    template_name = "libros/lista.html"

    def get_queryset(self):
        # Mostrar solo libros del tenant del usuario logueado
        return Libro.objects.filter(tenant=self.request.user.tenant)
    


# Create your views here.
