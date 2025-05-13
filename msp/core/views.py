from django.shortcuts import render, get_object_or_404, redirect
from .models import MarkingCode, MovementLog, Location
from django import forms

class MovementLogForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), label='Местоположение')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Описание')

def track_product_view(request, code):
    marking_code = get_object_or_404(MarkingCode, code=code)
    movements = marking_code.movements.all()

    if request.method == 'POST':
        form = MovementLogForm(request.POST)
        if form.is_valid():
            MovementLog.objects.create(
                code=marking_code,
                location=form.cleaned_data['location'].name,
                moved_by=request.user if request.user.is_authenticated else None
            )
            return redirect('track-product', code=code)
    else:
        form = MovementLogForm()

    return render(request, 'track_product.html', {
        'marking_code': marking_code,
        'movements': movements,
        'form': form,
    })
