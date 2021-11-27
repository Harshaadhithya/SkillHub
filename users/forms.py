from django.db import models
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Skill,Messages

class custom_user_creation_form(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','email','username','password1','password2']
        labels={'first_name':'Name'}

    def __init__(self,*args,**kwargs):
        super(custom_user_creation_form,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'input'})
        self.fields['email'].widget.attrs.update({'class':'input'})
        self.fields['username'].widget.attrs.update({'class':'input'})
        self.fields['password1'].widget.attrs.update({'class':'input'})
        self.fields['password2'].widget.attrs.update({'class':'input'})

class edit_account_form(ModelForm):
    class Meta:
        model=Profile
        fields= ['name','email','username','location','short_intro','bio','profile_image',
                 'social_github','social_twitter','social_linkedin','social_youtube','social_website']

    def __init__(self,*args,**kwargs):
        super(edit_account_form,self).__init__(*args,**kwargs)
        self.fields['name'].widget.attrs.update({'class':'input'})
        self.fields['email'].widget.attrs.update({'class':'input'})
        self.fields['username'].widget.attrs.update({'class':'input'})
        self.fields['location'].widget.attrs.update({'class':'input'})
        self.fields['short_intro'].widget.attrs.update({'class':'input'})
        self.fields['bio'].widget.attrs.update({'class':'input'})
        self.fields['profile_image'].widget.attrs.update({'class':'input'})
        self.fields['social_github'].widget.attrs.update({'class':'input'})
        self.fields['social_twitter'].widget.attrs.update({'class':'input'})
        self.fields['social_linkedin'].widget.attrs.update({'class':'input'})
        self.fields['social_youtube'].widget.attrs.update({'class':'input'})
        self.fields['social_website'].widget.attrs.update({'class':'input'})

class skill_form(ModelForm):
    class Meta:
        model=Skill
        fields='__all__'
        exclude=['owner']
        labels={'name':'Skill Name'}

    def __init__(self,*args,**kwargs):
        super(skill_form,self).__init__(*args,**kwargs)
        self.fields['name'].widget.attrs.update({'class':'input'})
        self.fields['description'].widget.attrs.update({'class':'input'})

class message_form(ModelForm):
    class Meta:
        model=Messages
        fields=['subject','body']

    def __init__(self,*args,**kwargs):
        super(message_form,self).__init__(*args,**kwargs)
        self.fields['subject'].widget.attrs.update({'class':'input'})
        self.fields['body'].widget.attrs.update({'class':'input'})

        
