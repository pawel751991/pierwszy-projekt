"""projektZaliczeniowy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.contrib.auth.models import User
from django.conf.urls.static import static
from sklint.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutUsView.as_view(), name="about"),
    path("contact-us/", ContactUsView.as_view(), name="contact"),
    path("all-categories/", AllCategoriesView.as_view(), name="allcategories"),
    path("product/<int:id>/", ProductDetailView.as_view(), name="productdetail"),
    path("add-to-cart-<int:id>", AddToCartView.as_view(), name="addtocart"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("register/", ClientRegisterView.as_view(), name="clientregistration"),
    path("logout/", ClientLogoutView.as_view(), name="clientlogout"),
    path("login/", ClientLoginView.as_view(), name="clientlogin"),
    path("orderhistory/", OrderHistoryView.as_view(), name="orderhistory"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)