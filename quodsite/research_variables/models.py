from django.db import models
from django import forms


# Data storage models

class NewVariable(models.Model):
    #Contains the information about the variables
    version = models.PositiveIntegerField()
    category = models.PositiveIntegerField()
    section = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()	
	
class NewSession(models.Model):
    user = models.CharField(max_length=45)
    session = models.PositiveIntegerField()
    version = models.CharField(max_length=45)
    timestamp = models.CharField(max_length=45)
    variables = models.ManyToManyField(NewVariable)
    name = models.CharField(max_length=45)
    saves = models.PositiveIntegerField()
    archived = models.BooleanField()
	
	
# Dynamic page models
class DictionaryStructure(models.Model):
    #Stores the rendering structure of variable dictionary
    DictionaryCategory = models.CharField(max_length=45)
    DictionarySection = models.CharField(max_length=45)
    DictionaryVersion = models.CharField(max_length=45)

# Variable selection form  	
class CollectionForm(forms.Form):
    FormName = models.CharField(max_length=45)
    FormSelection = models.BooleanField()
	
class NewCategory(models.Model):
    name = models.CharField(max_length=255)

class NewSection(models.Model):
    level = models.PositiveIntegerField()
    category = models.ForeignKey(NewCategory)
    name = models.CharField(max_length=255)
	
class SaveSession(forms.ModelForm):

    variables = forms.ModelMultipleChoiceField(queryset=NewVariable.objects.all())
    
    class Meta:
        model = NewSession
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
                      
class SaveSession2(forms.ModelForm):

    #variables = forms.ModelMultipleChoiceField(queryset=NewVariable.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = NewSession
        fields = ['session', 'name', 'variables']

	
	
	
