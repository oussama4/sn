from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .forms import UserCreationForm
from .models import User

def index(request):
    if request.user.is_authenticated:
        return render(request, 'feed/index.html')
    else:
        return render(request, 'index.html')

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
    followed_id = request.POST['id']
    action = request.POST['action']
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


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'