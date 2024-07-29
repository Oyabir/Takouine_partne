from django.shortcuts import render,redirect ,get_object_or_404
from .models import *
from .forms import EdituerForm,EdituerFormUpdate,UserUpdateForm,PasswordChangeForm,StagiaireForm,StagiaireFormUpdate,PartenaireForm,PartenaireFormUpdate
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from .decorators import notLoggedUsers,allowedUsers,forAdmins
from django.contrib.auth.models import User, Group
from .decorators import notLoggedUsers,allowedUsers,forAdmins
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login 
from django.shortcuts import render
from .models import Edituer
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from chartjs.views.lines import BaseLineChartView
from .models import Achat, Visite
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, reverse
from django.db.models import Count


# #Home
# def home(request):
#     if request.user.is_authenticated:
#         # Check if the user belongs to the group "Edituer" and "Stagiaire"
#         is_edituer = request.user.groups.filter(name='Edituer').exists()
#         is_stagiaire = request.user.groups.filter(name='stagiaire').exists()
#         is_partenaire = request.user.groups.filter(name='partenaire').exists()
#     else:
#         is_edituer = False
#         is_stagiaire = False   
#         is_partenaire= False     
#     context = {"is_edituer": is_edituer,"is_stagiaire": is_stagiaire,"is_partenaire": is_partenaire}

#     return render(request, "takouine/home.html",context)



def test(requset):
    return render(requset,"takouine/test.html")



#Add Edituer all
@notLoggedUsers
def register(request):
    form = EdituerForm()
    if request.method == 'POST':
        form = EdituerForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name="Edituer")
            user.groups.add(group)
            messages.success(request, f"{username} created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Invalid form submission. Please correct the errors below.")  
        
    context = {'form': form}
    return render(request, 'takouine/register.html', context)



#Login for Partenaire
@notLoggedUsers
def Partenairelogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.groups.filter(name='partenaire').exists():
                return redirect('/escpasPartenaire')
            elif request.user.groups.filter(name='Edituer').exists():
                return redirect('/escpasEdituer')
            if request.user.groups.filter(name='admin').exists():
                return redirect('/escpasAdmin')
            if request.user.groups.filter(name='stagiaire').exists():
                return redirect('/escpasStagiairer')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request,"takouine/PartenaireLoginHome/EscapePartenaireLogin.html")
 
 
 
 
 

#Login for Stagiaire
@notLoggedUsers
def Stagiairelogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request,user)
            if request.user.groups.filter(name='partenaire').exists():
                return redirect('/escpasPartenaire')
            elif request.user.groups.filter(name='Edituer').exists():
                return redirect('/escpasEdituer')
            if request.user.groups.filter(name='admin').exists():
                return redirect('/escpasAdmin')
            if request.user.groups.filter(name='stagiaire').exists():
                return redirect('/escpasStagiairer')
        else:
            messages.info(request,'email or password is 0')

    context = {}
    return render(request,"takouine/StagiaireLoginHome/EscapeStagiaireLogin.html", context)
 
 
 
 
 
    
    
from django.contrib.auth.decorators import login_required



#Logout for all

def userLogout(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='partenaire').exists():
            redirect_path = 'EscapePartenaireLogin'
        elif request.user.groups.filter(name='stagiaire').exists():
            redirect_path = 'EscapeStagiaireLogin'
        elif request.user.groups.filter(name='admin').exists():
            redirect_path = 'EscapePartenaireLogin'
        elif request.user.groups.filter(name='Edituer').exists():
            redirect_path = 'EscapePartenaireLogin'
        else:
            redirect_path = 'EscapePartenaireLogin'  # Default redirect

        # Perform logout
        logout(request)
        
        # Redirect to the appropriate page
        return redirect(redirect_path)




#escpasAdmin
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])   
def escpasAdmin(request):
    edituers = User.objects.filter(groups__name='Edituer')
    stagiaires = User.objects.filter(groups__name='stagiaire')
    partenaires = User.objects.filter(groups__name='partenaire')
    
    total_edituers = User.objects.filter(groups__name='Edituer').count()
    total_admins = User.objects.filter(groups__name='admin').count()
    total_stagiaires = User.objects.filter(groups__name='stagiaire').count()
    total_partenaires = User.objects.filter(groups__name='partenaire').count()
    
    context = {'edituers': edituers,'stagiaires': stagiaires ,'total_edituers': total_edituers,'total_admins': total_admins,'total_stagiaires': total_stagiaires,'partenaires': partenaires,'total_partenaires':total_partenaires} 
    return render(request, "takouine/escpasAdminEdituer/escpasAdmin.html", context)

from django.contrib import messages


#Add Edituer
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin']) 
def registerEdituer(request):
    form = EdituerForm()
    if request.method == 'POST':
        form = EdituerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save user object first without committing to the database
            user.save()  # Save the user object to generate an ID

            # Now create a Customer object associated with the user
            Edituer.objects.create(
                user=user,
                name=form.cleaned_data.get('name'),
                email=form.cleaned_data.get('email'),
                phone=form.cleaned_data.get('phone'),
                age=form.cleaned_data.get('age')
            )

            # Add user to the 'Edituer' group
            group = Group.objects.get(name="Edituer")
            user.groups.add(group)

            messages.success(request, f"{user.username} created successfully!")
            
            return redirect('/escpasAdmin')
        else:
            messages.error(request, "Invalid form submission. Please correct the errors below.")  
        
    context = {'form': form}
    return render(request, 'takouine/escpasAdminEdituer/registerEdituer.html', context)




# Update Edituer
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin']) 
def update_edituer(request, slugEdituer):
    edituer = get_object_or_404(Edituer, slugEdituer=slugEdituer)
    user = edituer.user
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        edituer_form = EdituerFormUpdate(request.POST, instance=edituer)
        if user_form.is_valid() and edituer_form.is_valid():
            user_form.save()
            edituer_form.save()
            messages.success(request, "User and customer updated successfully!")
            return redirect('/escpasAdmin')
        else:
            messages.error(request, "Invalid form submission. Please correct the errors below.")
    else:
        user_form = UserUpdateForm(instance=user)
        edituer_form = EdituerFormUpdate(instance=edituer)
    
    return render(request, 'takouine/escpasAdminEdituer/update_edituer.html', {'user_form': user_form, 'edituer_form': edituer_form})



# Change Password for Edituer
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin']) 
def change_password(request, slugEdituer):
    edituer = get_object_or_404(Edituer, slugEdituer=slugEdituer)
    user = edituer.user

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/escpasAdmin')  
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user)
    
    return render(request, 'takouine/escpasAdminEdituer/change_password.html', {'form': form})




@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin']) 
def delete_edituer(request, slugEdituer):
    try:
        edituer = get_object_or_404(Edituer, slugEdituer=slugEdituer)
    except Edituer.DoesNotExist:
        return HttpResponse("Edituer does not exist.", status=404)

    if request.method == 'POST':
        edituer.user.delete()  
        edituer.delete()  
        return redirect('/escpasAdmin')  

    return render(request, 'takouine/escpasAdminEdituer/delete_edituer.html', {'edituer': edituer})



#formations

from .forms import FormationForm

