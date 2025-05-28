# apps/modulo7/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from apps.core.decorators import group_required
from apps.modulo5.models import Medicamento
from .models import (
    Provider, ProviderMedication,
    CanastaItem, Pedido, PedidoItem
)
from .forms import (
    ProviderForm, ProviderUploadForm,
    PedidoTipoForm
)
import csv, io


from django.db.models import Sum



from django.http import HttpResponse
from reportlab.pdfgen import canvas










class Mod7LoginView(LoginView):
    template_name = 'modulo7/login.html'
    redirect_authenticated_user = False
    def get_success_url(self):
        return reverse_lazy('mod7_dashboard')

@group_required('Módulo7', login_url='mod7_login')
def dashboard_mod7(request):
    return render(request, 'modulo7/dashboard.html')

@group_required('Módulo7', login_url='mod7_login')
def notifications(request):
    meds = Medicamento.objects.all()
    solicitados = set(CanastaItem.objects.values_list('medicamento_id', flat=True))
    return render(request, 'modulo7/notifications.html', {
        'meds': meds,
        'solicitados': solicitados,
    })

@group_required('Módulo7', login_url='mod7_login')
def add_to_canasta(request, pk):
    med = get_object_or_404(Medicamento, pk=pk)
    CanastaItem.objects.get_or_create(medicamento=med)
    return redirect('mod7_notifications')

@group_required('Módulo7', login_url='mod7_login')
def remove_from_canasta(request, pk):
    # Elimina el medicamento de la canasta
    if request.method == 'POST':
        CanastaItem.objects.filter(medicamento_id=pk).delete()
    return redirect('mod7_basket')

@group_required('Módulo7', login_url='mod7_login')
def basket(request):
    items = CanastaItem.objects.select_related('medicamento')
    return render(request, 'modulo7/basket.html', {'items': items})



# @group_required('Módulo7', login_url='mod7_login')
# def basket_confirm(request):
#     if request.method == 'POST':
#         form = PedidoTipoForm(request.POST)
#         if form.is_valid():
#             tipo = form.cleaned_data['tipo']
#             pedido = Pedido.objects.create(tipo=tipo)
#             for ci in CanastaItem.objects.all():
#                 PedidoItem.objects.create(pedido=pedido, medicamento=ci.medicamento)
#             CanastaItem.objects.all().delete()
#             return redirect('mod7_basket')
#     else:
#         form = PedidoTipoForm()
#     return render(request, 'modulo7/basket_confirm.html', {'form': form})

# apps/modulo7/views.py



@group_required('Módulo7', login_url='mod7_login')
def basket_confirm(request):
    meds = [ci.medicamento for ci in CanastaItem.objects.all()]
    if request.method == 'POST':
        form = PedidoTipoForm(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data['tipo']
            # 1) Evaluar proveedores candidatos
            candidates = []
            for prov in Provider.objects.all():
                total = 0
                ok = True
                for m in meds:
                    pm = ProviderMedication.objects.filter(
                        provider=prov, compuesto=m.compuesto
                    ).first()
                    if not pm:
                        ok = False
                        break
                    total += pm.precio
                if ok:
                    candidates.append((prov, total))

            if not candidates:
                form.add_error(None, "Ningún proveedor tiene todos los compuestos.")
                return render(request, 'modulo7/basket_confirm.html', {'form': form})

            # 2) Filtrar según tipo
            if tipo == 'normal':
                # precio mínimo, luego rating_promedio
                min_price = min(total for _, total in candidates)
                best = [prov for prov, total in candidates if total == min_price]
            else:  # urgente
                # menor tiempo de entrega, luego rating_promedio
                min_days = min(p.tiempo_entrega for p, _ in candidates)
                best = [prov for prov, _ in candidates if prov.tiempo_entrega == min_days]

            # 3) Desempate por rating_promedio
            proveedor_elegido = max(best, key=lambda p: p.rating_promedio)
            total_elegido = dict(candidates)[proveedor_elegido]

            # 4) Crear Pedido con proveedor y total
            pedido = Pedido.objects.create(
                tipo=tipo,
                provider=proveedor_elegido,
                total_price=total_elegido
            )
            # 5) Crear los items y vaciar canasta
            for m in meds:
                PedidoItem.objects.create(pedido=pedido, medicamento=m)
            CanastaItem.objects.all().delete()

            # 6) Redirigir a la vista de PDF
            return redirect('mod7_pedido_pdf', pedido.id)
    else:
        form = PedidoTipoForm()
    return render(request, 'modulo7/basket_confirm.html', {'form': form})









@group_required('Módulo7', login_url='mod7_login')
def providers_catalog(request):
    providers = Provider.objects.all()
    return render(request, 'modulo7/providers.html', {'providers': providers})

@group_required('Módulo7', login_url='mod7_login')
def provider_create(request):
    if request.method == 'POST':
        form = ProviderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mod7_providers')
    else:
        form = ProviderForm()
    return render(request, 'modulo7/provider_form.html', {'form': form, 'action': 'Crear'})

@group_required('Módulo7', login_url='mod7_login')
def provider_edit(request, pk):
    prov = get_object_or_404(Provider, pk=pk)
    if request.method == 'POST':
        form = ProviderForm(request.POST, instance=prov)
        if form.is_valid():
            form.save()
            return redirect('mod7_providers')
    else:
        form = ProviderForm(instance=prov)
    return render(request, 'modulo7/provider_form.html', {'form': form, 'action': 'Editar'})

@group_required('Módulo7', login_url='mod7_login')
def provider_delete(request, pk):
    prov = get_object_or_404(Provider, pk=pk)
    if request.method == 'POST':
        prov.delete()
        return redirect('mod7_providers')
    return render(request, 'modulo7/provider_confirm_delete.html', {'prov': prov})

@group_required('Módulo7', login_url='mod7_login')
def provider_upload(request, pk):
    prov = get_object_or_404(Provider, pk=pk)
    if request.method == 'POST':
        form = ProviderUploadForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data['file'].read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(data))
            for row in reader:
                ProviderMedication.objects.update_or_create(
                    provider=prov,
                    compuesto=row['compuesto'],
                    defaults={'precio': row['precio']}
                )
            return redirect('mod7_providers')
    else:
        form = ProviderUploadForm()
    return render(request, 'modulo7/provider_upload.html', {'form': form, 'provider': prov})

@group_required('Módulo7', login_url='mod7_login')
def mod7_logout(request):
    logout(request)
    return redirect('mod7_login')





@group_required('Módulo7', login_url='mod7_login')
def pedido_pdf(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    y = 800

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, f"Pedido #{pedido.id} – {pedido.get_tipo_display()}")
    y -= 30

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Proveedor: {pedido.provider.nombre_legal}")
    y -= 20
    p.drawString(50, y, f"Total: ${pedido.total_price:.2f}")
    y -= 30

    p.drawString(50, y, "Detalle de compuestos:")
    y -= 20
    for item in pedido.items.all():
        p.drawString(70, y, f"- {item.medicamento.compuesto}")
        y -= 15
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
