from django.urls import path
from . import views

urlpatterns = [
    path('finances/transactions/<int:id_usuario>/', views.FinanzaListCreate.as_view(), name='finanza-list-create'),
    path('finances/details/<int:pk>/', views.FinanzaDetail.as_view(), name='finanza-detail'),
    path('finances/update/<int:pk>/', views.FinanzaUpdate.as_view(), name='finanza-update'),
    path('finances/delete/<int:pk>/', views.FinanzaDelete.as_view(), name='finanza-delete'),
    path('finances/reports/', views.FinanceReport.as_view(), name='finance-report'),
    path('finances/ingreso-total/<int:id_usuario>/', views.IngresoTotal.as_view(), name='ingreso-total'),
    path('finances/create/', views.FinanzaCreateView.as_view(), name='finanza-create'),

]