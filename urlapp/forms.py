from django.forms import ModelForm, ModelChoiceField, forms, TextInput, Textarea
from . import models


class URLForm(ModelForm):
    class Meta:
        model = models.Urls
        fields = ['url', 'short_url']
        widgets = {
            'url' : TextInput(attrs={'size' : '45', 'placeholder' : 'Your URL'}),
            'short_url' : TextInput(attrs={'size' : '25', 'placeholder' : 'Your short URL (optional)'})
        }
    def __init__(self, *args, **kwargs):
        super(URLForm, self).__init__(*args, **kwargs)
        self.fields['short_url'].required = False

class ManageForm(ModelForm):
    class Meta:
        model = models.Urls
        fields = [ 'short_url', 'text_message', 'click_count', 'add_date']
        widgets = {
            'short_url' : TextInput(attrs={'size' : '60'}),
            'text_message' : Textarea(attrs={'cols': '80', 'rows': '8'}),
            'click_count' : TextInput(attrs={'size' : '38'}),
            'add_date' : TextInput(attrs={'size' : '38'})
        }
