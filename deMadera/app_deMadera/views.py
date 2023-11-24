from django.shortcuts import redirect, render
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

def cotselect(request):
    return render(request,"cotselect.html")

def create_desk(request):
    desks = Desk.objects.all()
    legs = Leg.objects.all()

    if request.method == 'POST':
        selected_desk_id = request.POST.get('selected_desk')
        selected_leg_id = request.POST.get('selected_leg')

        # Guardar las selecciones en la sesión
        request.session['selected_desk_id'] = selected_desk_id
        request.session['selected_leg_id'] = selected_leg_id

        # Redirigir a la vista de creación de boleta
        return redirect('create_boleta')

    context = {'desks': desks, 'legs': legs}
    return render(request, 'cotselect.html', context)

def index_desk(request):
    # Vista para la página principal que muestra las opciones de escritorios y patas.
    desks = Desk.objects.all()
    legs = Leg.objects.all()
    
    # Obtener el primer objeto Desk y Leg
    selected_desk = desks.first()
    selected_leg = legs.first()

    return render(request, 'coti.html', {'desks': desks, 'legs': legs, 'selected_desk': selected_desk, 'selected_leg': selected_leg})


def update_desk(request):
    # Vista que maneja la actualización del precio y la imagen del escritorio
    # cuando se seleccionan diferentes opciones de cubierta y patas.
    desk_id = request.GET.get('desk_id')
    leg_id = request.GET.get('leg_id')
    
    # Obtener las instancias de Desk y Leg basadas en los ID proporcionados
    desk = Desk.objects.get(id=desk_id)
    leg = Leg.objects.get(id=leg_id)

    # Calcular el precio total
    total_price = desk.price + leg.price

    # Aquí asumimos que simplemente devolvemos la URL de la imagen del escritorio
    # En una aplicación real, podrías necesitar combinar imágenes o realizar otra lógica.
    desk_image_url = desk.image.url

    response = {
        'deskImageUrl': desk_image_url,
        'totalPrice': total_price,
    }
    
    return JsonResponse(response)





def create_boleta(request):
    selected_desk_id = request.session.get('selected_desk_id')
    selected_leg_id = request.session.get('selected_leg_id')

    try:
        selected_desk = Desk.objects.get(id=selected_desk_id) if selected_desk_id else None
        selected_leg = Leg.objects.get(id=selected_leg_id) if selected_leg_id else None
    except (Desk.DoesNotExist, Leg.DoesNotExist):
        # Manejar el error si los objetos no existen
        selected_desk = None
        selected_leg = None

    if request.method == 'POST':
        # Aquí manejas la lógica de creación de la boleta
        pass
    else:
        form = BoletaForm()

    context = {
        'form': form,
        'selected_desk': selected_desk,
        'selected_leg': selected_leg
    }
    return render(request, 'nombre_de_tu_app/creacion_boleta.html', context)


def generate_pdf(request, boleta_id):
    boleta = Boleta.objects.get(id=boleta_id)
    # Crea una respuesta HTTP de tipo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="boleta.pdf"'

    # Crea el PDF
    p = canvas.Canvas(response)
    p.drawString(100, 100, f"Boleta #{boleta.id} - Total: ${boleta.total}")
    # ... Añade más elementos al PDF según sea necesario ...

    p.showPage()
    p.save()
    return response
