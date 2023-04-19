from django.shortcuts import render,redirect
from django.views import View
from .forms import (RegisterUserForm,VerifyRegisterForm,
                    LoginUserForm,ChangePasswordForm,RememberPasswordForm,UserPanelUpdateForm)

# LoginUserForm,ChangePasswordForm,RememberPasswordForm

import utils
from .models import CustomUser,Customer
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from apps.orderApp.models import Order
from apps.paymentApp.models import Payment
#-----------------------------------------------------------------------------------------------

class RegisterUserView(View):
    ### dispatch is a first method in the View class which run befor get or post method.
    def dispatch(self, request, *args, **kwargs):
        ### if user login but request login page redirect to main page
        if request.user.is_authenticated:
            return redirect('main:index')
        ### call dispath super is important!.
        return super().dispatch(request,*args, **kwargs) 
     
    template_name="accounts_app/register.html"
    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        return render(request,self.template_name,{'form':form})


    def post(self, request, *args, **kwargs):
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            active_code=utils.create_random_code(5)
            CustomUser.objects.create_user(
                mobile_number=data['mobile_number'],
                password=data['password1'],
                active_code=active_code,
            )
            utils.send_sms(data['mobile_number'],'کد فعال سازی شما {active_code} می باشد')
            request.session['user_session']={
                'mobile_number':data['mobile_number'],
                'active_code':active_code,
                'remember_password':False
            }
            messages.success(request,'اطلاعات شما ثبت شد','success')
            return redirect('accounts:verify')
        messages.error(request,'اطلاعات شما صحیح نمی باشد','danger')
        return render(request,self.template_name,{'form':form})
        
#-----------------------------------------------------------------------------------------------

class VerifyRegisterViews(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)  
      
    template_name = "accounts_app/verify.html"
    def get(self, request, *args, **kwargs):
        form = VerifyRegisterForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = VerifyRegisterForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session['user_session']
            if user_session['remember_password']==False:
                user_db=CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                user_db.is_active=True
                user_db.active_code=utils.create_random_code(5)
                user_db.save()
                messages.success(request,'ثبت نام شما با موفقیت انجام شد','success')
                return redirect('main:index')
            else:
                return redirect('accounts:change_password')
        
        messages.error(request,'کد وارد شده صحیح نمی باشد','danger')
        return render(request,self.template_name,{'form':form})
    
#-----------------------------------------------------------------------------------------------

class LoginUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    template_name="accounts_app/login.html"  
    def get(self, request, *args, **kwargs):
        form=LoginUserForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form=LoginUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(username=data['mobile_number'],password=data['password'])
            db_user=CustomUser.objects.get(mobile_number=data['mobile_number'])
            if db_user.is_active:
                
                if db_user.is_admin==True:
                    messages.error(request,'کاربر ادمین ایز این بخش نمی تواند وارد شود','danger')
                    return render(request,self.template_name,{'form':form})
                else:
                    messages.success(request,'با موفقیت وارد شدید','success')
                    login(request,user)
                    next_url=request.GET.get('next_url')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('main:index')
                    
            messages.error(request,'حساب کاربری شما مسدود می باشد','danger')
            return render(request,self.template_name,{'form':form})
        
        messages.error(request,'اطلاعات وارد شده صحیح نمی باشد','danger')
        return render(request,self.template_name,{'form':form})

#-----------------------------------------------------------------------------------------------

class LogoutUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs) 
       
    def get(self, request, *args, **kwargs):
        session_data=request.session.get('shop_cart')
        logout(request)
        request.session['shop_cart']=session_data
        messages.success(request,'با موفقیت خارج شدید','success')
        return redirect('main:index')


#-----------------------------------------------------------------------------------------------

class ChangePasswordView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)   
     
    template_name="accounts_app/change_password.html"
    def get(self, request, *args, **kwargs):
        form=ChangePasswordForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session['user_session']
            user_db=CustomUser.objects.get(mobile_number=user_session['mobile_number'])
            user_db.set_password(data['password1'])
            user_db.active_code=utils.create_random_code(5)
            user_db.save()
            messages.success(request,'رمز عبور با موفقیت تغیر یافت','success')
            return redirect('accounts:login')
        
        messages.success(request,'اطلاعات وارد شده صحیح نمی باشد','danger')
        return redirect('accounts:login')
    
#-----------------------------------------------------------------------------------------------

class RememberPasswordView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
        
    template_name="accounts_app/remember_password.html"
    def get(self, request, *args, **kwargs):
        form=RememberPasswordForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form=RememberPasswordForm(request.POST)
        if form.is_valid():
            try:
                data=form.cleaned_data
                user=CustomUser.objects.get(mobile_number=data['mobile_number'])
                active_code=utils.create_random_code(5)
                user.active_code=active_code
                user.save()
                utils.send_sms(data['mobile_number'],'کد شما جهت تغیر رمز عبور {active_code} می باشد.')
                request.session['user_session']={
                    'mobile_number':data['mobile_number'],
                    'active_code':active_code,
                    'remember_password':True
                }
                messages.success(request,'جهت تغیر رمز عبور کد دریافتی را وارد کنید','success')
                return redirect('accounts:verify')
            except:
                messages.error(request,'موبایل وارد شده صحیح نمی باشد','danger')
                return render(request,self.template_name,{'form':form})
        
        messages.error(request,'اطلاعات وارد شده صحیح نمی باشد','danger')
        return render(request,self.template_name,{'form':form})
    