@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])   
def add_formation(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.groups.filter(name='admin').exists():
                return redirect('/escpasAdminFormation')
            elif request.user.groups.filter(name='Edituer').exists():
                return redirect('/escpasEdituerFormation')
        else:
            print(form.errors) 
    else:
        form = FormationForm()
    return form



@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def add_formationAdmin(request):
    if request.method == 'POST':
        form = FormationForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Formation added successfully!')
            return redirect('escpasAdminFormation')  # Redirect to a list view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FormationForm()  
    return render(request, 'takouine/escpasAdminFormation/add_formation.html', {'form': form})





@login_required(login_url='login')
@allowedUsers(allowedGroups=['Edituer'])
def add_formationEdituer(request):
    if request.method == 'POST':
        form = FormationForm(request.POST, request.FILES)  #i can delated request.FILES
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Formation added successfully!')
            return redirect('escpasEdituerFormation')  # Redirect to a list view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FormationForm()  

    return render(request, 'takouine/escpasEdituer/add_formation.html', {'form': form})

    



@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])  
def delete_formation(request, slugFormation):
    formation = get_object_or_404(Formation, slugFormation=slugFormation)
    if request.method == 'POST':
        formation.delete()
        messages.success(request, 'Formation deleted successfully!')
        # Check if the user is an admin or an editor and set the redirect URL
        if request.user.groups.filter(name='admin').exists():
            redirect_url = 'escpasAdminFormation'
        elif request.user.groups.filter(name='Edituer').exists():
            redirect_url = 'escpasEdituerFormation'
        return redirect(reverse(redirect_url))
    
    # Pass the redirect_url to the template
    if request.user.groups.filter(name='admin').exists():
        redirect_url = 'escpasAdminFormation'
    elif request.user.groups.filter(name='Edituer').exists():
        redirect_url = 'escpasEdituerFormation'
    else:
        redirect_url = None

    return render(request, 'takouine/escpasAdminFormation/delete_formation.html', {
        'formation': formation,
        'redirect_url': redirect_url
    })



@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])  
def update_formation(request, slugFormation):
    formation = get_object_or_404(Formation, slugFormation=slugFormation)
    if request.method == 'POST':
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formation Updated successfully!')
            if request.user.groups.filter(name='admin').exists():
                return redirect('/escpasAdminFormation')
            elif request.user.groups.filter(name='Edituer').exists():
                return redirect('/escpasEdituerFormation')
    else:
        form = FormationForm(instance=formation)
    return render(request, 'takouine/escpasAdminFormation/update_formation.html', {'form': form})



#escpasEdituer
@login_required(login_url='login')
@allowedUsers(allowedGroups=['Edituer'])   
def escpasEdituerFormation(request):
    formations = Formation.objects.all()
    
    edituers = User.objects.filter(groups__name='Edituer')
    stagiaires = User.objects.filter(groups__name='stagiaire')
    partenaires = User.objects.filter(groups__name='partenaire')
    
    total_edituers = User.objects.filter(groups__name='Edituer').count()
    total_admins = User.objects.filter(groups__name='admin').count()
    total_stagiaires = User.objects.filter(groups__name='stagiaire').count()
    total_partenaires = User.objects.filter(groups__name='partenaire').count()
    
    return render(request, 'takouine/escpasEdituer/formations.html', {'formations': formations,'edituers': edituers,'stagiaires': stagiaires ,'total_edituers': total_edituers,'total_admins': total_admins,'total_stagiaires': total_stagiaires,'partenaires': partenaires,'total_partenaires':total_partenaires})




#escpasAdmin
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])   
def escpasAdminFormation(request):
    formations = Formation.objects.all()
    
    edituers = User.objects.filter(groups__name='Edituer')
    stagiaires = User.objects.filter(groups__name='stagiaire')
    partenaires = User.objects.filter(groups__name='partenaire')
    
    total_edituers = User.objects.filter(groups__name='Edituer').count()
    total_admins = User.objects.filter(groups__name='admin').count()
    total_stagiaires = User.objects.filter(groups__name='stagiaire').count()
    total_partenaires = User.objects.filter(groups__name='partenaire').count()
    
    return render(request, 'takouine/escpasAdminFormation/formations.html', {'formations': formations,'edituers': edituers,'stagiaires': stagiaires ,'total_edituers': total_edituers,'total_admins': total_admins,'total_stagiaires': total_stagiaires,'partenaires': partenaires,'total_partenaires':total_partenaires})



#escpasAdmin
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])   
def escpasEdituerFormation(request):
    formations = Formation.objects.all()
    
    edituers = User.objects.filter(groups__name='Edituer')
    stagiaires = User.objects.filter(groups__name='stagiaire')
    partenaires = User.objects.filter(groups__name='partenaire')
    
    total_edituers = User.objects.filter(groups__name='Edituer').count()
    total_admins = User.objects.filter(groups__name='admin').count()
    total_stagiaires = User.objects.filter(groups__name='stagiaire').count()
    total_partenaires = User.objects.filter(groups__name='partenaire').count()
    
    return render(request, 'takouine/escpasEdituer/formations.html', {'formations': formations,'edituers': edituers,'stagiaires': stagiaires ,'total_edituers': total_edituers,'total_admins': total_admins,'total_stagiaires': total_stagiaires,'partenaires': partenaires,'total_partenaires':total_partenaires})




#Stagiaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])    
def registerStagiaire(request):
    form = StagiaireForm()
    if request.method == 'POST':
        form = StagiaireForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Check if a Stagiaire object already exists for the user
            try:
                stagiaire = user.stagiaire
            except Stagiaire.DoesNotExist:
                # If not, create a new Stagiaire object associated with the user
                stagiaire = Stagiaire.objects.create(user=user)

            # Update Stagiaire object fields based on form data
            stagiaire.name = form.cleaned_data.get('name')
            stagiaire.email = form.cleaned_data.get('email')
            stagiaire.phone = form.cleaned_data.get('phone')
            stagiaire.age = form.cleaned_data.get('age')
            stagiaire.avatar = form.cleaned_data.get('avatar')
            stagiaire.date_debut = form.cleaned_data.get('date_debut')
            stagiaire.date_fin = form.cleaned_data.get('date_fin')
            stagiaire.save()

            # Update Stagiaire formations
            formations = form.cleaned_data.get('formations')
            stagiaire.formations.set(formations)

            # Add user to the 'stagiaire' group
            group = Group.objects.get(name="stagiaire")
            user.groups.add(group)

            messages.success(request, f"{user.username} created successfully!")

            if request.user.groups.filter(name='admin').exists():
                return redirect('/escpasAdminStagiaire')
            elif request.user.groups.filter(name='Edituer').exists():
                return redirect('/escpasEdituer')
        else:
            messages.error(request, "Invalid form submission. Please correct the errors below.")  

    context = {'form': form}
    return render(request, 'takouine/escpasAdminStagiaire/registerStagiaire.html', context)



# Update Stagiaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])    
def update_stagiaire(request, slugStagiaire):
    stagiaire = get_object_or_404(Stagiaire, slugStagiaire=slugStagiaire)
    user = stagiaire.user
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        stagiaire_form = StagiaireFormUpdate(request.POST, request.FILES, instance=stagiaire)
        if user_form.is_valid() and stagiaire_form.is_valid():
            user_form.save()
            stagiaire_form.save()
            messages.success(request, "User and customer updated successfully!")
            if request.user.groups.filter(name='admin').exists():
                return redirect('/escpasAdminStagiaire') 
            elif request.user.groups.filter(name='Edituer').exists():
                return redirect('/escpasEdituer') 
        else:
            messages.error(request, "Invalid form submission. Please correct the errors below.")
    else:
        user_form = UserUpdateForm(instance=user)
        stagiaire_form = StagiaireFormUpdate(instance=stagiaire)
    
    return render(request, 'takouine/escpasAdminStagiaire/update_stagiaire.html', {'user_form': user_form, 'stagiaire_form': stagiaire_form})



