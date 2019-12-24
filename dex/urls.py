from django.urls import path
from dex import views

app_name='dex'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('list_all/', views.ListOrder.as_view(), {'game': None}, name="list_order"),
    path('list_all/<game>', views.ListOrder.as_view(), name="list_order"),
    path('addsellorder/', views.NewSellOrder.as_view(), name="add_sell"),
    path('sell_detail/<pk>', views.SellDetail.as_view(), name="detail_sell"),
    path('delete_sell/<pk>', views.DeleteSellOrder.as_view(), name="delete_sell"),
    path('addbuyorder/', views.NewBuyOrder.as_view(), name="add_buy"),
    path('buy_detail/<pk>', views.BuyDetail.as_view(), name="detail_buy"),
    path('delete_buy/<pk>', views.DeleteBuyOrder.as_view(), name="delete_buy")
]