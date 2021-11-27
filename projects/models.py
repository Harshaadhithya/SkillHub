from django.db import models
import uuid

from users.models import Profile

# Create your models here.
class Project(models.Model):
    owner=models.ForeignKey(Profile,blank=True,null=True,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    featured_image=models.ImageField(null=False,blank=False,default='default.jpg')
    tags=models.ManyToManyField('Tag',blank=True)
    demo_link=models.CharField(max_length=2000,null=True,blank=True)
    source_link=models.CharField(max_length=2000,null=True,blank=True)
    vote_total=models.IntegerField(default=0,blank=True,null=True)
    vote_ratio=models.IntegerField(default=0,blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.title
    class Meta:
        ordering=['-vote_ratio','-vote_total','-created']

    @property
    def count_vote(self):
        all_review_of_current_project=self.review_set.all()
        positive_review_count=all_review_of_current_project.filter(value='up').count()
        total_votes_count=all_review_of_current_project.count()

        vote_ratio=(positive_review_count/total_votes_count)*100

        self.vote_total=total_votes_count
        self.vote_ratio=vote_ratio

        self.save()

class Review(models.Model):
    vote_types=(
        ('up','Up Vote'),
        ('Down','Down Vote')
    )
    owner=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)
    value=models.CharField(max_length=100,choices=vote_types)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    class Meta:
        unique_together=[['owner','project']]

    def __str__(self):
        return self.value

class Tag(models.Model):
    name=models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.name
    