# Delete Stagiaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])
def delete_stagiaire(request, slugStagiaire):
    try:
        stagiaire = get_object_or_404(Stagiaire, slugStagiaire=slugStagiaire)
    except Stagiaire.DoesNotExist:
        return HttpResponse("stagiaire does not exist.", status=404)

    if request.method == 'POST':
        stagiaire.user.delete()
        stagiaire.delete()
        
        # Check user group and redirect
        if request.user.groups.filter(name='admin').exists():
            return redirect('/escpasAdminStagiaire')
        elif request.user.groups.filter(name='Edituer').exists():
            return redirect('/escpasEdituer')

    # Determine the redirect URL for the template
    if request.user.groups.filter(name='admin').exists():
        redirect_url = 'escpasAdminStagiaire'
    elif request.user.groups.filter(name='Edituer').exists():
        redirect_url = 'escpasEdituer'
    else:
        redirect_url = None  # or a default URL if needed

    return render(request, 'takouine/escpasAdminStagiaire/delete_stagiaire.html', {
        'stagiaire': stagiaire,
        'redirect_url': redirect_url
    })




#Change Password for Stagiaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])    
def change_password_stagiaire(request, slugStagiaire):
    stagiaire = get_object_or_404(Stagiaire, slugStagiaire=slugStagiaire)
    user = stagiaire.user

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
             # Check if the user is an admin or an editor
            if request.user.groups.filter(name='admin').exists():
                return redirect('/escpasAdminStagiaire')
            elif request.user.groups.filter(name='Edituer').exists():
                return redirect('/escpasEdituer')  
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user)
    
    return render(request, 'takouine/escpasAdminStagiaire/change_password_stagiaire.html', {'form': form})




#escpasAdminStagiaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])   
def escpasAdminStagiaire(request):
    edituers = User.objects.filter(groups__name='Edituer')
    stagiaires = User.objects.filter(groups__name='stagiaire')
    partenaires = User.objects.filter(groups__name='partenaire')
    
    total_edituers = User.objects.filter(groups__name='Edituer').count()
    total_admins = User.objects.filter(groups__name='admin').count()
    total_stagiaires = User.objects.filter(groups__name='stagiaire').count()
    total_partenaires = User.objects.filter(groups__name='partenaire').count()
    
    context = {'edituers': edituers,'stagiaires': stagiaires ,'total_edituers': total_edituers,'total_admins': total_admins,'total_stagiaires': total_stagiaires,'partenaires': partenaires,'total_partenaires':total_partenaires} 
    return render(request, "takouine/escpasAdminStagiaire/escpasAdminStagiaire.html", context)



#Partenaire

#Add Partenaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])    
def registerPartenaire(request):
    form = PartenaireForm()
    if request.method == 'POST':
        form = PartenaireForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save user object first without committing to the database
            user.save()  # Save the user object to generate an ID

            # Now create a Partenaire object associated with the user
            partenaire = Partenaire.objects.create(
                user=user,
                CompanyName=form.cleaned_data.get('CompanyName'),
                CompanyPhone=form.cleaned_data.get('CompanyPhone'),
                Companyemail=form.cleaned_data.get('Companyemail'),
                category=form.cleaned_data.get('category')  # Add category field
            )

            # Add user to the 'partenaire' group
            group = Group.objects.get(name="partenaire")
            user.groups.add(group)

            messages.success(request, f"{user.email} created successfully!")
            # Check if the user is an admin or an editor
            if request.user.groups.filter(name='admin').exists():
                return redirect('/escpasAdminPartenaire')  # Redirect to admin stagiaire page
            elif request.user.groups.filter(name='Edituer').exists():
                return redirect('/escpasEdituerPartenaire')  # Redirect to edituer page
        else:
            messages.error(request, "Invalid form submission. Please correct the errors below.")  
        
    context = {'form': form}
    return render(request, 'takouine/escpasAdminPartenaire/registerPartenaire.html', context)




#Update Partenaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])    
def update_partenaire(request, slugPartenaire):
    partenaire = get_object_or_404(Partenaire, slugPartenaire=slugPartenaire)
    user = partenaire.user
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        partenaire_form = PartenaireFormUpdate(request.POST, instance=partenaire)
        if user_form.is_valid() and partenaire_form.is_valid():
            user_form.save()
            partenaire_form.save()
            messages.success(request, "User and partenaire updated successfully!")
            # Check if the user is an admin or an editor
            if request.user.groups.filter(name='admin').exists():
                return redirect('/escpasAdminPartenaire')
            elif request.user.groups.filter(name='Edituer').exists():
                return redirect('/escpasEdituerPartenaire') 
        else:
            messages.error(request, "Invalid form submission. Please correct the errors below.")
    else:
        user_form = UserUpdateForm(instance=user)
        previous_category_value = partenaire.category
        partenaire_form = PartenaireFormUpdate(instance=partenaire, initial={'category': previous_category_value})

    
    return render(request, 'takouine/escpasAdminPartenaire/update_partenaire.html', {'user_form': user_form, 'partenaire_form': partenaire_form})





# Delete Partenaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])
def delete_partenaire(request, slugPartenaire):
    try:
        partenaire = get_object_or_404(Partenaire, slugPartenaire=slugPartenaire)
    except Partenaire.DoesNotExist:
        return HttpResponse("Partenaire does not exist.", status=404)

    if request.method == 'POST':
        partenaire.user.delete()
        partenaire.delete()
        
        # Check user group and redirect
        if request.user.groups.filter(name='admin').exists():
            return redirect('/escpasAdminPartenaire')
        elif request.user.groups.filter(name='Edituer').exists():
            return redirect('/escpasEdituerPartenaire')

    # Determine the redirect URL for the template
    if request.user.groups.filter(name='admin').exists():
        redirect_url = 'escpasAdminPartenaire'
    elif request.user.groups.filter(name='Edituer').exists():
        redirect_url = 'escpasEdituerPartenaire'
    else:
        redirect_url = None  # or a default URL if needed

    return render(request, 'takouine/escpasAdminPartenaire/delete_partenaire.html', {
        'partenaire': partenaire,
        'redirect_url': redirect_url
    })



# Change Password for Partenaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])    
def change_password_partenaire(request, slugPartenaire):
    partenaire = get_object_or_404(Partenaire, slugPartenaire=slugPartenaire)
    user = partenaire.user

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            # Check if the user is an admin or an editor
            if request.user.groups.filter(name='admin').exists():
                return redirect('/escpasAdminPartenaire')  # Adjusted to correct URL
            elif request.user.groups.filter(name='Edituer').exists():
                return redirect('/escpasEdituerPartenaire')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user)
    
    # Determine the redirect URL for the template
    if request.user.groups.filter(name='admin').exists():
        redirect_url = 'escpasAdminPartenaire'
    elif request.user.groups.filter(name='Edituer').exists():
        redirect_url = 'escpasEdituerPartenaire'
    else:
        redirect_url = 'home'  # Default URL if needed

    return render(request, 'takouine/escpasAdminPartenaire/change_password_partenaire.html', {
        'form': form,
        'redirect_url': redirect_url
    })
    
    
#escpasAdminStagiaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])    
def escpasAdminPartenaire(request):
    edituers = User.objects.filter(groups__name='Edituer')
    stagiaires = User.objects.filter(groups__name='stagiaire')
    partenaires = User.objects.filter(groups__name='partenaire')
    
    total_edituers = User.objects.filter(groups__name='Edituer').count()
    total_admins = User.objects.filter(groups__name='admin').count()
    total_stagiaires = User.objects.filter(groups__name='stagiaire').count()
    total_partenaires = User.objects.filter(groups__name='partenaire').count()
    
    context = {'edituers': edituers,'stagiaires': stagiaires ,'total_edituers': total_edituers,'total_admins': total_admins,'total_stagiaires': total_stagiaires,'partenaires': partenaires,'total_partenaires':total_partenaires} 
    return render(request, "takouine/escpasAdminPartenaire/escpasAdminPartenaire.html", context)


