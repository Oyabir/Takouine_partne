from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.Partenairelogin, name="Partenairelogin"), 
    path('register/',views.register, name="register"),
    
    path('Partenairelogin/',views.Partenairelogin, name="Partenairelogin"),
    path('Stagiairelogin/',views.Stagiairelogin, name="Stagiairelogin"),
   
    path('logout/',views.userLogout, name="logout"),
    path('login/', views.Partenairelogin, name="login"),
    
    
    path('escpasAdmin/',views.escpasAdmin, name="escpasAdmin"),
    path('registerEdituer/',views.registerEdituer, name="registerEdituer"),
    path('update_edituer/<slug:slugEdituer>',views.update_edituer, name="update_edituer"),
    path('change_password/<slug:slugEdituer>/', views.change_password, name='change_password'),
    path('delete_edituer/<slug:slugEdituer>/', views.delete_edituer, name='delete_edituer'),
    
    path('registerStagiaire/',views.registerStagiaire, name="registerStagiaire"),
    path('escpasAdminStagiaire/',views.escpasAdminStagiaire, name="escpasAdminStagiaire"),
    path('update_stagiaire/<slug:slugStagiaire>',views.update_stagiaire, name="update_stagiaire"),
    path('change_password_stagiaire/<slug:slugStagiaire>/', views.change_password_stagiaire, name='change_password_stagiaire'),
    path('delete_stagiaire/<slug:slugStagiaire>/', views.delete_stagiaire, name='delete_stagiaire'),

    path('registerPartenaire/',views.registerPartenaire, name="registerPartenaire"),
    path('escpasAdminPartenaire/',views.escpasAdminPartenaire, name="escpasAdminPartenaire"),
    path('update_partenaire/<slug:slugPartenaire>',views.update_partenaire, name="update_partenaire"),
    path('delete_partenaire/<slug:slugPartenaire>/', views.delete_partenaire, name='delete_partenaire'),
    path('change_password_partenaire/<slug:slugPartenaire>/', views.change_password_partenaire, name='change_password_partenaire'),



    path('escpasEdituer/',views.escpasEdituer, name="escpasEdituer"),
    path('escpasEdituerPartenaire/',views.escpasEdituerPartenaire, name="escpasEdituerPartenaire"),

    path('escpasPartenaire/',views.escpasPartenaire, name="escpasPartenaire"),
    path('escpasPartenaireStagiaire/',views.escpasPartenaireStagiaire, name="escpasPartenaireStagiaire"),
    path('search_stagiaire/',views.search_stagiaire, name="search_stagiaire"),
    path('view_stagiaire/<slug:slugStagiaire>/', views.view_stagiaire, name='view_stagiaire'),


    path('increment_achat/<slug:slugPartenaire>/<slug:slugStagiaire>/', views.increment_achat, name='increment_achat'),
    path('increment_visite/<int:partenaire_id>/', views.increment_visite, name='increment_visite'),
    path('achat/<slug:slugPartenaire>/<slug:slugStagiaire>/', views.achat_form, name='achat_form'),
    path('increment_visite/<slug:slugPartenaire>/<slug:slugStagiaire>/', views.increment_visite, name='increment_visite'),
    
    path('rapportsPartenaire/', views.rapportsPartenaire, name='rapportsPartenaire'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('generate_pdf_visite/', views.generate_visite_pdf, name='generate_visite_pdf'),
    
    path('add_formationAdmin/', views.add_formationAdmin, name='add_formationAdmin'),
    # path('get_formation/', views.get_formation, name='get_formation'),
    path('update_formation/<slug:slugFormation>/', views.update_formation, name='update_formation'),
    path('delete_formation/<slug:slugFormation>/', views.delete_formation, name='delete_formation'),
    path('escpasAdminFormation/',views.escpasAdminFormation, name="escpasAdminFormation"),

    path('escpasAdminRapports/',views.escpasAdminRapports, name="escpasAdminRapports"),
    path('generate_stagiaires_pdf/', views.generate_stagiaires_pdf, name='generate_stagiaires_pdf'),
    path('generate_partenaires_pdf/', views.generate_partenaires_pdf, name='generate_partenaires_pdf'),

    path('filter_achats/', views.filter_achats, name='filter_achats'),
    path('clear_filters_achats/', views.clear_filters_achats, name='clear_filters_achats'),
    
    path('filter_visite/', views.filter_visite, name='filter_visite'),
    path('clear_filters_visite/', views.clear_filters_visite, name='clear_filters_visite'),

    
    path('add_More_partenaire/<slug:slugPartenaire>/', views.add_More_partenaire, name='add_More_partenaire'),

    path('escpasStagiairer/',views.escpasStagiairer, name="escpasStagiairer"),
    path('escpasStagiairePartenaire/',views.escpasStagiairePartenaire, name="escpasStagiairePartenaire"),

    # path('view_partenaire/<int:partenaire_id>/', views.view_partenaire, name='view_partenaire'),
    path('view_partenaire/<slug:slugPartenaire>/', views.view_partenaire, name='view_partenaire'),

    path('filter_partenaire/', views.filter_partenaire, name='filter_partenaire'),

    path('add_More_Stagiaire/<slug:slugStagiaire>/', views.add_More_Stagiaire, name='add_More_Stagiaire'),

    path('douvientpartenaire/', views.douvientpartenaire, name='douvientpartenaire'),
    
    path('escpasAdminMessagePartenaire/', views.escpasAdminMessagePartenaire, name='escpasAdminMessagePartenaire'),

    path('helpsPartenaire/', views.helpsPartenaire, name='helpsPartenaire'),

    
    path('escpasEdituerFormation/',views.escpasEdituerFormation, name="escpasEdituerFormation"),
    path('add_formationEdituer/', views.add_formationEdituer, name='add_formationEdituer'),
    path('escpasEdituerRapports/',views.escpasEdituerRapports, name="escpasEdituerRapports"),
    path('escpasEdituerMessagePartenaire/', views.escpasEdituerMessagePartenaire, name='escpasEdituerMessagePartenaire'),


    path('EscapePartenaireLogin/', views.EscapePartenaireLogin, name='EscapePartenaireLogin'),
    path('EscapeStagiaireLogin/', views.EscapeStagiaireLogin, name='EscapeStagiaireLogin'),

]   


 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

