from django.http import JsonResponse

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from projects.models import Project,Review,Tag
from .serializers import ProjectSerializer




@api_view(['GET'])
def get_routes(request):
    routes=[
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
    ]
    #return JsonResponse(routes,safe=False)
    return Response(routes)

@api_view(['GET'])

def get_projects(request):
    projects=Project.objects.all()
    serialized_project=ProjectSerializer(projects,many=True).data
    return Response(serialized_project)

@api_view(['GET'])
def get_project(request,pk):
    project=Project.objects.get(id=pk)
    serialized_project=ProjectSerializer(project,many=False)
    return Response(serialized_project.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_vote(request,pk):
    project=Project.objects.get(id=pk)
    user=request.user.profile
    data=request.data
    review,is_created_newly=Review.objects.get_or_create(owner=user,project=project,)

    review.value=data['value']
    review.save()

    project.count_vote
    
    serialized_project=ProjectSerializer(project,many=False)
    
    return Response(serialized_project.data)

@api_view(['DELETE'])
def remove_tag(request):
    tag_id=request.data['tag']
    project_id=request.data['project']
    
    project=Project.objects.get(id=project_id)
    tag=Tag.objects.get(id=tag_id)

    project.tags.remove(tag)
    
    return Response("Tag was deleted")