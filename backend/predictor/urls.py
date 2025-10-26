from django.urls import path
from .views import PredictView, home

urlpatterns = [
    # Esto le dice a Django:
    # "Cuando la URL principal te envíe tráfico, 
    # usa la URL 'predict/' para activar la PredictView"
    path('', home, name='home'),
    path('predict/', PredictView.as_view(), name='predict'),
]