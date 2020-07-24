import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
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


def json_response(data):
    return HttpResponse(
        json.dumps(data),
        content_type='application/json',
    )


def api_items(request):
    login_for_api(request)
    return json_response(
        [
            x.as_dict()
            for x in Item.objects.filter(completed=False).select_related('user')
        ]
    )


@csrf_exempt
def api_add(request):
    login_for_api(request)

    return json_response(
        Item.objects.create(user=request.user, name=request.POST['name']).as_dict(),
    )


@csrf_exempt
def api_complete(request):
    login_for_api(request)
    id = request.POST['id']

    Item.objects.filter(pk=id).update(completed=True)
    return json_response(Item.objects.get(pk=id).as_dict())


@csrf_exempt
def api_un_complete(request):
    login_for_api(request)
    id = request.POST['id']

    Item.objects.filter(pk=id).update(completed=False)
    return json_response(Item.objects.get(pk=id).as_dict())


@csrf_exempt
def api_edit(request):
    login_for_api(request)
    id = request.POST['id']

    item = Item.objects.get(pk=id)
    item.name = request.POST['name']
    item.save()
    return json_response(Item.objects.get(pk=id).as_dict())


def redirect_login(request):
    return HttpResponseRedirect('/login/')