#escpasEdituer
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer']) 
def escpasEdituer(request):
    edituers = User.objects.filter(groups__name='Edituer')
    stagiaires = User.objects.filter(groups__name='stagiaire')
    partenaires = User.objects.filter(groups__name='partenaire')
    
    total_edituers = User.objects.filter(groups__name='Edituer').count()
    total_admins = User.objects.filter(groups__name='admin').count()
    total_stagiaires = User.objects.filter(groups__name='stagiaire').count()
    total_partenaires = User.objects.filter(groups__name='partenaire').count()
    
    context = {'edituers': edituers,'stagiaires': stagiaires ,'total_edituers': total_edituers,'total_admins': total_admins,'total_stagiaires': total_stagiaires,'partenaires': partenaires,'total_partenaires':total_partenaires} 
    return render(request, "takouine/escpasEdituer/escpasEdituer.html", context)


#escpasEdituerPartenaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])    
def escpasEdituerPartenaire(request):
    edituers = User.objects.filter(groups__name='Edituer')
    stagiaires = User.objects.filter(groups__name='stagiaire')
    partenaires = User.objects.filter(groups__name='partenaire')
    
    total_edituers = User.objects.filter(groups__name='Edituer').count()
    total_admins = User.objects.filter(groups__name='admin').count()
    total_stagiaires = User.objects.filter(groups__name='stagiaire').count()
    total_partenaires = User.objects.filter(groups__name='partenaire').count()
    
    context = {'edituers': edituers,'stagiaires': stagiaires ,'total_edituers': total_edituers,'total_admins': total_admins,'total_stagiaires': total_stagiaires,'partenaires': partenaires,'total_partenaires':total_partenaires} 
    return render(request, "takouine/escpasEdituer/escpasEdituerPartenaire.html", context)



@login_required(login_url='login')  
@allowedUsers(allowedGroups=['admin','Edituer']) 
def rapportsFormation(request):
    stagiaires = Stagiaire.objects.all()[:10]
    partenaires = Partenaire.objects.all()[:10]

    return render(request, 'takouine/escpasAdminRapports/rapportsFormation.html', {'stagiaires': stagiaires,'partenaires':partenaires})


from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from io import BytesIO
from django.template.loader import render_to_string


#pdf ALL Stagiaires 
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])
def generate_stagiaires_pdf(request):
    stagiaires = Stagiaire.objects.all().order_by('-date_created')
    context = {'stagiaires': stagiaires}
    
    # Render the HTML template to a string
    html = render_to_string('takouine/escpasAdminRapports/pdf_template_stagiaires.html', context)
    
    # Create a bytes buffer for the PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Create styles
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    header_style = styles['Heading2']
    
    # Start with the header
    elements = []
    elements.append(Paragraph('Tous les Stagiaires', header_style))
    
    # Create table data
    table_data = []
    table_data.append(["Nom d'utilisateur", 'E-mail', 'Code Stagiaire', 'Formations'])
    
    for stagiaire in context['stagiaires']:
        formations = ', '.join([formation.name for formation in stagiaire.formations.all()])
        table_data.append([
            stagiaire.name,
            stagiaire.email,
            stagiaire.stagiaireCode,
            formations
        ])
    
    # Create a table and style it
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#f2f2f2'),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONT', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 1), (-1, -1), '#ffffff'),
    ]))
    
    elements.append(table)
    
    # Build the PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="stagiaires_all.pdf"'
    return response




#PDF ALL Partenaires
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin', 'Edituer'])
def generate_partenaires_pdf(request):
    partenaires = Partenaire.objects.all().order_by('-date_created')
    context = {'partenaires': partenaires}
    
    # Render the HTML template to a string
    html = render_to_string('takouine/escpasAdminRapports/pdf_template_partenaires.html', context)
    
    # Create a bytes buffer for the PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Create styles
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    header_style = styles['Heading2']
    
    # Start with the header
    elements = []
    elements.append(Paragraph('Tous les partenaires', header_style))
    
    # Create table data
    table_data = []
    table_data.append(["Nom de l'entreprise", 'E-mail', "Code de l'entreprise"])
    
    for partenaire in context['partenaires']:
        table_data.append([
            partenaire.CompanyName,
            partenaire.Companyemail,
            partenaire.CompanyCode
        ])
    
    # Create a table and style it
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#f2f2f2'),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONT', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 1), (-1, -1), '#ffffff'),
    ]))
    
    elements.append(table)
    
    # Build the PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="partenaires_all.pdf"'
    return response




@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin','Edituer'])   
def escpasAdminRapports(request):
    stagiaires = Stagiaire.objects.all()[:10]
    partenaires = Partenaire.objects.all()[:10]
    
    total_edituers = User.objects.filter(groups__name='Edituer').count()
    total_admins = User.objects.filter(groups__name='admin').count()
    total_stagiaires = User.objects.filter(groups__name='stagiaire').count()
    total_partenaires = User.objects.filter(groups__name='partenaire').count()
    
    return render(request, 'takouine/escpasAdminRapports/rapportsFormation.html', {'stagiaires': stagiaires,'partenaires':partenaires ,'total_edituers': total_edituers,'total_admins': total_admins,'total_stagiaires': total_stagiaires,'partenaires': partenaires,'total_partenaires':total_partenaires})




# #escpasAdminRapports
# @login_required(login_url='login')
# @allowedUsers(allowedGroups=['admin'])   
# def escpasAdminRapports(request):
#     stagiaires = Stagiaire.objects.all()[:10]
#     partenaires = Partenaire.objects.all()[:10]
    
#     total_edituers = User.objects.filter(groups__name='Edituer').count()
#     total_admins = User.objects.filter(groups__name='admin').count()
#     total_stagiaires = User.objects.filter(groups__name='stagiaire').count()
#     total_partenaires = User.objects.filter(groups__name='partenaire').count()
    
#     return render(request, 'takouine/escpasAdminRapports/rapportsFormation.html', {'stagiaires': stagiaires,'partenaires':partenaires ,'total_edituers': total_edituers,'total_admins': total_admins,'total_stagiaires': total_stagiaires,'partenaires': partenaires,'total_partenaires':total_partenaires})



#escpasAdminRapports
@login_required(login_url='login')
@allowedUsers(allowedGroups=['Edituer'])   
def escpasEdituerRapports(request):
    stagiaires = Stagiaire.objects.all()[:10]
    partenaires = Partenaire.objects.all()[:10]
    
    total_edituers = User.objects.filter(groups__name='Edituer').count()
    total_admins = User.objects.filter(groups__name='admin').count()
    total_stagiaires = User.objects.filter(groups__name='stagiaire').count()
    total_partenaires = User.objects.filter(groups__name='partenaire').count()
    
    return render(request, 'takouine/escpasEdituer/escpasEdituerRapports.html', {'stagiaires': stagiaires,'partenaires':partenaires ,'total_edituers': total_edituers,'total_admins': total_admins,'total_stagiaires': total_stagiaires,'partenaires': partenaires,'total_partenaires':total_partenaires})





def is_partner(user):
    return user.groups.filter(name='partenaire').exists()


def get_total_achat_today(partenaire, today):
    total_achat_today = Achat.objects.filter(partenaire=partenaire, date_added__date=today).aggregate(total_achat_today=Sum('amount'))['total_achat_today']
    return total_achat_today or 0

def get_total_achat_month(partenaire, today):
    first_day_of_month = today.replace(day=1)
    thirtieth_day_of_month = first_day_of_month + timedelta(days=29)
    total_achat_month = Achat.objects.filter(partenaire=partenaire, date_added__gte=first_day_of_month, date_added__lte=thirtieth_day_of_month).aggregate(total_achat_month=Sum('amount'))['total_achat_month']
    return total_achat_month or 0

def get_total_visite_month(partenaire, today):
    first_day_of_month = today.replace(day=1)
    thirtieth_day_of_month = first_day_of_month + timedelta(days=29)
    total_visite_month = Visite.objects.filter(partenaire=partenaire, date_visited__gte=first_day_of_month, date_visited__lte=thirtieth_day_of_month).count()
    return total_visite_month






