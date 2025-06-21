from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Cliente, Carrito
from django.contrib.auth.decorators import login_required

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})


def agregar_al_carrito(request, producto_id):
    cliente = Cliente.objects.first()
    carrito, _ = Carrito.objects.get_or_create(cliente=cliente)
    producto = get_object_or_404(Producto, pk=producto_id)
    if producto.hay_stock(1):
        carrito.agregar_producto(producto, 1)
    return redirect('resumen')

@login_required
def resumen(request):
 
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        return redirect('registro')  


    carrito, creado = Carrito.objects.get_or_create(cliente=cliente)

   
    carrito.aplicar_descuento(10)

    resumen = carrito.mostrar_resumen()
    total = carrito.calcular_total()
    subtotal = sum(item.subtotal() for item in resumen)

    return render(request, 'resumen.html', {
        'resumen': resumen,
        'total': total,
        'subtotal': subtotal
    })