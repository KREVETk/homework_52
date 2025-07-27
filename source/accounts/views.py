from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('project_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"

    def get_success_url(self):
        return self.request.GET.get("next") or reverse_lazy("projects")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return redirect(self.get_success_url())