def get_daily_totals(model, partenaire, today):
    first_day_of_month = today.replace(day=1)
    thirtieth_day_of_month = first_day_of_month + timedelta(days=29)
    last_day_of_month = (first_day_of_month.replace(day=1, month=first_day_of_month.month + 1) - timedelta(days=1))  # Remove .date() here
    
    date_field = 'date_added' if model == Achat else 'date_visited'
    daily_data = (
        model.objects
        .filter(partenaire=partenaire, **{f'{date_field}__date__gte': first_day_of_month, f'{date_field}__date__lte': last_day_of_month})
        .values(f'{date_field}__date')
        .annotate(total_amount=Sum('amount') if model == Achat else Count('id'))
        .order_by(f'{date_field}__date')
    )

    labels = [data[f'{date_field}__date'].strftime('%Y-%m-%d') for data in daily_data]
    data = [data['total_amount'] for data in daily_data]
    
    return labels, data



# def get_daily_totals(model, partenaire, start_date, end_date):
#     date_field = 'date_added' if model == Achat else 'date_visited'
#     daily_data = (
#         model.objects
#         .filter(partenaire=partenaire, **{f'{date_field}__date__gte': start_date, f'{date_field}__date__lte': end_date})
#         .values(f'{date_field}__date')
#         .annotate(total_amount=Sum('amount') if model == Achat else Count('id'))
#         .order_by(f'{date_field}__date')
#     )

#     labels = [data[f'{date_field}__date'].strftime('%Y-%m-%d') for data in daily_data]
#     data = [data['total_amount'] for data in daily_data]

    # return labels, data
 
    
@login_required(login_url='login')  
@user_passes_test(is_partner, login_url='login')
@allowedUsers(allowedGroups=['partenaire'])   
def escpasPartenaire(request):
    partenaire = Partenaire.objects.filter(user=request.user).first()
    if not partenaire:
        return redirect('/')
    
    partenaire_id = partenaire.id   # Fetch partenaire_id after retrieving partenaire object
    
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    

    total_achat_today = get_total_achat_today(partenaire, today)
    total_achat = partenaire.Achat if partenaire else 0
    total_achat_month = get_total_achat_month(partenaire, today)
    total_visite_month = get_total_visite_month(partenaire, today)
    total_visits_today = Visite.objects.filter(partenaire=partenaire, date_visited__date=today).count()
    total_visits = Visite.objects.filter(partenaire=partenaire).count()
    
    # labels, data = get_daily_totals(Achat, partenaire, thirty_days_ago, today)
    labels, data = get_daily_totals(Achat, partenaire, today)

    # visit_labels, visit_data = get_daily_totals(Visite, partenaire, thirty_days_ago, today)
    visit_labels, visit_data = get_daily_totals(Visite, partenaire, today)

    return render(request, 'takouine/escpasPartenaire/escpasPartenaire.html', {
        'total_achat': total_achat,
        'total_achat_today': total_achat_today,
        'total_visits_today': total_visits_today,
        'total_visits': total_visits,
        'total_achat_month': total_achat_month,
        'total_visite_month': total_visite_month,
        'labels': labels,
        'data': data,
        'visit_labels': visit_labels,
        'visit_data': visit_data,
        'partenaire': partenaire,
        'partenaire_id': partenaire_id,
    })


@login_required(login_url='login')  
@user_passes_test(is_partner, login_url='login')
@allowedUsers(allowedGroups=['partenaire'])  
def escpasPartenaireStagiaire(request):
    partenaire_id = request.user.partenaire.id
    partenaire = Partenaire.objects.filter(user=request.user).first()
    if not partenaire:
        return redirect('/')
    
    partenaire_id = partenaire.id
    
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)

    total_achat_today = get_total_achat_today(partenaire, today)
    total_achat = partenaire.Achat if partenaire else 0
    total_achat_month = get_total_achat_month(partenaire, today)
    total_visite_month = get_total_visite_month(partenaire, today)
    total_visits_today = Visite.objects.filter(partenaire=partenaire, date_visited__date=today).count()
    total_visits = Visite.objects.filter(partenaire=partenaire).count()
    
    return render(request, "takouine/escpasPartenaire/escpasPartenaireStagiaire.html",
        {'total_achat': total_achat,
        'total_achat_today': total_achat_today,
        'total_visits_today': total_visits_today,
        'total_visits': total_visits,
        'total_achat_month': total_achat_month,
        'total_visite_month': total_visite_month,
        'partenaire_id': partenaire_id,
        'partenaire': partenaire,
        })


@login_required(login_url='login')  
@user_passes_test(is_partner, login_url='login')
@allowedUsers(allowedGroups=['partenaire']) 
def search_stagiaire(request):
    # partenaire_id = request.user.partenaire.id
    partenaire = Partenaire.objects.filter(user=request.user).first()
    if not partenaire:
        return redirect('/')
    
    today = timezone.now().date()

    total_achat_today = get_total_achat_today(partenaire, today)
    total_achat = partenaire.Achat if partenaire else 0
    total_achat_month = get_total_achat_month(partenaire, today)
    total_visite_month = get_total_visite_month(partenaire, today)
    total_visits_today = Visite.objects.filter(partenaire=partenaire, date_visited__date=today).count()
    total_visits = Visite.objects.filter(partenaire=partenaire).count()
    
    if request.method == 'POST':
        stagiaire_code = request.POST.get('stagiaire_code')
        try:
            stagiaire = Stagiaire.objects.get(stagiaireCode=stagiaire_code)
            stagiaire_info = {
                'id': stagiaire.user.stagiaire.id,
                'name': stagiaire.name,
                'formations': stagiaire.formations,
                'date_fin': stagiaire.date_fin,
                'avatar_url': stagiaire.avatar.url if stagiaire.avatar else None,
                'slugStagiaire': stagiaire.slugStagiaire,
            }
            # Check if the logged-in user is a Partenaire
            if hasattr(request.user, 'partenaire'):
                partenaire = request.user.partenaire
            else:
                partenaire = None
            return render(request, 'takouine/escpasPartenaire/escpasPartenaireStagiaire.html',
        {
        'stagiaire_info': stagiaire_info, 
        'partenaire': partenaire, 
        'total_achat': total_achat,
        'total_achat_today': total_achat_today,
        'total_visits_today': total_visits_today,
        'total_visits': total_visits,
        'total_achat_month': total_achat_month,
        'total_visite_month': total_visite_month,
        })
        except Stagiaire.DoesNotExist:
            error = 'Stagiaire not found'
            return render(request, 'takouine/escpasPartenaire/escpasPartenaireStagiaire.html', {'error': error,'partenaire': partenaire, 
        'total_achat': total_achat,
        'total_achat_today': total_achat_today,
        'total_visits_today': total_visits_today,
        'total_visits': total_visits,
        'total_achat_month': total_achat_month,
        'total_visite_month': total_visite_month,})
    else:
        return render(request, 'takouine/escpasPartenaire/escpasPartenaireStagiaire.html')


# @login_required(login_url='login')  
# @user_passes_test(is_partner, login_url='login')
# @allowedUsers(allowedGroups=['partenaire']) 
# def view_stagiaire(request, stagiaire_id):
#     stagiaire = get_object_or_404(Stagiaire, pk=stagiaire_id)
#     return render(request, 'takouine/escpasPartenaire/showDataStagiaire.html', {'stagiaire': stagiaire})



