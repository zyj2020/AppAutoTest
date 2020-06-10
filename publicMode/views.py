from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from projectMode.models import ProductMode, ProjectMode


def login(request):
    next_page = request.GET.get('next', '')
    if request.POST:
        username = password = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session['user'] = username
            if next_page == "":
                return HttpResponseRedirect('/home')
            else:
                return HttpResponseRedirect(next_page)
        #  return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'username or password error'})

    return render(request, 'login.html', {"next": next_page})


def home(request):
    return render(request, "home.html")


def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


def get_list(module, sub_type='testCase'):
    project_list = ProjectMode.objects.filter(projectFlag=True, module__exact=module, subType__exact=sub_type)
    project_pro_list = project_list.values_list('productId', flat=True)
    product_list = ProductMode.objects.filter(productFlag=True, id__in=project_pro_list)
    return [product_list, project_list]
