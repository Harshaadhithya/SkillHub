from django.forms import ModelForm, fields, models, widgets
from .models import Project, Review

from django import forms

class ProjectFrom(ModelForm):
    class Meta:
        model=Project
        fields=['title','featured_image','description','demo_link','source_link',]

        widgets={
            'tags':forms.CheckboxSelectMultiple()
            }
    def __init__(self,*args,**kwargs):
        super(ProjectFrom,self).__init__(*args,**kwargs)
        self.fields['title'].widget.attrs.update({'class':'input input--text'})
        self.fields['featured_image'].widget.attrs.update({'class':'input'})
        self.fields['description'].widget.attrs.update({'class':'input input--text'})
        self.fields['demo_link'].widget.attrs.update({'class':'input input--text'})
        self.fields['source_link'].widget.attrs.update({'class':'input input--text'})


class Review_form(ModelForm):
    class Meta:
        model=Review
        fields=['value','body']

        labels={'value':'Place your Vote','body':'Add a comment'}

    def __init__(self,*args,**kwargs):
        super(Review_form,self).__init__(*args,**kwargs)
        self.fields['value'].widget.attrs.update({'class':'input'})
        self.fields['body'].widget.attrs.update({'class':'input','id':'formInput#textarea'})
        

        

        