from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,ProductGroup,FeatureValue,Brand
from django.db.models import Q,Count,Min,Max
from django.views import View
from django.http import JsonResponse,HttpResponse
from .filters import ProductFilter
from django.core.paginator import Paginator
from .compare import CompareProduct
#--------------------------------------------------------------------

# return parent group
def get_root_groups():
    return ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))

#--------------------------------------------------------------------

### the cheapest products with parent groups for show in main page
def cheapest_products(request,*args,**kwargs):
    products=Product.objects.filter(is_active=True).order_by('price')[:5]
    # call parent group method
    product_group=get_root_groups()
    context={
        'products':products,
        'product_group':product_group,
    } 
    return render(request,'product_app/partials/cheapest_products.html',context)

#---------------------------------------------------------------------------------------------------

### the newest products with parent groups for show in main page
def th_newest_products(request,*args,**kwargs):
    products=Product.objects.filter(is_active=True).order_by('-register_published')[:5]
    # call parent group method
    product_group=get_root_groups()
    context={
        'products':products,
        'product_group':product_group,
    } 
    return render(request,'product_app/partials/newes_products.html',context)

#---------------------------------------------------------------------------------------------------

### popular groups show in main page

def popular_groups(request,*args,**kwargs): 
    product_groups=ProductGroup.objects.filter(Q(is_active=True))\
        .annotate(count=Count('products_of_group'))\
        .order_by('-count')[:6]
        
    context={
        'product_groups':product_groups,
    }
    return render(request,'product_app/partials/popular_groups.html',context)

#---------------------------------------------------------------------------------------------------

### detail product

class ProductDetailView(View):
    def get(self, request,slug):
        product=get_object_or_404(Product,slug=slug)
        if product.is_active:
            return render(request,'product_app/product_detail.html',{'product':product})
        
#---------------------------------------------------------------------------------------------------
    
### get related products
    
def related_products(request,*args,**kwargs):
    current_product=get_object_or_404(Product,slug=kwargs['slug'])
    related_products=[]
    for group in current_product.product_group.all():
        related_products.extend(Product.objects.filter(Q(is_active=True) & Q(product_group=group) & ~Q(id=current_product.id)))
    return render(request,'product_app/partials/related_product.html',{'related_products':related_products})    
        
#---------------------------------------------------------------------------------------------------

### get all groups of product

def product_group_all(request,*args,**kwargs):
    product_groups=ProductGroup.objects.filter(Q(is_active=True))\
        .annotate(count=Count('products_of_group'))\
        .order_by('-count')
    return render(request,'product_app/product_group_all.html',{'product_groups':product_groups})

#---------------------------------------------------------------------------------------------------





#---------------------------------------------------------------------------------------------------
#**********************************************************************************
### get all product about ech product groups
class products_ech_groups(View):
    def get(self,request,*args,**kwargs):
        slug=kwargs['slug']
        current_group=get_object_or_404(ProductGroup,slug=slug)
        products=Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))
        
       
        ### price filter
        res_aggre=products.aggregate(min=Min('price'),max=Max('price')) ### price for min and max
        price_filter=ProductFilter(request.GET,queryset=products)
        products=price_filter.qs
        
        ### brand filter
        filter_brand=request.GET.getlist('brand')
        if filter_brand:
            products=products.filter(brand__id__in=filter_brand)
        
        ### features filter
        filter_features=request.GET.getlist('feature')
        if filter_features:
            products=products.filter(product_features__filter_value__id__in=filter_features).distinct()
        
        
        
        sort_type=request.GET.get('sort_type')
        if not sort_type:
            sort_type="0"
        elif sort_type=="1":
            products=products.order_by("price")
        elif sort_type=="2":        
            products=products.order_by("-price")
            
            
            
        select_show_product_number=request.GET.get('show_products')
        if not select_show_product_number:
            product_per_page=4
        else:
            product_per_page=int(select_show_product_number)
              
              
        group_slug=slug
        paginator=Paginator(products,product_per_page)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        product_count=products.count()
        
        show_count_product=[i for i in range(0,product_count,2) if i<=product_count+2 and i!=0] 
        
            
        
        
        context={
            'products':products,
            'current_group':current_group,
            'res_aggre':res_aggre,
            'group_slug':group_slug,
            'page_obj':page_obj,
            'product_count':product_count,
            'sort_type':sort_type,
            'price_filter':price_filter,
            'show_count_product':show_count_product,
            }
        
        return render(request,'product_app/products.html',context) 
    