@login_required(login_url='login')
@user_passes_test(is_partner, login_url='login')
@allowedUsers(allowedGroups=['partenaire']) 
def view_stagiaire(request, slugStagiaire):
    if request.user.is_authenticated:
        is_partenaire = request.user.groups.filter(name='partenaire').exists()
    else:
        is_partenaire= False
        
    partenaire = Partenaire.objects.filter(user=request.user).first()
    if not partenaire:
        return redirect('/')
    
    stagiaire = get_object_or_404(Stagiaire, slugStagiaire=slugStagiaire)
    return render(request, 'takouine/escpasPartenaire/showDataStagiaire.html', {'stagiaire': stagiaire,"is_partenaire": is_partenaire})



@login_required(login_url='login')  
@user_passes_test(is_partner, login_url='login')
@allowedUsers(allowedGroups=['partenaire']) 
def increment_achat(request, slugPartenaire, slugStagiaire):
    partenaire = Partenaire.objects.filter(user=request.user, slugPartenaire=slugPartenaire).first()
    if not partenaire:
        return redirect('/') 
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            partenaire = Partenaire.objects.get(slugPartenaire=slugPartenaire)
            stagiaire = Stagiaire.objects.get(slugStagiaire=slugStagiaire) 
            # Check if the attribute exists in the Partenaire model
            if hasattr(partenaire, 'Achat'):
                partenaire.Achat += int(amount)
                partenaire.save()
                messages.success(request, f"Achat of {amount} added successfully.")
                # Create an Achat object with both Partenaire and Stagiaire
                Achat.objects.create(partenaire=partenaire, stagiaire=stagiaire, amount=amount)
                return redirect('escpasPartenaireStagiaire')
            else:
                messages.error(request, "Achat attribute doesn't exist in the Partenaire model.")
        except Partenaire.DoesNotExist:
            pass
        except Stagiaire.DoesNotExist:
            pass
    partenaire = get_object_or_404(Partenaire, slugPartenaire=slugPartenaire)
    return render(request, 'takouine/escpasPartenaire/escpasPartenaireStagiaire.html', {'partenaire': partenaire})




@login_required(login_url='login')  
@user_passes_test(is_partner, login_url='login')
@allowedUsers(allowedGroups=['partenaire']) 
def achat_form(request, slugPartenaire, slugStagiaire):
    if request.user.is_authenticated:
        is_partenaire = request.user.groups.filter(name='partenaire').exists()
    else:
        is_partenaire= False
        
    partenaire = Partenaire.objects.filter(user=request.user, slugPartenaire=slugPartenaire).first()
    if not partenaire:
        return redirect('/')

    
    return render(request, 'takouine/escpasPartenaire/achat_form.html', {'slugPartenaire': slugPartenaire, 'slugStagiaire': slugStagiaire,"is_partenaire": is_partenaire})





@login_required(login_url='login')  
@user_passes_test(is_partner, login_url='login')
@allowedUsers(allowedGroups=['partenaire']) 
def increment_visite(request, slugPartenaire, slugStagiaire):
    partenaire = Partenaire.objects.filter(user=request.user, slugPartenaire=slugPartenaire).first()
    if not partenaire:
        return redirect('/')
    try:
        partenaire = Partenaire.objects.get(slugPartenaire=slugPartenaire)
        stagiaire = Stagiaire.objects.get(slugStagiaire=slugStagiaire)
        # Create a new visit entry with the partenaire and stagiaire
        Visite.objects.create(partenaire=partenaire, stagiaire=stagiaire)
        messages.success(request, f"Visit added successfully for {partenaire.CompanyName}")
        return redirect(reverse('escpasPartenaireStagiaire') + f'?partenaire_id={slugPartenaire}')
    except (Partenaire.DoesNotExist, Stagiaire.DoesNotExist):
        messages.error(request, "Partenaire or Stagiaire does not exist.")
        return redirect('/')  # Redirect to a different page or handle the error as needed


from django.utils import timezone

@login_required(login_url='login')  
@user_passes_test(is_partner, login_url='login')
@allowedUsers(allowedGroups=['partenaire'])  
def rapportsPartenaire(request):
    partenaire = Partenaire.objects.filter(user=request.user).first()
    if not partenaire:
        return redirect('/')
    
    partenaire_id = partenaire.id
    
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)

    total_achat_today = get_total_achat_today(partenaire, today)
    total_achat = partenaire.Achat if partenaire else 0
    total_achat_month = get_total_achat_month(partenaire, today)
    total_visite_month = get_total_visite_month(partenaire, today)
    
    total_visits_today = Visite.objects.filter(partenaire=partenaire, date_visited__date=today).count()
    total_visits = Visite.objects.filter(partenaire=partenaire).count()
    
    thirty_days_ago = today - timedelta(days=30)
    achats_last_30_days = Achat.objects.filter(partenaire=partenaire, date_added__gte=thirty_days_ago).order_by('-date_added')[:10]
    
    achats_all = Achat.objects.filter(partenaire=partenaire).order_by('-date_added')[:15]
    visite_all = Visite.objects.filter(partenaire=partenaire).order_by('-date_visited')[:15]
    
    return render(request, 'takouine/escpasPartenaire/rapportsPartenaire.html', {
        'achats_last_30_days': achats_last_30_days,
        'total_achat': total_achat,
        'total_achat_today': total_achat_today,
        'total_visits_today': total_visits_today,
        'total_visits': total_visits,
        'total_achat_month': total_achat_month,
        'total_visite_month': total_visite_month,
        'achats_all': achats_all,
        'visite_all': visite_all,
        'partenaire_id': partenaire_id,
        'partenaire': partenaire,
    })






def generate_pdf(request):
    # Extract data from the database
    context = {'achats_all': Achat.objects.all()}
    
    # Render the HTML template to a string
    html = render_to_string('takouine/escpasPartenaire/pdf_template.html', context)

    # Create a bytes buffer for the PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Create styles
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    header_style = styles['Heading2']
    
    # Start with the header
    elements = []
    elements.append(Paragraph('ALL Achat Operations', header_style))
    
    # Create table data
    table_data = []
    table_data.append(['Partenaire', 'Stagiaire', 'Amount', 'Date Added'])
    
    for achat in context['achats_all']:
        table_data.append([
            achat.partenaire.CompanyName,
            achat.stagiaire.stagiaireCode if achat.stagiaire else 'None',
            f'{achat.amount} MAD',
            achat.date_added.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    # Create a table and style it
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#f2f2f2'),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONT', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 1), (-1, -1), '#ffffff'),
    ]))
    
    elements.append(table)
    
    # Build the PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="achats_all.pdf"'
    return response




@login_required(login_url='login')
@user_passes_test(is_partner, login_url='login')
@allowedUsers(allowedGroups=['partenaire'])
def generate_visite_pdf(request):
    partenaire = request.user.partenaire
    visite_all = Visite.objects.filter(partenaire=partenaire).order_by('-date_visited')
    context = {'visite_all': visite_all}
    
    # Render the HTML template to a string
    html = render_to_string('takouine/escpasPartenaire/pdf_template_visite.html', context)
    
    # Create a bytes buffer for the PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Create styles
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    header_style = styles['Heading2']
    
    # Start with the header
    elements = []
    elements.append(Paragraph('ALL Visite Operations', header_style))
    
    # Create table data
    table_data = []
    table_data.append(['Partenaire', 'Stagiaire', 'Date Visited'])
    
    for visite in context['visite_all']:
        table_data.append([
            visite.partenaire.CompanyName,
            visite.stagiaire.stagiaireCode if visite.stagiaire else 'None',
            visite.date_visited.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    # Create a table and style it
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#f2f2f2'),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONT', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 1), (-1, -1), '#ffffff'),
    ]))
    
    elements.append(table)
    
    # Build the PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="visite_all.pdf"'
    return response





import datetime
from datetime import timedelta
from django.utils import timezone

