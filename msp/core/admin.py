import uuid
from django.contrib import admin
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import path, reverse

from .models import Product, MarkingCode, ProductBatch
from .utils import generate_pdf_with_codes


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    list_filter = ('owner',)
    search_fields = ('name', 'owner__username')
    exclude = ('owner',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not change or not obj.owner_id:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


class ProductBatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'quantity', 'created_at')
    change_list_template = "admin/batch_change_list.html"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        for _ in range(obj.quantity):
            code = str(uuid.uuid4())
            MarkingCode.objects.create(product=obj.product, batch=obj, code=code)
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:batch_id>/generate-pdf/', self.admin_site.admin_view(self.generate_pdf), name='generate-pdf'),
        ]
        return custom_urls + urls

    def generate_pdf(self, request, batch_id):
        batch = get_object_or_404(ProductBatch, id=batch_id)
        codes = [mc.code for mc in batch.codes.all()]
        pdf_buffer = generate_pdf_with_codes(codes)
        return FileResponse(pdf_buffer, as_attachment=True, filename=f'{batch.name}_labels.pdf')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['batches'] = ProductBatch.objects.all()
        return super().changelist_view(request, extra_context=extra_context)



admin.site.register(Product, ProductAdmin)
admin.site.register(ProductBatch, ProductBatchAdmin)