#================================================================================================================================================================================================
                                                #### User panel section



### LoginRequiredMixin : if user dont login , redirect to login page
class UserPanelView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            user=request.user
            customer=Customer.objects.get(user_id=user)
            user_info={
                'name':user.name,
                'family':user.family,
                'mobile_number':user.mobile_number,
                'email':user.email,
                'address':customer.address,
                'phone_number':customer.phone_number,
                'image_name':customer.image_name,
            }
        except ObjectDoesNotExist:
            user_info={
                'name':user.name,
                'family':user.family,
                'mobile_number':user.mobile_number,
                'email':user.email,
            }
        return render(request,'accounts_app/partials/user_panel_dashboard.html',{'user_info':user_info}) 
    
#-----------------------------------------------------------------------------------------------

@login_required
def user_panel_last_order(request):
    last_orders=Order.objects.filter(customer_id=request.user.id).order_by('-register_date')[:5]    
    return render(request,'accounts_app/partials/last_order.html',{'last_orders':last_orders}) 
    
    
#-----------------------------------------------------------------------------------------------
    
class UserPanelUpdateView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        user=request.user
        try:
            customer=Customer.objects.get(user_id=user)
            initial_form_info={
                'mobile_number':user.mobile_number,
                'name':user.name,
                'family':user.family,
                'email':user.email,
                'phone_number':customer.phone_number,
                'address':customer.address,}
            form=UserPanelUpdateForm(initial=initial_form_info) 
        except ObjectDoesNotExist:
            initial_form_info={
                'mobile_number':user.mobile_number,
                'name':user.name,
                'family':user.family,
                'email':user.email,}
            
            form=UserPanelUpdateForm(initial=initial_form_info)
        return render(request, 'accounts_app/partials/user_panel_update.html',{'form':form,'image':customer.image_name})        
    
    
    def post(self, request, *args, **kwargs):
        form=UserPanelUpdateForm(request.POST, request.FILES)
        if request.POST or request.FILES:
            if form.is_valid():
                cd=form.cleaned_data
                user=request.user
                user.name=cd['name']
                user.family=cd['family']
                user.email=cd['email']
                user.save()
                try:
                    customer=Customer.objects.get(user_id=request.user)
                    customer.phone_number=cd['phone_number']
                    customer.address=cd['address']
                    if cd['image']:
                        customer.image_name=cd['image']
                    customer.save()
                except ObjectDoesNotExist:
                    Customer.objects.create(
                        user=request.user,
                        phone_number=cd['phone_number'],
                        address=cd['address'],
                        image_name=cd['image'])
                messages.success(request,'اطلاعات شما با موفقیت ویرایش شد','success')
                return redirect('accounts:user_panel')
            
            messages.error(request,'اطلاعات وارد شده صحیح نمی باشد','danger')
            return render(request, 'accounts_app/partials/user_panel_update.html',{'form':form})
        
        messages.error(request,'اطلاعات وارد شده معتبر نمی باشد','danger')
        return render(request, 'accounts_app/partials/user_panel_update.html',{'form':form})
                            
#-----------------------------------------------------------------------------------------------

@login_required
def peyment_history(request):
    customer=Customer.objects.get(user_id=request.user)
    payments=Payment.objects.filter(customer_id=customer).order_by('register_date')
    return render(request, 'accounts_app/partials/user_panel_payment.html',{'payments':payments})
        
#-----------------------------------------------------------------------------------------------
    
# @login_required
# def peyment_history(request):
#     customer=Customer.objects.get(user_id=request.user)
#     payments=Payment.objects.filter(customer_id=customer).order_by('register_date')
#     return render(request, 'accounts_app/partials/user_panel_payment.html',{'payments':payments})

#-----------------------------------------------------------------------------------------------
   
class ChangePasswordUserPanelView(View):
    template_name="accounts_app/userpanel_changepassword.html"
    def get(self, request, *args, **kwargs):
        form=ChangePasswordForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form=ChangePasswordForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                data=form.cleaned_data
                user=request.user
                user.set_password(data['password1'])
                user.active_code=utils.create_random_code(5)
                user.save()
                messages.success(request,'رمز عبور با موفقیت تغیر یافت','success')
                next_url=request.GET.get('next_url')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('accounts:user_panel')

            return render(request,"accounts_app/userpanel_changepassword.html",{'form':form})   

        return render(request,"accounts_app/userpanel_changepassword.html",{'form':form})