#**********************************************************************************
#---------------------------------------------------------------------------------------------------
    
    
### dropdown ajax for featurevalue in adminpanel part add product
def get_filter_value_for_feature(request):
    
    if request.method == 'GET':
        feature_id=request.GET["feature_id"]
        feature_values=FeatureValue.objects.filter(feature_id=feature_id)
        res={fv.value_title:fv.id for fv in feature_values}
        
        ### another way to handle response
        # import json
        # json_stats = json.dumps(res)
        #return HttpResponse(json_stats,content_type='application/json')
        return JsonResponse(data=res,safe=False)  
    
#---------------------------------------------------------------------------------------------------

### render_partial view for filter of group type :

def filter_get_product_groups(request):
    product_groups=ProductGroup.objects.annotate(count=Count('products_of_group'))\
                                .filter(Q(is_active=True) & ~Q(count=0))\
                                .order_by('-count')
    return render(request,'product_app/partials/product_group.html',{'product_groups':product_groups,})   
                             
#---------------------------------------------------------------------------------------------------

### render_partial view for filter of brands :

def filter_get_product_brands(request,*args,**kwargs):
    current__group=get_object_or_404(ProductGroup, slug=kwargs['slug'])
    ### list of product include this current group , brand id values
    brand_list_id=current__group.products_of_group.filter(Q(is_active=True)).values('brand_id')
    
    brands=Brand.objects.filter(pk__in=brand_list_id)\
        .annotate(count=Count('brands'))\
        .filter(~Q(count=0))\
        .order_by('-count')    
 
    return render(request,'product_app/partials/filter_brands.html',{'brands':brands})   
#---------------------------------------------------------------------------------------------------

### render_partial view for filter of brands :

def filter_get_product_features(request,*args,**kwargs):
    current_group=get_object_or_404(ProductGroup, slug=kwargs['slug'])
    feature_list=current_group.features_of_groups.all()
    feature_dict=dict()
    for feature in feature_list:
        feature_dict[feature]=feature.feature_value.all() 
    return render(request,'product_app/partials/filter_features.html',{'feature_dict':feature_dict})   

#---------------------------------------------------------------------------------------------------


class ShowCompareListView(View):
    def get(self, request, *args, **kwargs):
        compare_list=CompareProduct(request)
        
        context={
            'compare_list':compare_list,
        }
        return render(request,'product_app/compare_list.html',context)
    
 
def compare_table(request):
    compare_product=CompareProduct(request)
    
    products=[]
    for product_id in compare_product.compare_product:
        product=Product.objects.get(id=product_id)
        products.append(product)    
        
    features=[]
    for product in products:
        for item in product.product_features.all():
            if item.feature not in features:
                features.append(item.feature) 
                
    context={
        'products':products,
        'features':features,
    }
    return render(request,'product_app/partials/compare_table.html',context)               
    

def status_of_compare_list(request):
    compare_product=CompareProduct(request)
    return HttpResponse(compare_product.count)

    
def add_to_compare_list(request):
    product_id=request.GET.get('productId')
    product_main_group=request.GET.get('productMainGroup')
    compare_product=CompareProduct(request)
    compare_product.add_to_compare_list(product_id)
    return HttpResponse('کالای مورد نظر در لیست علایق درج شد')


def DeleteFromCompareList(request):
    product_id=request.GET.get('productId')
    compare_product=CompareProduct(request)
    compare_product.remove_from_compare_list(product_id)
    return redirect('products:compare_table')


