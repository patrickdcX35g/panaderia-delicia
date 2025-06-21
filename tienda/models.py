from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from accounts.models import Cliente

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)  

    def __str__(self):
        return f"{self.nombre} - S/{self.precio}"

    def hay_stock(self, cantidad):
        return self.stock >= cantidad

    def aplicar_descuento(self, porcentaje):
        return self.precio * (1 - porcentaje / 100)







class Carrito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='ItemCarrito')
    _descuento = models.FloatField(default=0) 

    def agregar_producto(self, producto, cantidad):
        item, creado = ItemCarrito.objects.get_or_create(
            carrito=self,
            producto=producto,
            defaults={'cantidad': cantidad}  
        )
        if not creado:
            item.cantidad += cantidad
            item.save()

    def calcular_total(self):
        subtotal = sum(item.subtotal() for item in self.itemcarrito_set.all())
        descuento_decimal = Decimal(self._descuento) / Decimal(100)  
        total = subtotal * (Decimal('1.0') - descuento_decimal)
        return round(total, 2)
    
    def aplicar_descuento(self, porcentaje):
        self._descuento = porcentaje
        self.save()

    def mostrar_resumen(self):
        return self.itemcarrito_set.all()

    def buscar_producto(self, nombre):
        return self.productos.filter(nombre__icontains=nombre)



class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def subtotal(self):
        return self.producto.precio * self.cantidad
