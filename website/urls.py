from django.urls import path, include
from website.views import HomeView, SignupView, WishlistView, WishlistDetailView, NewCategoryView, NewWishView


urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('wishlist/<str:username>/', WishlistView.as_view(), name = 'wishlist'),
    path('wishlist/<str:username>/<int:category_id>', WishlistDetailView.as_view(), name = 'wishlist_detail'),
    path('wish/new', NewWishView.as_view(), name = 'new_wish'),
    path('category/new', NewCategoryView.as_view(), name = 'new_category'),
    path('signup', SignupView.as_view(), name = 'signup'),
    path('', include('django.contrib.auth.urls')),
]
