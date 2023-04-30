from django import forms
from .models import CustomUser, Advertisement, Response
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from formtools.wizard.views import SessionWizardView
from django.shortcuts import get_object_or_404, render, redirect
from .models import Advertisement, Response
from .forms import ResponseForm


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')

        return confirm_password

class AdvertisementCreateForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'text', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Создать объявление'))

class AdvertisementUpdateForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'text', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить изменения'))

class AdvertisementContentStep(forms.Form):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    videos = forms.URLField(widget=forms.Textarea(attrs={'rows': 2}))

class AdvertisementCreateWizard(SessionWizardView):
    form_list = [AdvertisementCreateForm, AdvertisementContentStep]
    templates_name = 'advertisement_create_wizard.html'

    def done(self, form_list, form_dict, **kwargs):
        advertisement_form = form_dict['AdvertisementCreateForm']
        content_form = form_dict['AdvertisementContentStep']
        advertisement = advertisement_form.save(commit=False)
        advertisement.author = self.request.user
        advertisement.save()
        for image in self.request.FILES.getlist('images'):
            AdvertisementImage.objects.create(advertisement=advertisement, image=image)
        for video in form_data['videos'].split():
            advertisement.videos.create(video=video)
        return redirect('advertisement_detail', pk=advertisement.pk)

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']

def advertisement_detail(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    responses = advertisement.responses.all()
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.advertisement = advertisement
            response.user = request.user
            response.save()
            return redirect('advertisement_detail', pk=pk)
    else:
        form = ResponseForm()
    context = {'advertisement': advertisement, 'responses': responses, 'form': form}
    return render(request, 'advertisement_detail.html', context)