from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.mainApp.urls',namespace='main')),
    path('accounts/',include('apps.accountsApp.urls',namespace='accounts')),
    path('product/',include('apps.productApp.urls',namespace='products')),
    path('order/',include('apps.orderApp.urls',namespace='orders')),
    path('discount/',include('apps.discountsApp.urls',namespace='discounts')),
    path('payments/',include('apps.paymentApp.urls',namespace='payments')),
    path('warehouse/',include('apps.warehouseApp.urls',namespace='warehouse')),
    path('search/',include('apps.searchApp.urls',namespace='search_app')),
    path('csw/',include('apps.comments_scoring_whislistApp.urls',namespace='csws')),
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('tinymce/', include('tinymce.urls')),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


admin.site.site_header='پنل مدیریت فروشگاه'
admin.site.index_title='به پنل مدیریت خوش آمدید'