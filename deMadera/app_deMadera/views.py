import io
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Desk, Leg
from django.shortcuts import render
from .models import Desk, Leg
from .forms import BoletaForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Boleta
from .forms import BoletaForm
from django.contrib.auth import authenticate, login
from django.http import FileResponse
from reportlab.pdfgen import canvas


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
    if request.method == 'POST':
        form = BoletaForm(request.POST)
        if form.is_valid():
            boleta = form.save()
            # Generar el PDF aquí o redirigir a una vista que lo haga
            return render(request, 'boleta_pdf.html', {'boleta': boleta})
    else:
        form = BoletaForm()
    return render(request, 'creacion_boleta.html', {'form': form})

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



def login_view(request):
    data = {"fondologin":"fondologin.jpg"}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin:index')
        else:
            return render(request, 'login.html', {'error': 'Nombre de usuario o contraseña incorrectos'})
    else:
        return render(request, 'login.html',data)
    


def imprimirPDF(request):
    # Recoge los valores del formulario
    email = request.POST.get('email')
    name = request.POST.get('name')
    address = request.POST.get('address')

    # Crea un objeto de archivo en memoria
    buffer = io.BytesIO()

    # Crea el archivo PDF, utilizando el objeto como su "archivo"
    p = canvas.Canvas(buffer)

    # Dibuja cosas en el PDF. Aquí es donde se genera el PDF. 
    # Consulta la documentación de ReportLab para obtener la lista completa de funcionalidades.
    p.drawString(100, 100, "Correo Electronico: " + email)
    p.drawString(100, 120, "Nombre y apellido: " + name)
    p.drawString(100, 140, "Direccion: " + address)

    # Cierra el objeto PDF limpiamente y termina la página
    p.showPage()
    p.save()

    # Recupera el valor del objeto de tipo 'file'. Este será el contenido PDF.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='datos.pdf')

def some_view(request):
    # Crea un objeto de archivo en memoria
    buffer = io.BytesIO()

    # Crea el archivo PDF, utilizando el objeto como su "archivo"
    p = canvas.Canvas(buffer)

    # Dibuja cosas en el PDF. Aquí es donde se genera el PDF. 
    # Consulta la documentación de ReportLab para obtener la lista completa de funcionalidades.
    p.drawString(100, 100, "Hello world.")

    # Cierra el objeto PDF limpiamente y termina la página
    p.showPage()
    p.save()

    # Recupera el valor del objeto de tipo 'file'. Este será el contenido PDF.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
