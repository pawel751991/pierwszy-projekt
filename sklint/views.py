from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, View, CreateView, FormView
from django.urls import reverse_lazy
from sklint.models import *
from sklint.forms import *


class ClientMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_object = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.client:
                cart_object.client = request.user.client
                cart_object.save()
        return super().dispatch(request, *args, **kwargs)


class HomeView(ClientMixin, TemplateView):
    template_name = 'home.html'

    # na stronie głównej wyświetla wszytkie produkty w sklepie, przy czym pierwszy produkt to produkt ostatnio dodany
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all().order_by("-id")
        return context


# po przejściu w link kategorie wyświetla pruktu po kategoriach
class AllCategoriesView(ClientMixin, TemplateView):
    template_name = 'allcategories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


# szczegóły produktu
class ProductDetailView(ClientMixin, TemplateView):
    template_name = 'productdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_id = self.kwargs['id']
        product = Product.objects.get(id=url_id)
        context['product'] = product
        return context


# dodawanie produktu do koszyka
class AddToCartView(ClientMixin, TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pobieranie id produktu z url
        product_id = self.kwargs['id']
        product_object = Product.objects.get(id=product_id)
        # sprawdzamy czy koszyk istnieje
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_object = Cart.objects.get(id=cart_id)
            product_in_cart = cart_object.cartproduct_set.filter(product=product_object)
            # przedmiot który już istnieje w koszyku
            if product_in_cart.exists():
                cartproduct = product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_object.price
                cartproduct.save()
                cart_object.total += product_object.price
                cart_object.save()
            # dodawanie nowego przedmiotu do koszyka
            else:
                cartproduct = CartProduct.objects.create(cart=cart_object, product=product_object,
                                                         price=product_object.price, quantity=1,
                                                         subtotal=product_object.price)
                cart_object.total += product_object.price
                cart_object.save()
                return cartproduct
        else:
            cart_object = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_object.id
            cartproduct = CartProduct.objects.create(cart=cart_object, product=product_object,
                                                     price=product_object.price, quantity=1,
                                                     subtotal=product_object.price)
            cart_object.total += product_object.price
            cart_object.save()
            return cartproduct
        return context


# modyfikacja koszyka
class ManageCartView(ClientMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_object = CartProduct.objects.get(id=cp_id)
        cart_object = cp_object.cart
        #        cart1 = cp_object.cart
        #        cart.id = request.session.get("card_id", None)
        #        if cart_id:
        #            cart2 = Cart.objects.get(id=cart_id)
        #            if cart1 != cart2:
        #                return redirect("my-cart")
        # dodawanie produktu w koszyku
        if action == "inc":
            cp_object.quantity += 1
            cp_object.subtotal += cp_object.price
            cp_object.save()
            cart_object.total += cp_object.price
            cart_object.save()
        # usuwanie produktu w koszyku
        elif action == "dcr":
            cp_object.quantity -= 1
            cp_object.subtotal -= cp_object.price
            cp_object.save()
            cart_object.total -= cp_object.price
            cart_object.save()
            if cp_object.quantity == 0:
                cp_object.delete()
        # usuwanie wszystkich produktów z kloszyka
        elif action == "rmv":
            cart_object.total -= cp_object.subtotal
            cart_object.save()
            cp_object.delete()
        else:
            pass
        return redirect('mycart')


# wyświetlanie produktów w koszyku
class MyCartView(ClientMixin, TemplateView):
    template_name = 'mycart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


# sprawdzanie zamówienia
class CheckoutView(ClientMixin, CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.client:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_object = Cart.objects.get(id=cart_id)
        else:
            cart_object = None
        context['cart'] = cart_object
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_object = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_object
            del self.request.session['cart_id']
        else:
            return redirect("")
        return super().form_valid(form)


class ClientRegisterView(CreateView):
    template_name = "clientregister.html"
    form_class = ClientRegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)


class ClientLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")


class ClientLoginView(FormView):
    template_name = "clientlogin.html"
    form_class = ClientLoginForm
    success_url = reverse_lazy("home")

    # form_valid jest jedną z metod post
    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None and user.client:
            login(self.request, user)
        else:
            return render(self.request, "clientlogin.html",
                          {"form": self.form_class, "error": "Nieprawidłowy login lub hasło"})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class OrderHistoryView(TemplateView):
    template_name = 'orderhistory.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.client:
            pass
        else:
            return redirect("/login/?next=/orderhistory/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.request.user.client
        context['client'] = client
        orders = CartProduct.objects.filter(cart__client=client)
        context["cartproduct"] = orders
        return context


class AboutUsView(ClientMixin, TemplateView):
    template_name = 'about.html'


class ContactUsView(ClientMixin, TemplateView):
    template_name = "contactus.html"
