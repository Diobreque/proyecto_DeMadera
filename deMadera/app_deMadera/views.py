from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Desk, Leg
from django.shortcuts import render
from .models import Desk, Leg
from .forms import BoletaForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Boleta
from .forms import BoletaForm


# Create your views here.
from django.shortcuts import render

# Create your views here.

def index(request):
    data = {"imgPrincipal":"fondoPrincipal.jpg"}
    return render(request, "index.html", data)

def cotizar(request):
    data = {"mesamadera":"mesamadera.jpg",
            "sillamadera":"sillamadera.jpg",
            "escritoriomadera":"escritoriomadera.jpg"}
    return render(request,"cotizar.html", data)



from django.shortcuts import render, redirect
from .models import Desk, Leg, Boleta
from .forms import BoletaForm

def create_desk(request):
    desks = Desk.objects.all()
    legs = Leg.objects.all()

    if request.method == 'POST':
        form = BoletaForm(request.POST)
        if form.is_valid():
            selected_desk_id = request.POST.get('selected_desk_id')
            selected_leg_id = request.POST.get('selected_leg_id')

            boleta = form.save(commit=False)
            boleta.cubierta = Desk.objects.get(id=selected_desk_id)
            boleta.bases = Leg.objects.get(id=selected_leg_id)

            # Calcula el precio total aquí si es necesario
            boleta.total = boleta.cubierta.price + boleta.bases.price * 2

            boleta.save()
            return redirect('ver_boleta', boleta_id=boleta.id)

    else:
        form = BoletaForm()

    context = {'desks': desks, 'legs': legs, 'form': form}
    return render(request, 'cotselect.html', context)


def ver_boleta(request, boleta_id):
    boleta = get_object_or_404(Boleta, id=boleta_id)
    return render(request, 'ver_boleta.html', {'boleta': boleta})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Desk, Leg, Boleta
from .forms import BoletaForm


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Desk, Leg, Boleta
from .forms import BoletaForm
import logging

logger = logging.getLogger(__name__)

def create_boleta(request):
    if request.method == 'POST':
        form = BoletaForm(request.POST)
        if form.is_valid():
            selected_desk_id = request.POST.get('selected_desk_id')
            selected_leg_id = request.POST.get('selected_leg_id')
            boleta = form.save(commit=False)
            # ... configuración adicional de 'boleta' si es necesario ...
            boleta.save()
            return redirect('ver_boleta', boleta_id=boleta.id)

            # Verificar si los IDs están presentes
            if not selected_desk_id or not selected_leg_id:
                messages.error(request, 'Faltan datos del escritorio o las bases.')
                return render(request, 'pagina_error.html', {'form': form})

            try:
                boleta = form.save(commit=False)
                boleta.cubierta = Desk.objects.get(id=selected_desk_id)
                boleta.bases = Leg.objects.get(id=selected_leg_id)
                boleta.total = request.POST.get('total_price')
                boleta.save()
                return redirect('ver_boleta', boleta_id=boleta.id)
            except (Desk.DoesNotExist, Leg.DoesNotExist, ValueError) as e:
                logger.error("Error al crear boleta: {}".format(e))
                messages.error(request, 'Hubo un error al procesar tu selección.')
                return render(request, 'pagina_error.html', {'form': form})
        else:
            messages.error(request, 'Información del formulario no válida.')
            return render(request, 'pagina_error.html', {'form': form})
    else:
    # El formulario no es válido
        print("Formulario no válido:", form.errors)
        logger.debug("Errores del formulario: %s", form.errors)
        messages.error(request, 'Información del formulario no válida.')
        return render(request, 'pagina_error.html', {'form': form})