from django.shortcuts import render, get_list_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm
from .models import User

def index(request):
    if request.user.is_authenticated:
        return render(request, 'feed/index.html')
    else:
        return render(request, 'index.html')

@login_required
def profile(request, pk):
    profile_owner = get_list_or_404(User, id=pk)
    num_followers = profile_owner.followers.count()
    same_user = False
    if request.user.id == id:
        same_user = True
    context = {'num_follow': num_followers,
                'same_user': same_user,
                'profile_owner': profile_owner}
    return render(request, 'accounts/profile.html', context)



class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'