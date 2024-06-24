from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from decimal import Decimal , ROUND_HALF_UP
from .serializers import *
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
import requests



def Internacionales(request):
    api_key = '88a85ce0b56c40379806d62bec15fb63'
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'language': 'en',
        'apiKey': api_key
    }

    response = requests.get(url, params=params)
    news_data = response.json()

    if news_data['status'] == 'ok':
        articles = news_data['articles']
    else:
        articles = []

    paginator = Paginator(articles, 3)  # 2 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/internacionales.html', {'page_obj': page_obj})




logger = logging.getLogger(__name__)

# Create your views here.



class PeriodistaViewSet(viewsets.ModelViewSet):
    queryset = Periodista.objects.all()
    serializer_class = PeriodistaSerializer
    renderer_classes = [JSONRenderer]

class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer
    renderer_classes = [JSONRenderer]





def index(request):
    noticias =  Noticia.objects.filter(estado=True)
    paginator = Paginator(noticias,6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Categoria.objects.prefetch_related('noticia_set').all()
    return render(request, 'core/index.html', {'noticias': noticias,'categories': categories, 'page_obj': page_obj})

def base(request):
    return render(request,'core/base.html')

def bloqueo(request):
    return render(request,'core/admon/bloqueo.html')

def ver_api(request):
    return render(request,'core/ver_api.html')

@login_required
def historial(request):

    usuario = request.user
    compras = Voucher.objects.filter(usuario=usuario).order_by('-fecha_voucher') 
    
    context = {
        'compras': compras
    }

    return render(request,'core/historial.html', context)

@staff_member_required
def lista_admin(request):
    noticias_usuario = Noticia.objects.filter()
    imagenes_usuario = Imagen.objects.filter()
    return render(request,'core/admon/lista_admin.html', {'noticias_usuario': noticias_usuario, 'imagenes_usuario': imagenes_usuario})


@login_required
def miperfil(request):
    try:
        periodista = Periodista.objects.get(usuario=request.user)
    except Periodista.DoesNotExist:
        periodista = None  # Maneja el caso donde el usuario no sea un periodista
    
    noticias_usuario = Noticia.objects.filter(periodista=periodista) if periodista else []
    imagenes_usuario = Imagen.objects.filter(noticia__periodista=periodista) if periodista else []
    noticias_contador = Noticia.objects.filter(periodista=periodista).count() if periodista else 0
    
    context = {
        'noticias_usuario': noticias_usuario,
        'imagenes_usuario': imagenes_usuario,
        'noticias_contador': noticias_contador,
        'periodista' : periodista,
    }
    
    return render(request, 'core/miperfil.html', context,)

def periodistas(request):
    todos_periodistas = Periodista.objects.all()
    noticias =  Noticia.objects.filter(estado=True)
    return render(request, 'core/periodistas.html', {'lista' : noticias, 'periodistas' : todos_periodistas})

@login_required
@staff_member_required
def admin2(request):
    return render(request,'core/admon/admin.html')
    
@login_required
@staff_member_required
def noticia_admin(request):
    noticias_usuario =  Noticia.objects.filter(estado=False)
    imagenes_usuario = Imagen.objects.all()
    return render(request, 'core/admon/noticias.html', {'noticias_usuario': noticias_usuario, 'imagenes_usuario': imagenes_usuario})

def categori(request):
    categories = Categoria.objects.prefetch_related('noticia_set').all()
    return render(request, 'core/categori.html', {'categories': categories})

def contacto(request):
    return render(request,'core/contacto.html')

@login_required
def suscripcion(request):
    return render(request,'core/suscripcion.html')


def latest_news(request, ):
    noticias = Noticia.objects.all().order_by('-fecha_noticia')[:4]  
    return render(request,'core/latest_news.html', {'noticias': noticias})

def noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    return render(request, 'core/noticias/index.html', {'noticia': noticia})

def handle_form_submission(request):
    if request.method == 'POST':
        return HttpResponse('Formulario enviado exitosamente')
    else:
        return HttpResponse('Método no permitido')

def login(request,user):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Inicio de sesión correcto')
                return redirect('index')  # Redirigir a la página de inicio u otra página
            else:
                messages.error(request, 'Correo electrónico o contraseña incorrectos')
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = RegistroUsuarioForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            group, created = Group.objects.get_or_create(name='Usuario')
            user.groups.add(group)
            login(request, user)
            messages.success(request, 'Registro exitoso')
            return redirect('index')  

    else:
        user_form = RegistroUsuarioForm()

    return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def noticia_add(request):
    if request.method == 'POST':
        noticia_form = NoticiaForm(request.POST)
        imagen_form = ImagenForm(request.POST, request.FILES)
        if noticia_form.is_valid() and imagen_form.is_valid():
            noticia = noticia_form.save(commit=False)
            noticia.periodista = request.user.periodista  # Asignar el periodista actual
            noticia.save()
            imagen = Imagen(noticia=noticia, image=request.FILES['image'])
            imagen.save()
            messages.success(request, 'La noticia creada correctamente.')
            return redirect('index')
    else:
        noticia_form = NoticiaForm()
        imagen_form = ImagenForm()
    return render(request, 'core/noticias/crud/add.html', {'noticia_form': noticia_form, 'imagen_form': imagen_form})


@login_required
def editar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    
    if request.method == 'POST':
        form_noticia = NoticiaForm(request.POST,request.FILES, instance=noticia)
        imagen_instance = noticia.images.first() if noticia.images.exists() else None
        form_imagen = ImagenForm(request.POST, request.FILES, instance=imagen_instance)
        
        if form_noticia.is_valid() and form_imagen.is_valid():
            form_noticia.save()
            form_imagen.save()
            messages.success(request, 'La noticia ha sido modificada correctamente.')
            return redirect('index')
    else:
        form_noticia = NoticiaForm(instance=noticia)
        imagen_instance = noticia.images.first() if noticia.images.exists() else None
        form_imagen = ImagenForm(instance=imagen_instance)
    
    return render(request, 'core/noticias/crud/update.html', {'form_noticia': form_noticia, 'form_imagen': form_imagen})

@login_required
def noticia_delete(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    if request.method == 'POST':
        noticia.delete()
        messages.success(request, 'La noticia ha sido eliminada correctamente.')
        return redirect('index')
    return render(request, 'core/noticias/crud/delete.html', {'noticia': noticia})

@login_required
@staff_member_required
def crear_periodista(request):
    if request.method == 'POST':
        form = CrearPeriodistaForm(request.POST)
        if form.is_valid():
            nuevo_periodista = form.save()
            nuevo_periodista.usuario.groups.remove(Group.objects.get(name='Usuario'))
            nuevo_periodista.usuario.groups.add(Group.objects.get(name='Periodista'))
            messages.success(request, 'El periodista ha sido creado correctamente.')
            return redirect('index')  
    else:
        form = CrearPeriodistaForm()
    return render(request, 'core/Periodista/crud/add.html', {'form': form})


@staff_member_required
@csrf_exempt
def aprobar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    noticia.estado = True
    noticia.save()
    return redirect('noticia_admin')
    
@staff_member_required
@csrf_exempt
def rechazar_noticia(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        noticia_id = data.get('noticia_id')
        motivo_rechazo = data.get('motivo_rechazo')
        
        noticia = get_object_or_404(Noticia, id=noticia_id)
        noticia.estado = False
        noticia.razon = motivo_rechazo
        noticia.save()
        
        # Enviar una respuesta JSON indicando que el proceso se completó correctamente
        return JsonResponse({'status': 'success'})
        
    
    # Si no es una solicitud POST, devolver un estado de error
    return JsonResponse({'status': 'error'}, status=400)






@csrf_exempt
@login_required
def actualizar_plan(request):
    if request.method == 'POST':
        print("Solicitud POST recibida")
        user_id = request.user.id
        nuevo_plan_id = request.POST.get('plan_id')
        order_id = request.POST.get('orderID')
        details = json.loads(request.POST.get('details'))
        
        print(f"User ID: {user_id}, Plan ID: {nuevo_plan_id}, Order ID: {order_id}")
        
        if not nuevo_plan_id:
            return JsonResponse({'status': 'error', 'message': 'Plan ID is missing'}, status=400)
        
        periodista = get_object_or_404(Periodista, usuario_id=user_id)
        nuevo_plan = get_object_or_404(Plan, id=nuevo_plan_id)
        periodista.plan = nuevo_plan
        periodista.save()

        # Simulación de monto para el voucher (debes ajustar según tu lógica)
        monto = Decimal('20.00')  # Aquí debes obtener el monto real desde el detalle de la transacción

        # Crear o actualizar el voucher
        voucher_obj, created = Voucher.objects.update_or_create(
            usuario_id=user_id,
            defaults={'monto': monto}
        )

        # Obtener la fecha y el monto del voucher
        fecha_voucher = voucher_obj.fecha_voucher.strftime('%d-%m-%Y')
        monto_voucher = voucher_obj.monto

        return JsonResponse({'status': 'success', 'voucher_url': request.build_absolute_uri('/voucher/'), 'fecha_voucher': fecha_voucher, 'monto_voucher': float(monto_voucher)})
    
    return JsonResponse({'status': 'error'}, status=400)



class Mindicador:

    def __init__(self, indicador):
        self.indicador = indicador

    def InfoApi(self):
    # En este caso hacemos la solicitud para el caso de consulta de un indicador en un año determinado
        url = f'https://mindicador.cl/api/{self.indicador}'
        response = requests.get(url)
        data = json.loads(response.text.encode("utf-8"))
        # Para que el json se vea ordenado, retornar pretty_json
        pretty_json = json.dumps(data, indent=2)
        return data


def convert_currency(amount, from_currency, to_currency):
    if from_currency == 'USD' and to_currency == 'CLP':
        url = 'https://mindicador.cl/api'
        response = requests.get(url)
        data = response.json()
        if 'dolar' in data:
            conversion_rate = Decimal(data['dolar']['valor'])
            converted_amount = amount * conversion_rate
            # Redondear a un decimal
            converted_amount = converted_amount.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
            return converted_amount
        else:
            raise ValueError("Error en la conversión de divisas")
    else:
        raise ValueError("Solo se admite conversión de USD a CLP")

def generate_voucher(usuario, details, fecha_voucher, monto_voucher):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Usuario: {usuario.username}")
    p.drawString(100, 720, f"Monto: {details['transactions'][0]['amount']['total']} {details['transactions'][0]['amount']['currency']}")
    p.drawString(100, 705, f"Estado: {details['state']}")
    p.drawString(100, 690, f"Fecha de la transacción: {fecha_voucher}")  # Incluir la fecha del voucher
    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Boleta.pdf'
    return response

@login_required
def voucher(request):
    user = request.user
    voucher = get_object_or_404(Voucher, usuario=user)

    # Simulación de detalles del pago para generación del voucher
    details = {
        'transactions': [{'amount': {'total': '20.00', 'currency': 'USD'}}],  # Reemplaza con el monto correcto
        'state': 'completed',  # Ajusta según sea necesario
    }

    # Obtener la fecha y el monto del voucher
    fecha_voucher = voucher.fecha_voucher.strftime('%d-%m-%Y')
    monto_voucher = Decimal(details['transactions'][0]['amount']['total'])

    # Convertir monto de USD a CLP
    try:
        monto_voucher_clp = convert_currency(monto_voucher, 'USD', 'CLP')
        details['transactions'][0]['amount']['total'] = str(monto_voucher_clp)
        details['transactions'][0]['amount']['currency'] = 'CLP'
    except ValueError as e:
        messages.error(request, f"Error en la conversión de divisas: {e}")
        return redirect('some-error-page')  # Redirige a una página de error si ocurre un problema

    return generate_voucher(user, details, fecha_voucher, monto_voucher_clp)