from django.db import models
from django.contrib.auth.models import User

class Kafedra(models.Model):

    name = models.CharField(max_length=200, help_text=" ")
    
    
    def __str__(self):

        return self.name

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Mamandyk(models.Model):

    title = models.CharField(max_length=200)
    mugalim = models.ForeignKey('Mugalim', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text=' ')
    isbn = models.CharField('ISBN',max_length=15, help_text=' ')
    kafedra = models.ManyToManyField(Kafedra, help_text=' ')

    
   
    def display_genre(self):

        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
	
    display_genre.short_description = 'Kafedra'
    
    def __str__(self):

        return self.title
		
    def get_absolute_url(self):

        return reverse('book-detail', args=[str(self.id)])

import uuid

class Kurs(models.Model):

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=" ")
    book = models.ForeignKey('Mamandyk', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('1', 'bir'),
        ('2', 'eki'),
        ('3', 'ush'),
        ('4', 'tort'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text=' ')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)
        

    def __str__(self):

        return '{0} ({1})'.format(self.id,self.book.title)

class Mugalim(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ["last_name","first_name"]
    
    def get_absolute_url(self):

        return reverse('author-detail', args=[str(self.id)])
    

    def __str__(self):

        return '{0}, {1}'.format(self.last_name,self.first_name)
   