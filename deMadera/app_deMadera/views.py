from django.shortcuts import render
from django.http import JsonResponse
from .models import Desk, Leg

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
    context = {'desks': desks, 'legs': legs}
    return render(request, 'creacion_desk.html', context)

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
