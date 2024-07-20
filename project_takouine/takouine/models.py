from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.translation import gettext_lazy as _ 
from django.utils.text import slugify


class Edituer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    age = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    slugEdituer = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slugEdituer:
            self.slugEdituer = slugify(self.user.username) #slugify(self.user.username) 
        super().save(*args, **kwargs)
  
        
    def __str__(self):
        return self.name



from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def user_save(sender, instance, created, **kwargs):
    try:
        edituer = instance.edituer
        if edituer.slugEdituer != slugify(instance.username):
            edituer.slugEdituer = slugify(instance.username)
            edituer.save()
    except Edituer.DoesNotExist:
        pass



def generate_stagiaire_code():
    prefix = "KT"
    unique_id = uuid.uuid4().hex[:8]  # Generate a unique ID
    return prefix + unique_id




class Formation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    slugFormation = models.SlugField(blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slugFormation:
            self.slugFormation = slugify(self.name) 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



   
#update_formation_slug   
@receiver(post_save, sender=Formation)
def update_formation_slug(sender, instance, created, **kwargs):
    if created or instance.name != instance.slugFormation:
        instance.slugFormation = slugify(instance.name)
        Formation.objects.filter(pk=instance.pk).update(slugFormation=instance.slugFormation)
        

    




class Stagiaire(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    age = models.CharField(max_length=100, null=True)
    avatar = models.ImageField(null=True)
    formations = models.ManyToManyField(Formation)  # Many-to-many relationship with Formation
    date_debut = models.DateTimeField(null=True)
    date_fin = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    stagiaireCode = models.CharField(max_length=100, null=True, default=generate_stagiaire_code)
    
    
    slugStagiaire = models.SlugField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slugStagiaire:
            self.slugStagiaire = slugify(self.name)
        super(Stagiaire, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    
    
#update_stagiaire_slug   
@receiver(post_save, sender=User)
def update_stagiaire_slug(sender, instance, created, **kwargs):
        try:
            stagiaire = instance.stagiaire
            if stagiaire.slugStagiaire != slugify(instance.username):
                stagiaire.slugStagiaire = slugify(instance.username)
                stagiaire.save()
        except Stagiaire.DoesNotExist:
            pass
        


# Function to generate a random company code
def generate_company_code():
    return str(uuid.uuid4().hex)[:10]




class Partenaire(models.Model):
    CATEGORY_CHOICES = [
        ('Telephone et tablette', 'Telephone et tablette'),
        ('Electromenager', 'Electromenager'),
        ('Informatique', 'Informatique'),
        ('Maison et cuisine', 'Maison et cuisine'),
        ('Bureau', 'Bureau'),
        ('Vetements et chaussures', 'Vetements et chaussures'),
        ('Beautes et sante', 'Beautes et sante'),
        ('Jeux Videos et consoles', 'Jeux Videos et consoles'),
        ('Sport et Loisirs', 'Sport et Loisirs'),
        ('Bebe et Jouets', 'Bebe et Jouets'),
        ('Supermarche', 'Supermarche'),
        ('Librairies', 'Librairies'),
        ('Services', 'Services'),
    ]
    
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    CompanyName = models.CharField(max_length=100, null=True, unique=True) #If have a problem in id == slug add , unique=True
    CompanyPhone = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    CompanyCode = models.CharField(max_length=100, null=True, default=generate_company_code)
    Achat = models.IntegerField(default=0)
    Visite = models.IntegerField(default=0)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True)
    Companyemail = models.EmailField(null=True, blank=True)
    logo = models.ImageField( null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    photo1 = models.ImageField(null=True, blank=True)
    photo2 = models.ImageField(null=True, blank=True)
    photo3 = models.ImageField(null=True, blank=True)
    photo4 = models.ImageField(null=True, blank=True)
    photo5 = models.ImageField(null=True, blank=True)
    
    slugPartenaire = models.SlugField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slugPartenaire:
            self.slugPartenaire = slugify(self.CompanyName)
        super(Partenaire, self).save(*args, **kwargs)


    def __str__(self):
        return self.CompanyName

  
  
#update_partenaire_slug   
@receiver(post_save, sender=User)
def update_partenaire_slug(sender, instance, created, **kwargs):
        try:
            partenaire = instance.partenaire
            if partenaire.slugPartenaire != slugify(instance.username):
                partenaire.slugPartenaire = slugify(instance.username)
                partenaire.save()
        except Partenaire.DoesNotExist:
            pass
  


    
class Achat(models.Model):
    partenaire = models.ForeignKey(Partenaire, on_delete=models.CASCADE)
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        stagiaire_code = self.stagiaire.stagiaireCode if self.stagiaire else 'None'
        return f"{self.partenaire.CompanyName} - {self.amount} - {self.date_added} - {stagiaire_code}"


   
   
       
class Visite(models.Model):
    partenaire = models.ForeignKey(Partenaire, on_delete=models.CASCADE)
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.SET_NULL, null=True)
    date_visited = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = _("Visite")
        verbose_name_plural = _("Visites")

    def __str__(self):
        stagiaire_code = self.stagiaire.stagiaireCode if self.stagiaire else 'None'
        return f"{self.partenaire.CompanyName} - {self.date_visited} - {stagiaire_code}"




class ContactMessagePartenaire(models.Model):
    CATEGORY_CHOICES = [
        ('Telephone et tablette', 'Telephone et tablette'),
        ('Electromenager', 'Electromenager'),
        ('Informatique', 'Informatique'),
        ('Maison et cuisine', 'Maison et cuisine'),
        ('Bureau', 'Bureau'),
        ('Vetements et chaussures', 'Vetements et chaussures'),
        ('Beautes et sante', 'Beautes et sante'),
        ('Jeux Videos et consoles', 'Jeux Videos et consoles'),
        ('Sport et Loisirs', 'Sport et Loisirs'),
        ('Bebe et Jouets', 'Bebe et Jouets'),
        ('Supermarche', 'Supermarche'),
        ('Librairies', 'Librairies'),
        ('Services', 'Services'),
    ]
    Companyname = models.CharField(max_length=100)
    email = models.EmailField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True)
    CompanyPhone = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Companyname
