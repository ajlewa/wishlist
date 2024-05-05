from django.views.generic import TemplateView, FormView
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from website.forms import SignupForm, NewCategoryForm, WishCreationForm
from website.models import Category, Wish

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        UserModel = get_user_model()
        user = request.user
        if(user.is_anonymous):
            return redirect('login')
        app_user = UserModel.objects.get(id = user.id)
        context = {}
        context['following'] = app_user.following.all()
        context['categories'] = Category.objects.filter(owner=user)

        return render(request, self.template_name, context)
    
class SignupView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class WishlistView(TemplateView):
    template_name = 'wishlist.html'

    def get(self, request, username):
        UserModel = get_user_model()
        user = UserModel.objects.get(username = username)
        categories = Category.objects.filter(owner = user)
        context = {}
        context['user'] = user
        context['categories'] = categories

        return render(request, self.template_name, context)
    
class WishlistDetailView(TemplateView):
    template_name = 'wishlist_detail.html'

    def get(self, request, username, category_id):
        UserModel = get_user_model()
        user = UserModel.objects.get(username = username)
        category = Category.objects.get(id = category_id)
        wishes = [x for x in Wish.objects.filter(owner = user) if x.categories.filter(id = category_id)]
        context = {}
        context['user'] = user
        context['category'] = category
        context['wishes'] = wishes

        return render(request, self.template_name, context)

class NewCategoryView(LoginRequiredMixin, FormView):
    template_name = 'new_category.html'
    form_class = NewCategoryForm
    success_url = reverse_lazy('new_category')
    
    def form_valid(self, form):
        category = form.save(commit=False)
        category.owner = self.request.user
        category.save()
        return super().form_valid(form)

class NewWishView(LoginRequiredMixin, FormView):
    template_name = 'new_wish.html'
    form_class = WishCreationForm
    success_url = reverse_lazy('new_wish')

    def get_form_kwargs(self):
        kwargs = super(NewWishView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        wish = form.save(commit=False)
        wish.owner = self.request.user
        wish.save()
        return super().form_valid(form)