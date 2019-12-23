from django.urls import path
from dex import views

app_name='dex'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('list_all/', views.ListSellOrder.as_view(), name="list_sell"),
    path('addsellorder/', views.NewSellOrder.as_view(), name="add_sell"),
    path('show/<pk>', views.SellDetail.as_view(), name="detail_sell"),
    path('delete/<pk>', views.DeleteSellOrder.as_view(), name="delete_sell")
]