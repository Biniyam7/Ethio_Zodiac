
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import UserRegisterForm
from .form import UserUpdateForm
from .form import ProfileUpdateForm
from .form import CommentForm
from .models import Comment


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to login.')
            return redirect('login')
    else:    
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES, 
                                    instance=request.user.profile)
        if u_form.is_valid and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account Has Been Updated')
            return redirect('profile')

   
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
       'u_form': u_form,
       'p_form': p_form
   }
    return render(request, 'users/profile.html', context)


@login_required
def comment(request):
    comnt= Comment.objects.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            comment_form.save(commit=False)
            comment_form.instance.user = request.user
            comment_form.save()
            messages.success(request, f'commented by  {request.user}! ')
        else:
            print(comment_form.errors)
            
    else:
        comment_form = CommentForm()
    return render(request, 'users/comment.html', {'comnt':comnt,
                                                'comment_form': comment_form})
    





