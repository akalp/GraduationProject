from django.urls import path
from dex import views

app_name = 'dex'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('', views.IndexView.as_view(), name="index"),

    path('exchange/', views.ListOrder.as_view(), {'game': None}, name="list_order"),
    path('exchange/<game>', views.ListOrder.as_view(), name="list_order"),

    path('exchange_ajax/', views.ListOrderAjax.as_view(), {'game': None}, name="list_order_ajax"),
    path('exchange_ajax/<game>', views.ListOrderAjax.as_view(), name="list_order_ajax"),

    path('addsellorder/', views.NewSellOrder.as_view(), name="add_sell"),

    path('sell_detail/', views.SellDetail.as_view(), name="detail_sell"),
    path('sell_detail/<pk>', views.SellDetail.as_view(), name="detail_sell"),

    path('delete_sell/', views.DeleteSellOrder.as_view(), name="delete_sell"),
    path('delete_sell/<pk>', views.DeleteSellOrder.as_view(), name="delete_sell"),

    path('addbuyorder/', views.NewBuyOrder.as_view(), name="add_buy"),

    path('buy_detail/', views.BuyDetail.as_view(), name="detail_buy"),
    path('buy_detail/<pk>', views.BuyDetail.as_view(), name="detail_buy"),

    path('delete_buy/', views.DeleteBuyOrder.as_view(), name="delete_buy"),
    path('delete_buy/<pk>', views.DeleteBuyOrder.as_view(), name="delete_buy"),

    path('gamelist/<c>', views.GameListView.as_view(), name="game_list"),

    path('me/', views.ProfileView.as_view(), {'game': None}, name="profile"),
    path('me/<game>', views.ProfileView.as_view(), name="profile"),

    path('me_ajax/', views.ProfileViewAjax.as_view(), {'game': None}, name="profile_ajax"),
    path('me_ajax/<game>', views.ProfileViewAjax.as_view(), name="profile_ajax"),

    path('create_game/', views.GameCreateView.as_view(), name="create_game"),
    path('create_token/', views.TokenCreateView.as_view(), name="create_token"),

    path('developer/', views.DeveloperTemplateView.as_view(), name="developer")
]
