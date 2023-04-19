from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('cheapest_products/',cheapest_products,name='cheapest_products'),
    path('newest_products/',th_newest_products,name='newest_products'),
    path('popular_groups/',popular_groups,name='popular_groups'),
    path('product_detail/<slug:slug>/',ProductDetailView.as_view(),name='product_detail'),
    path('related_product/<slug:slug>/',related_products,name='related_product'),
    path('product_group_all/',product_group_all,name='product_group_all'),
    path('products_ech_group/<slug:slug>/',products_ech_groups.as_view(),name='products_ech_group'),
    path('ajax_admin/',get_filter_value_for_feature,name='filter_value_for_feature'),
    path('filter_get_product_groups/',filter_get_product_groups,name='filter_get_product_groups'),
    path('filter_get_product_brands/<slug:slug>/',filter_get_product_brands,name='filter_get_product_brands'),
    path('filter_get_product_features/<slug:slug>/',filter_get_product_features,name='filter_get_product_features'),
    path('compare_list/',ShowCompareListView.as_view(),name='compare_list'),
    path('compare_table/',compare_table,name='compare_table'),
    path('add_to_compare_list/',add_to_compare_list,name='add_to_compare_list'),
    path('delete_from_compare_list/',DeleteFromCompareList,name='delete_from_compare_list'),
    path('status_of_compare_list/',status_of_compare_list,name='status_of_compare_list'),
   
]
