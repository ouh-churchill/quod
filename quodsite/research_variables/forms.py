from django import forms

from quodsite.research_variables.models import Session, Variable


class SaveSession(forms.ModelForm):
    variables = forms.ModelMultipleChoiceField(queryset=Variable.objects.all())

    class Meta:
        model = Session
        fields = ['session', 'name', 'variables']

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['variables'] = [t.pk for t in kwargs['instance'].variable_set.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.variable_set.clear()
            for variable in self.cleaned_data['variables']:
                instance.variable_set.add(variable)

        self.save_m2m = save_m2m
        if commit:
            instance.save()
            self.save_m2m()



# Variable selection form
class CollectionForm(forms.Form):
    FormName = forms.CharField(max_length=45)
    FormSelection = forms.BooleanField()
