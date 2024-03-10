from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from apps.views import ProductListView, ProductDetailView, RegisterFormView, CustomLogoutView, ForgotPasswordView, \
    SettingsView, OrderFormView, SuccessDetailView, UserUpdateView, WishListView, DeleteWishlistView, OperatorView, \
    WishlistPageView, ChangePasswordView
from root import settings

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('login/', LoginView.as_view(template_name='apps/auth/login.html', next_page='product_list'), name='login'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('order/', OrderFormView.as_view(), name='order'),
    path('success/<int:pk>', SuccessDetailView.as_view(), name='success'),
    path('user/update/', UserUpdateView.as_view(), name='update'),
    path('wishlist/<int:product_id>', WishListView.as_view(), name='wishlist_create'),
    path('wishlist/delete/<int:pk>', DeleteWishlistView.as_view(), name='wishlists_delete'),
    path('operator', OperatorView.as_view(), name='operator'),
    path('wishlist', WishlistPageView.as_view(), name='wishlists'),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                        document_root=settings.MEDIA_ROOT)