@login_required(login_url='login')  
@user_passes_test(is_partner, login_url='login')
@allowedUsers(allowedGroups=['partenaire']) 
def filter_achats(request):
    partenaire = Partenaire.objects.filter(user=request.user).first()
    if not partenaire:
        return redirect('/')
    
    today = timezone.now().date()

    total_achat_today = get_total_achat_today(partenaire, today)
    total_achat = partenaire.Achat if partenaire else 0
    total_achat_month = get_total_achat_month(partenaire, today)
    total_visite_month = get_total_visite_month(partenaire, today)
    
    total_visits_today = Visite.objects.filter(partenaire=partenaire, date_visited__date=today).count()
    total_visits = Visite.objects.filter(partenaire=partenaire).count()
    
    amount = request.GET.get('amount')
    stagiaire_code = request.GET.get('stagiaireCode')
    start_date = request.GET.get('start_date')

    # Prepare the filter parameters
    filter_params = {}

    if amount:
        filter_params['amount'] = amount

    if stagiaire_code:
        filter_params['stagiaire__stagiaireCode'] = stagiaire_code
        
    if start_date:
        # Convert string date to datetime object
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

        # Add start date filter
        filter_params['date_added__date'] = start_date


    visite_all = Visite.objects.filter(partenaire=partenaire).order_by('-date_visited')[:15]

    # Apply filters
    achats_all = Achat.objects.filter(partenaire=partenaire, **filter_params).order_by('-date_added')[:15]

    return render(request, 'takouine/escpasPartenaire/rapportsPartenaire.html', {
        'total_achat': total_achat,
        'total_achat_today': total_achat_today,
        'total_visits_today': total_visits_today,
        'total_visits': total_visits,
        'total_achat_month': total_achat_month,
        'total_visite_month': total_visite_month,
        'achats_all': achats_all,
        'visite_all': visite_all,
        'partenaire':partenaire,
    })



@login_required(login_url='login')  
@user_passes_test(is_partner, login_url='login')
@allowedUsers(allowedGroups=['partenaire']) 
def filter_visite(request):
    partenaire = Partenaire.objects.filter(user=request.user).first()
    if not partenaire:
        return redirect('/')
    
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)

    total_achat_today = get_total_achat_today(partenaire, today)
    total_achat = partenaire.Achat if partenaire else 0
    total_achat_month = get_total_achat_month(partenaire, today)
    total_visite_month = get_total_visite_month(partenaire, today)
    
    total_visits_today = Visite.objects.filter(partenaire=partenaire, date_visited__date=today).count()
    total_visits = Visite.objects.filter(partenaire=partenaire).count()
    
    achats_all = Achat.objects.filter(partenaire=partenaire).order_by('-date_added')[:15]
    
    visites_last_30_days = Visite.objects.filter(partenaire=partenaire, date_visited__gte=thirty_days_ago).order_by('-date_visited')[:10]
    
   # Filter
    stagiaire_code = request.GET.get('stagiaireCode')
    start_date = request.GET.get('start_date')

    # Prepare the filter parameters
    filter_params = {}

    if stagiaire_code:
        filter_params['stagiaire__stagiaireCode'] = stagiaire_code

    if start_date:
        # Convert string date to datetime object
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

        # Add start date filter
        filter_params['date_visited__date'] = start_date
        
    # Apply filters
    visite_all = Visite.objects.filter(partenaire=partenaire, **filter_params).order_by('-date_visited')[:15]
    
    return render(request, 'takouine/escpasPartenaire/rapportsPartenaire.html', {
        'total_achat': total_achat,
        'total_achat_today': total_achat_today,
        'total_visits_today': total_visits_today,
        'total_visits': total_visits,
        'total_achat_month': total_achat_month,
        'total_visite_month': total_visite_month,
        'visites_last_30_days': visites_last_30_days,
        'achats_all': achats_all,
        'visite_all': visite_all,
        'partenaire':partenaire,
    })



from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required(login_url='login')  
@user_passes_test(is_partner, login_url='login')
@allowedUsers(allowedGroups=['partenaire']) 
def clear_filters_achats(request):
    redirect_url = reverse('filter_achats')
    response = redirect(redirect_url)
    response = redirect('rapportsPartenaire')
    return response
    
    
@login_required(login_url='login')  
@user_passes_test(is_partner, login_url='login')
@allowedUsers(allowedGroups=['partenaire']) 
def clear_filters_visite(request):
    redirect_url = reverse('filter_visite')
    response = redirect(redirect_url)
    response = redirect('rapportsPartenaire')
    return response



from .forms import PartenaireMoreForm
from django.shortcuts import get_object_or_404

def add_More_partenaire(request, slugPartenaire):
    partenaire = get_object_or_404(Partenaire, slugPartenaire=slugPartenaire)
    if partenaire.user != request.user:
        return redirect('/')
    
    if request.method == 'POST':
        form = PartenaireMoreForm(request.POST, request.FILES, instance=partenaire)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informations Updated successfully!')
            # Redirect to the partenaire's detail page after updating the partenaire
            return redirect(reverse('add_More_partenaire', kwargs={'slugPartenaire': slugPartenaire}))
    else:
        form = PartenaireMoreForm(instance=partenaire)
    
    return render(request, 'takouine/escpasPartenaire/add_partenaire_description.html', {'form': form, 'partenaire': partenaire})





def is_stagiaire(user):
    return user.groups.filter(name='stagiaire').exists()

def get_total_achat_today_stagiaire(stagiaire, today):
    total_achat_today = Achat.objects.filter(stagiaire=stagiaire, date_added__date=today).aggregate(total_achat_today=Sum('amount'))['total_achat_today']
    return total_achat_today or 0

def get_total_achat_month_stagiaire(stagiaire, today):
    first_day_of_month = today.replace(day=1)
    thirtieth_day_of_month = first_day_of_month + timedelta(days=29)
    total_achat_month = Achat.objects.filter(stagiaire=stagiaire, date_added__gte=first_day_of_month, date_added__lte=thirtieth_day_of_month).aggregate(total_achat_month=Sum('amount'))['total_achat_month']
    return total_achat_month or 0

def get_total_visite_month_stagiaire(stagiaire, today):
    first_day_of_month = today.replace(day=1)
    thirtieth_day_of_month = first_day_of_month + timedelta(days=29)
    total_visite_month = Visite.objects.filter(stagiaire=stagiaire, date_visited__gte=first_day_of_month, date_visited__lte=thirtieth_day_of_month).count()
    return total_visite_month


#escpasStagiaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['stagiaire']) 
def escpasStagiairer(request):
    stagiaire = Stagiaire.objects.get(user=request.user)
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)

    total_achat = Achat.objects.filter(stagiaire=stagiaire).aggregate(Sum('amount'))['amount__sum'] or 0
    total_visits = Visite.objects.filter(stagiaire=stagiaire).count()
    total_achat_today = get_total_achat_today_stagiaire(stagiaire, today)
    total_achat_month = get_total_achat_month_stagiaire(stagiaire, today)
    total_visite_month = get_total_visite_month_stagiaire(stagiaire, today)
    total_visits_today = Visite.objects.filter(stagiaire=stagiaire, date_visited__date=today).count()

    context = {'stagiaire': stagiaire,'total_achat':total_achat,'total_visits':total_visits,'total_achat_month':total_achat_month,'total_visite_month':total_visite_month} 
    return render(request, "takouine/escpasStagiairer/escpasStagiairer.html", context)





#escpasEdituerPartenaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['stagiaire'])    
def escpasStagiairePartenaire(request):
    stagiaire = Stagiaire.objects.get(user=request.user)
    partenaires = User.objects.filter(groups__name='partenaire')
    partenaire_categories = Partenaire.CATEGORY_CHOICES
    
    context = {'partenaires': partenaires,'stagiaire': stagiaire,'partenaire_categories': partenaire_categories} 
    
    return render(request, "takouine/escpasStagiairer/escpasStagiairePartenaire.html", context)


