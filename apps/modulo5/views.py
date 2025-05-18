# apps/modulo5/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from apps.core.decorators import group_required
from .models import Medicamento
from .forms import MedicamentoForm, ReduceStockForm

@group_required('Módulo5', login_url='mod5_login')
def lista_medicamentos(request):
    meds = Medicamento.objects.all()
    return render(request, 'modulo5/list.html', {'meds': meds})

@group_required('Módulo5', login_url='mod5_login')
def add_medicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            obj, created = Medicamento.objects.get_or_create(
                compuesto=cd['compuesto'],
                numero_serie=cd['numero_serie'],
                defaults={
                    'categoria': cd['categoria'],
                    'cantidad': cd['cantidad'],
                }
            )
            if not created:
                obj.cantidad += cd['cantidad']
                obj.save()
            return redirect('mod5_list')
    else:
        form = MedicamentoForm()
    return render(request, 'modulo5/add.html', {'form': form})

@group_required('Módulo5', login_url='mod5_login')
def reduce_stock(request):
    if request.method == 'POST':
        form = ReduceStockForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                obj = Medicamento.objects.get(
                    compuesto=cd['compuesto'],
                    numero_serie=cd['numero_serie']
                )
            except Medicamento.DoesNotExist:
                form.add_error(None, 'El compuesto y número de serie no coinciden.')
                return render(request, 'modulo5/reduce.html', {'form': form})
            obj.cantidad -= cd['cantidad']
            if obj.cantidad <= 0:
                obj.delete()
            else:
                obj.save()
            return redirect('mod5_list')
    else:
        form = ReduceStockForm()
    return render(request, 'modulo5/reduce.html', {'form': form})

@group_required('Módulo5', login_url='mod5_login')
def delete_medicamento(request, pk):
    obj = Medicamento.objects.filter(pk=pk).first()
    if request.method == 'POST' and obj:
        obj.delete()
        return redirect('mod5_list')
    return render(request, 'modulo5/confirm_delete.html', {'obj': obj})


def mod5_logout_view(request):
    logout(request)
    return redirect('mod5_login')
