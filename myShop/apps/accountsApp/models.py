from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.utils import timezone
from utils import UploadFile
#------------------------------------------------------------------------------
### manage class user: with this class we can create normal user with create_user method 
# and create super user with create_superuser method
class CustomUserManager(BaseUserManager):
    def create_user(self,mobile_number,email="",name="",family="",active_code=None,gender=None,password=None):
        if not mobile_number:
            raise ValueError('شماره موبایل را باید وارد کنید')
        
        user=self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #-------------------------------------------------------------------
    
    ## use create_user function for superuser and then make True some fields
    ### note : in CustomUser class which is our model , we required some field like email,name and family
    ### so in create_user method we need to get that field with empty string. 
    def create_superuser(self,mobile_number,email,name,family,password=None,active_code=None,gender=None):
        user=self.create_user(
            mobile_number=mobile_number,
            email=email,
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
            password=password, 
        )
        user.is_active=True
        user.is_admin=True
        ### using option for make sure that user be save in database
        user.save(using=self._db)
        return user
        
#------------------------------------------------------------------------------

### model of user 
class CustomUser(AbstractBaseUser,PermissionsMixin):
    mobile_number=models.CharField(max_length=11,verbose_name='شماره موبایل',unique=True)
    email=models.EmailField(max_length=200,blank=True,verbose_name='ایمیل')
    name=models.CharField(max_length=50,blank=True,verbose_name='نام')
    family=models.CharField(max_length=50,blank=True,verbose_name='نام خانوادگی')
    CHOICES=(('True','مرد'),('False','زن'))
    gender=models.CharField(max_length=20,choices=CHOICES,blank=True,null=True,verbose_name='جنسیت')
    register_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ ثبت در سیستم')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت فعال/عیرفعال')
    active_code=models.CharField(max_length=100,null=True,blank=True,verbose_name='کد فعالسازی')
    is_admin=models.BooleanField(default=False,verbose_name='وضعیت ادمین/غیرادمین')
    
    ### defined username field
    USERNAME_FIELD='mobile_number'
    ### defined required field for create superuser
    REQUIRED_FIELDS=['email','name','family']
    
    ### for queryset : like model.objects.all()
    objects=CustomUserManager()
    
    def __str__(self):
        return self.name+" "+self.family
    
    ### for access admin panel for superuser
    @property
    def is_staff(self):
        return self.is_admin
    
#------------------------------------------------------------------------------


### defined model for customer 

class Customer(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    phone_number=models.CharField(max_length=11,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    file_upload=UploadFile('images','customer')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر پروفایل',null=True,blank=True)    

    def __str__(self):
        return str(self.user.id)

    class Meta:
        verbose_name ='مشتری'
        verbose_name_plural ='مشتری ها'
        db_table ='t_customer'








