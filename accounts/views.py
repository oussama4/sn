from json import loads

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views import View
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from .serializers import RegisterSerializer
from .models import User, OfpptID
from .validators import valid_password

@login_required
def profile(request, pk):
    profile_owner = get_object_or_404(User, id=pk)
    num_followers = profile_owner.followers.count()
    same_user = False
    if request.user.id == pk:
        same_user = True
    context = {'num_follow': num_followers,
                'same_user': same_user,
                'profile_owner': profile_owner}
    return render(request, 'accounts/profile.html', context)

@require_POST
@login_required
def follow(request):
    """
    handles a post request to trigger the follow/unfollow action
    """

    print('follow user called')
    payload = loads(request.body)
    followed_id = payload['id']
    action = payload['action']
    if followed_id and action:
        try:
            followed = User.objects.get(id=followed_id)
            if action == 'follow':
                followed.followers.add(request.user)
            else:
                followed.followers.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})

@method_decorator(csrf_exempt, name='dispatch')
class SignUp(APIView):
    """
    a view to handle user registration requests
    """

    def post(self, request):
        data = loads(request.body)
        serializer = RegisterSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse({'errored': True, 'errors': serializer.errors})
        serializer.create(serializer.validated_data)
        return JsonResponse({'errored': False, 'errors': None})
    

class UpdateUser(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['email', 'first_name', 'last_name', 'avatar', 'bio']
    template_name = 'accounts/settings.html'