# login_required(login_url='login')  
# @allowedUsers(allowedGroups=['stagiaire']) 
# def view_partenaire(request, partenaire_id):
#     partenaire = get_object_or_404(Partenaire, pk=partenaire_id)
#     stagiaire = Stagiaire.objects.get(user=request.user)
#     context = {'partenaire': partenaire,'stagiaire': stagiaire}
#     return render(request, 'takouine/escpasStagiairer/showDataPartenaire.html', context)



@login_required(login_url='login')  
@allowedUsers(allowedGroups=['stagiaire']) 
def view_partenaire(request, slugPartenaire):
    partenaire = get_object_or_404(Partenaire, slugPartenaire=slugPartenaire)
    stagiaire = Stagiaire.objects.get(user=request.user)
    context = {'partenaire': partenaire, 'stagiaire': stagiaire}
    return render(request, 'takouine/escpasStagiairer/showDataPartenaire.html', context)


@login_required(login_url='login')  
@allowedUsers(allowedGroups=['stagiaire']) 
def filter_partenaire(request):
    stagiaire = Stagiaire.objects.get(user=request.user)
    
    partenaire_categories = Partenaire.CATEGORY_CHOICES
    
    category = request.GET.get('category')

    filter_params = {}

    if category:
        filter_params['category'] = category

    filter_partenaires = Partenaire.objects.filter(**filter_params)
    
    return render(request, 'takouine/escpasStagiairer/escpasStagiairePartenaire.html', {'filter_partenaires': filter_partenaires, 'partenaire_categories': partenaire_categories,'stagiaire':stagiaire})






from .forms import StagiaireMoreForm
@allowedUsers(allowedGroups=['stagiaire']) 
def add_More_Stagiaire(request, slugStagiaire):
    stagiaire = get_object_or_404(Stagiaire, slugStagiaire=slugStagiaire)
    
    if stagiaire.user != request.user:
        return redirect('/')
    
    if request.method == 'POST':
        form_stagiaire = StagiaireMoreForm(request.POST, request.FILES, instance=stagiaire)
        if form_stagiaire.is_valid():
            form_stagiaire.save()
            messages.success(request, 'Informations Updated successfully!')
            return redirect(reverse('add_More_Stagiaire', kwargs={'slugStagiaire': stagiaire.slugStagiaire}))
    else:
        form_stagiaire = StagiaireMoreForm(instance=stagiaire)
    
    return render(request, 'takouine/escpasStagiairer/add_stagiaire_description.html', {'form_stagiaire': form_stagiaire, 'slugStagiaire': slugStagiaire, 'stagiaire': stagiaire})





from django.shortcuts import render, redirect
from .forms import ContactFormPartenaire


def douvientpartenaire(request):
    if request.method == 'POST':
        form = ContactFormPartenaire(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')  # Add success message

            return redirect('/')  # Redirect to a success page
    else:
        form = ContactFormPartenaire()
    return render(request, 'takouine/Douvientpartenaire.html', {'form': form})



#escpasAdminMessagePartenaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])   
def escpasAdminMessagePartenaire(request):
    MessagePartenaires = ContactMessagePartenaire.objects.all()
    
    edituers = User.objects.filter(groups__name='Edituer')
    stagiaires = User.objects.filter(groups__name='stagiaire')
    partenaires = User.objects.filter(groups__name='partenaire')
    
    total_edituers = User.objects.filter(groups__name='Edituer').count()
    total_admins = User.objects.filter(groups__name='admin').count()
    total_stagiaires = User.objects.filter(groups__name='stagiaire').count()
    total_partenaires = User.objects.filter(groups__name='partenaire').count()
    
    return render(request, 'takouine/escpasAdminMessagePartenaire/escpasAdminMessagePartenaire.html', {'MessagePartenaires': MessagePartenaires,'edituers': edituers,'stagiaires': stagiaires ,'total_edituers': total_edituers,'total_admins': total_admins,'total_stagiaires': total_stagiaires,'partenaires': partenaires,'total_partenaires':total_partenaires})





#escpasEdituerMessagePartenaire
@login_required(login_url='login')
@allowedUsers(allowedGroups=['Edituer']) 
def escpasEdituerMessagePartenaire(request):
    MessagePartenaires = ContactMessagePartenaire.objects.all()
    
    edituers = User.objects.filter(groups__name='Edituer')
    stagiaires = User.objects.filter(groups__name='stagiaire')
    partenaires = User.objects.filter(groups__name='partenaire')
    
    total_edituers = User.objects.filter(groups__name='Edituer').count()
    total_admins = User.objects.filter(groups__name='admin').count()
    total_stagiaires = User.objects.filter(groups__name='stagiaire').count()
    total_partenaires = User.objects.filter(groups__name='partenaire').count()
    
    return render(request, 'takouine/escpasEdituerMessagePartenaire/escpasEdituerMessagePartenaire.html', {'MessagePartenaires': MessagePartenaires,'edituers': edituers,'stagiaires': stagiaires ,'total_edituers': total_edituers,'total_admins': total_admins,'total_stagiaires': total_stagiaires,'partenaires': partenaires,'total_partenaires':total_partenaires})





def helpsPartenaire(request):
    if request.user.is_authenticated:
        is_edituer = request.user.groups.filter(name='Edituer').exists()
        is_stagiaire = request.user.groups.filter(name='stagiaire').exists()
        is_partenaire = request.user.groups.filter(name='partenaire').exists()
    else:
        is_edituer = False
        is_stagiaire = False   
        is_partenaire= False
    
    context = {"is_edituer": is_edituer,"is_stagiaire": is_stagiaire,"is_partenaire": is_partenaire}

        
    return render(request, 'takouine/helpsPartenaire.html',context)




def EscapePartenaireLogin(request):
    if request.user.is_authenticated:
        # Check if the user belongs to the group "Edituer" and "Stagiaire"
        is_edituer = request.user.groups.filter(name='Edituer').exists()
        is_stagiaire = request.user.groups.filter(name='stagiaire').exists()
        is_partenaire = request.user.groups.filter(name='partenaire').exists()
    else:
        is_edituer = False
        is_stagiaire = False   
        is_partenaire= False     
    context = {"is_edituer": is_edituer,"is_stagiaire": is_stagiaire,"is_partenaire": is_partenaire}
    
    return render(request, 'takouine/PartenaireLoginHome/EscapePartenaireLogin.html',context)



def EscapePartenairehome(request):
    if request.user.is_authenticated:
        # Check if the user belongs to the group "Edituer" and "Stagiaire"
        is_edituer = request.user.groups.filter(name='Edituer').exists()
        is_stagiaire = request.user.groups.filter(name='stagiaire').exists()
        is_partenaire = request.user.groups.filter(name='partenaire').exists()
    else:
        is_edituer = False
        is_stagiaire = False   
        is_partenaire= False     
        
    context = {"is_edituer": is_edituer,"is_stagiaire": is_stagiaire,"is_partenaire": is_partenaire}
    
    
    return render(request, 'takouine/PartenaireLoginHome/EscapePartenairehome.html',context)



def EscapeStagiaireLogin(request):
    if request.user.is_authenticated:
        # Check if the user belongs to the group "Edituer" and "Stagiaire"
        is_edituer = request.user.groups.filter(name='Edituer').exists()
        is_stagiaire = request.user.groups.filter(name='stagiaire').exists()
        is_partenaire = request.user.groups.filter(name='partenaire').exists()
    else:
        is_edituer = False
        is_stagiaire = False   
        is_partenaire= False     
        
    context = {"is_edituer": is_edituer,"is_stagiaire": is_stagiaire,"is_partenaire": is_partenaire}
    
    
    return render(request, 'takouine/StagiaireLoginHome/EscapeStagiaireLogin.html',context)

