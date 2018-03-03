from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import DatabaseError, transaction
from django.contrib.contenttypes.models import ContentType

from .models import Action, Post

@require_POST
@login_required
def post_action(request):
    """
    handles a request to post to the news feed
    """
    print('post_actionnnnnnnnnnnnnnnnnnnn')
    
    if (not request.POST['post_text']) and (not request.FILES):
        return JsonResponse({'status': 'empty'})
    t = request.POST['post_text']
    if not request.FILES:
        try:
            with transaction.atomic():
                p = Post.objects.create(text=t)
                a = Action(actor=request.user, verb='post', target_id=p.pk)
                a.target_ct = ContentType.objects.get_for_model(Post)
                a.save()
        except DatabaseError as err:
            return JsonResponse({'status': 'error'})
    elif not t:
        try:
            with transaction.atomic():
                p = Post.objects.create(image=request.FILES['post_image'])
                a = Action(actor=request.user, verb='post', target_id=p.pk)
                a.target_ct = ContentType.objects.get_for_model(Post)
                a.save()
        except DatabaseError as err:
            return JsonResponse({'status': 'error'})
    else:
        try:
            with transaction.atomic():
                p = Post.objects.create(text=t, image=request.FILES['post_image'])
                a = Action(actor=request.user, verb='post', target_id=p.pk)
                a.target_ct = ContentType.objects.get_for_model(Post)
                a.save()
        except DatabaseError as err:
            return JsonResponse({'status': 'error'})
    
    return JsonResponse({'status': 'ok'})