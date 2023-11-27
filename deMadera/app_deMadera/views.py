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


from django.shortcuts import render, redirect
from .models import Desk, Leg, Boleta
from .forms import BoletaForm

def create_boleta(request):
    if request.method == 'POST':
        form = BoletaForm(request.POST)
        if form.is_valid():
            boleta = form.save(commit=False)
            selected_desk_id = request.session.get('selected_desk_id')
            selected_leg_id = request.session.get('selected_leg_id')

            try:
                selected_desk = Desk.objects.get(id=selected_desk_id) if selected_desk_id else None
                selected_leg = Leg.objects.get(id=selected_leg_id) if selected_leg_id else None
            except (Desk.DoesNotExist, Leg.DoesNotExist):
                selected_desk = None
                selected_leg = None

            boleta.cubierta = selected_desk
            boleta.bases = selected_leg
            boleta.total = selected_desk.price + selected_leg.price * 2
            boleta.save()

            del request.session['selected_desk_id']
            del request.session['selected_leg_id']

            return redirect('boleta_pdf.html')
    else:
        form = BoletaForm()
        # No es necesario manejar selected_desk_id y selected_leg_id aquí si no se van a utilizar para pre-poblar el formulario

    return render(request, 'boleta_pdf.html', {'form': form})



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
