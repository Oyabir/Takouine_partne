from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Stagiaire,Edituer,Partenaire,ContactMessagePartenaire



class EdituerForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(max_length=100)
    age = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name','email', 'phone', 'age']





class EdituerFormUpdate(forms.ModelForm):
    class Meta:
        model = Edituer
        fields = ['email','name','phone', 'age']



class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','email']
        
        
        
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control', 'placeholder': fieldname.capitalize()})
            
            
            
from django.forms import DateInput

from django import forms
from .models import Stagiaire, Formation

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['name']
        

from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Stagiaire, Formation

class StagiaireForm(UserCreationForm):
    formations = forms.ModelMultipleChoiceField(queryset=Formation.objects.all()) 
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(max_length=100)
    age = forms.CharField(max_length=100)
    avatar = forms.ImageField(required=False)  
    date_debut = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'name', 'phone', 'age', 'avatar', 'formations', 'date_debut', 'date_fin']
      
        
class StagiaireFormUpdate(forms.ModelForm):
    class Meta:
        model = Stagiaire
        fields = ['name', 'phone', 'age', 'avatar', 'formations', 'date_debut', 'date_fin']



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Partenaire


class PartenaireForm(UserCreationForm):
    CompanyName = forms.CharField(max_length=100, required=False)
    CompanyPhone = forms.CharField(max_length=100, required=False)
    Companyemail = forms.EmailField(required=True)
    category = forms.ChoiceField(choices=Partenaire.CATEGORY_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'CompanyName', 'CompanyPhone', 'Companyemail', 'category']   
        



class PartenaireFormUpdate(forms.ModelForm):
    class Meta:
        model = Partenaire
        fields = ['CompanyName', 'Companyemail','CompanyPhone', 'category']
        
        
        

class PartenaireMoreForm(forms.ModelForm):
    class Meta:
        model = Partenaire
        fields = ['CompanyName', 'Companyemail','CompanyPhone', 'description', 'address', 'logo', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5', 'category']
        
        
       
        
class StagiaireMoreForm(forms.ModelForm):
    class Meta:
        model = Stagiaire
        fields = ['name','email', 'phone', 'age', 'avatar']
        
        
        
        
from django import forms
from .models import ContactMessagePartenaire

class ContactFormPartenaire(forms.ModelForm):
    class Meta:
        model = ContactMessagePartenaire
        fields = ['Companyname', 'email', 'category', 'CompanyPhone']

