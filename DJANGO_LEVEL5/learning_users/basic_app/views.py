from django.contrib import auth
from basic_app.forms import UserForm, UserProfileInfoForm
from django.shortcuts import render
# Create your views here.

# para el login esto
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'basic_app/index.html')


@login_required()
def special(request):
    # si por ejemplo quiero que solo un usuario logeado vea esto
    # lo decoro con eso
    return(HttpResponse('your are logged in, nice!'))


@login_required()
def user_logout(request):
    # para que solo un usuario logeado pueda hacer esto,
    # osea desloguearse, le
    # decoro con el @

    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False

    if request.method == 'POST':
        # agarramos la info de los form
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # nos fijamos si son validos
        if user_form.is_valid() and profile_form.is_valid():

            # agarramos lo del usuario lo guardamos,
            # le hacemos hash a la contraseña y guardamos de nuevo
            # osea agarramos todo del user form
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # es falso porque no quiero guardar todavia, quiero hacer algo
            # primero

            # osea aca en el profile agarramos todo lo del profile_form
            profile = profile_form.save(commit=False)

            # como el UserProfileInfo tiene una oneToOne con USER, esto se
            # define asi
            profile.user = user

            # si puso imagen la guardamos
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    # SI SE llena la info del login
    if request.method == 'POST':
        # agarramos por post.get porque en el html, usamos simple html
        # y lo llamamos username en el html, y el password iguall
        username = request.POST.get('username')
        password = request.POST.get('password')

        # con esta sola linea django hace toda la comprobacion
        # si estas logeado o no, te da un objeto
        user = authenticate(username=username, password=password)

        if user:
            # ahora me dijo si esta activada la cuenta el user
            if user.is_active:
                # con la funcion login que importamos
                # logeamos al usuario con login, y despues lo mandamos
                # a la pagina que queremos
                login(request, user)
                # si es logeado lo redirijo de nuevo a la pagina home
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account not active')
        else:
            print("someone trie to log in and failed")
            print('Username: {} and password {}').format(username, password)
            return HttpResponse("invalid login details supplid")
    else:
        return render(request, 'basic_app/login.html', {})
