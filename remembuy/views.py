import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.utils.safestring import mark_safe
from iommi import (
    Page,
    html,
    Field,
    Form,
    Table,
)

from remembuy.models import Item


class LoginForm(Form):
    username = Field()
    password = Field.password()

    class Meta:
        title = 'Login'

        @staticmethod
        def actions__submit__post_handler(form, **_):
            if form.is_valid():
                user = auth.authenticate(
                    username=form.fields.username.value,
                    password=form.fields.password.value,
                )

                if user is not None:
                    request = form.get_request()
                    auth.login(request, user)
                    return HttpResponseRedirect(request.GET.get('next', '/'))

                form.errors.add('Unknown username or password')


class LoginPage(Page):
    form = LoginForm()
    set_focus = html.script(mark_safe(
        'document.getElementById("id_username").focus();',
    ))


def login(request):
    return LoginPage()


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def index(request):
    return Table(auto__model=Item)


def login_for_api(request):
    if request.user.is_anonymous:
        data = request.GET if request.method == 'GET' else request.POST
        request.user = auth.authenticate(
            username=data['username'],
            password=data['password'],
        )


def api_items(request):
    login_for_api(request)
    return HttpResponse(json.dumps([
        dict(
            id=x.id,
            name=x.name,
            createdAt=x.created_at,
            user=x.user.username,
            completed=x.completed,
            completedAt=x.completed_at,
        )
        for x in Item.objects.filter(completed=False).select_related('user')
    ]))


def api_add(request):
    login_for_api(request)

    Item.objects.create(user=request.user, name=request.POST['name'])
    return HttpResponse('OK')


def api_complete(request, id):
    login_for_api(request)

    Item.objects.filter(pk=id).update(completed=True)
    return HttpResponse('OK')


def api_un_complete(request, id):
    login_for_api(request)

    Item.objects.filter(pk=id).update(completed=False)
    return HttpResponse('OK')


def api_edit(request, id):
    login_for_api(request)

    item = Item.objects.get(pk=id)
    item.name = request.POST['name']
    item.save()
    return HttpResponse('OK')


def redirect_login(request):
    return HttpResponseRedirect('/login/')
