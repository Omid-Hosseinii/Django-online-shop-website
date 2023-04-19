from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm,CustomChangeForm
from .models import CustomUser,Customer
#----------------------------------------------------------------

### this class show forms in admin panel
class CustomUserAdmin(UserAdmin):
    
    form=CustomChangeForm
    add_form=UserCreationForm
    
    list_display=('mobile_number','email','name','family','gender','is_active','is_admin')
    list_filter=('is_active','is_admin','family')
    
    ### add form fields
    fieldsets=(
        (None,{'fields':('mobile_number','password')}),
        ('personal info',{'fields':('email','name','family','gender','active_code')}),
        ('permissions',{'fields':('is_active','is_admin','user_permissions','groups','is_superuser')}),
    )

    ### change form fields
    add_fieldsets=(
        (None,{'fields':('mobile_number','email','name','family','gender','password1','password2')}),
    )

    search_fields=('mobile_number',)
    ordering=('mobile_number',)
    
    ### make right column for permissions and group 
    filter_horizontal=('user_permissions','groups')

### for register class     
admin.site.register(CustomUser,CustomUserAdmin)    


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['user','phone_number',]