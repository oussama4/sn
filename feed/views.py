from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import DatabaseError, transaction
from django.contrib.contenttypes.models import ContentType
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from .models import Action, Post
from accounts.utils import get_auth_token, get_user_by_token

def index(request):
    if request.user.is_authenticated:
        return render(request, 'feed/index.html')
    else:
        return render(request, 'index.html')

@method_decorator(csrf_exempt, name='dispatch')    
class CreatePsotView(APIView):
    def post(self, request):
        """
        handles a request to post to the news feed
        """
        print('post_actionnnnnnnnnnnnnnnnnnnn')
        
        if (not request.POST['post_text']) and (not request.FILES):
            return JsonResponse({'status': 'empty'})
        t = request.POST['post_text']
        token = get_auth_token(request)
        u = get_user_by_token(token)
        if not request.FILES:
            try:
                with transaction.atomic():
                    p = Post.objects.create(text=t)
                    a = Action(actor=u, verb='post', target_id=p.pk)
                    a.target_ct = ContentType.objects.get_for_model(Post)
                    a.save()
            except DatabaseError as err:
                return JsonResponse({'status': 'error'})
        elif not t:
            try:
                with transaction.atomic():
                    p = Post.objects.create(image=request.FILES['post_image'])
                    a = Action(actor=u, verb='post', target_id=p.pk)
                    a.target_ct = ContentType.objects.get_for_model(Post)
                    a.save()
            except DatabaseError as err:
                return JsonResponse({'status': 'error'})
        else:
            try:
                with transaction.atomic():
                    p = Post.objects.create(text=t, image=request.FILES['post_image'])
                    a = Action(actor=u, verb='post', target_id=p.pk)
                    a.target_ct = ContentType.objects.get_for_model(Post)
                    a.save()
            except DatabaseError as err:
                return JsonResponse({'status': 'error'})
        
        return JsonResponse({'status': 'ok'})