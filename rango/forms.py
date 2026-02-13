from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        help_text="Please enter the category name."
    )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This category already exists!")
        return name


class PageForm(forms.ModelForm):
    title = forms.CharField(
        help_text="Please enter the title of the page."
    )
    url = forms.URLField(
        help_text="Please enter the URL of the page."
    )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        if url and not url.startswith(('http://', 'https://')):
            url = f'http://{url}'
        cleaned_data['url'] = url
        return cleaned_data
