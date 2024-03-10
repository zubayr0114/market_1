from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView, FormView, UpdateView

from apps.forms import UserRegistrationForm, OrderForm, UserSettingsForm
from apps.models import Product, Order, SiteSettings, WishList, Category


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.order_by('-id')
    paginate_by = 9
    template_name = 'apps/product/product_list.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        category_id = self.request.GET.get('category', None)
        if category_id:
            return self.queryset.filter(category_id=category_id)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent_id=None)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'apps/product/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent_id=None)
        return context


class RegisterFormView(FormView):
    form_class = UserRegistrationForm
    template_name = 'apps/auth/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# class CustomLoginView(LoginView):
#     template_name = 'apps/auth/login.html'
#     authentication_form = AuthenticationForm
#     next_page = 'product-list'
#
#     def form_valid(self, form):
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         return super().form_invalid(form)


class CustomLogoutView(TemplateView):
    template_name = 'apps/auth/logout.html'


class ForgotPasswordView(TemplateView):
    template_name = 'apps/auth/forgot_password.html'


class SettingsView(TemplateView):
    template_name = 'apps/auth/settings.html'


class OrderFormView(FormView):
    form_class = OrderForm
    template_name = 'apps/product/product_detail.html'

    def form_valid(self, form):
        order = form.save()
        order.product.quantity -= order.quantity
        order.product.save()
        return redirect('success', order.id)

    def form_invalid(self, form):
        return super().form_invalid(form)


class SuccessDetailView(DetailView):
    template_name = 'apps/product/success.html'
    queryset = Order.objects.all()
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_settings = SiteSettings.objects.first()
        context['delivery_price'] = site_settings.delivery_price
        return context


class UserUpdateView(UpdateView):
    form_class = UserSettingsForm
    template_name = 'apps/auth/settings.html'
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user


class WishListView(View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        wishlist, created = WishList.objects.get_or_create(user=request.user, product_id=product_id)
        if not created:
            wishlist.delete()
        return redirect('/')


class WishlistPageView(ListView):
    model = WishList
    template_name = 'apps/auth/wishlist.html'
    context_object_name = 'wishlists'

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['total_sum'] = sum(self.get_queryset().values_list('product__price', flat=True))
        return context


class DeleteWishlistView(View):

    def get(self, request, pk=None):
        WishList.objects.filter(user_id=self.request.user.id, product_id=pk).delete()
        return redirect('wishlists')


class OperatorView(ListView):
    model = WishList
    template_name = 'apps/auth/operators.html'
    context_object_name = 'operator'


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'apps/auth/settings.html'
    success_url = reverse_lazy('login')

    def form_invalid(self, form):
        return super().form_invalid(form)