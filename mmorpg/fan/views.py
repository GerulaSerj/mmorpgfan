from django.contrib.auth import authenticate, login
from .forms import RegistrationForm
from .models import CustomUser, Response, Advertisement, Subscription, Category
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ResponseForm, AdvertisementCreateWizard
from django.urls import reverse_lazy
from django.core.cache import cache
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import View
from django.views.decorators.cache import cache_page
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
   ListView, DetailView, CreateView, UpdateView, DeleteView
)
class CustomLoginView(LoginView):
    template_name = 'login.html' # указываем имя шаблона для страницы логина
    redirect_authenticated_user = True # указываем, что уже аутентифицированный пользователь будет перенаправлен на страницу, указанную в LOGIN_REDIRECT_URL в settings.py

class CustomLogoutView(LogoutView):
    pass # используем базовый класс LogoutView без изменений

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = CustomUser.objects.create_user(email=email, password=password)
            user.is_active = False
            user.save()

            send_mail(
                'Account activation',
                'Activate your account with this code: ' + str(user.activation_code),
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return redirect('login')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)

@login_required
def respond_to_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    form = ResponseForm()

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.advertisement = advertisement
            response.user = request.user
            response.save()
            return redirect('view_advertisement', pk=advertisement.pk)

    return render(request, 'response_form.html', {'form': form, 'advertisement': advertisement})

class ResponseForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Response
        fields = ('text',)

class AdvertisementCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = AdvertisementCreateWizard
    model = Advertisement
    template_name = 'advertisement.html'

class AdvertisementListView(ListView):
    model = Advertisement
    ordering = 'created_at'
    template_name = 'alladvertisement.html'
    context_object_name = 'advertisement'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class AdvertisementSearch(ListView):
    model = Advertisement
    ordering = 'category'
    template_name = 'search.html'
    context_object_name = 'category_search'
    paginate_by = 10

    def get_queryset(self):

        queryset = super().get_queryset()
        self.filterset = Advertisement(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context

class AdvertisementDetail(DetailView):
    model = Advertisement
    template_name = 'Advertisement.html'
    context_object_name = 'Advertisement'
    queryset = Advertisement.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'Advertisement-{self.kwargs["pk"]}',
                        None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'Advertisement-{self.kwargs["pk"]}', obj)

        return obj

class AdvertisementUpdate(UpdateView):
    form_class = AdvertisementCreateWizard
    model = Advertisement
    template_name = 'Advertisement_edit.html'

class AdvertisementDelete(DeleteView):
    model = Advertisement
    template_name = 'Advertisement_delete.html'
    success_url = reverse_lazy('Advertisement_list')

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )