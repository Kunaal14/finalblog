from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render, Http404 
from django.utils import timezone
# Create your views here.
from django.db.models import Q

from django.forms import inlineformset_factory
from .models import Post
from .forms import PostModelForm
from django.contrib.auth import login, get_user_model, logout
from django.shortcuts import render, redirect
from django.forms import formset_factory, modelformset_factory
#from . models import Profile
from django.forms.models import inlineformset_factory
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import MyUser
from django import template
from django.contrib.auth import login, get_user_model, logout
from .forms import UserCreationForm, UserLoginForm
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView , ContextMixin, TemplateResponseMixin
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from. import models
from django.contrib.messages.views import SuccessMessageMixin

User = get_user_model()

def register(request, *args, **kwargs):

    #a = Post.objects.filter(slug = "k")
    

    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        print("user created ")
        return HttpResponseRedirect("/login")

    return render(request, "register.html", {"form":form})


def user_login(request, *args, **kwargs):

    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get("user_obj")

        #user_obj = User.objects.get(username__iexact=query)
        login(request, user_obj)
        ##print(request.user.profile.user)
        #print(user_obj)
        print(user_obj.username)
        context = {
            "username" : user_obj.username
#
        }
        return redirect('blog:dashboard')
        # def get_success_url(self):
        #       return reverse("A1:dashboard")
        #return render(request, "A1/dashboard.html")
    return render(request, "login.html", {"form":form})

# class Dashboard(TemplateView):
#     template_name = "A1/index.html"

#     @method_decorator(login_required)
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "this is the data"
#         return context


def dashboard(request):
    if request.user.is_authenticated:
        qs = Post.objects.filter(user=request.user)
        obj = request.user.username
        query = request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                    Q(title__icontains=query) |
                    Q(content__icontains=query) 
                    #Q(slug__icontains=query)

                )
        #obj1 = get_object_or_404(UserBlogs, slug=obj)
    #print(request.user.slug)
    #print(str())
    #obj = get_object_or_404(MyUser)
        context = {
                "object_list":qs,
                "object" : obj,
            }
    #context = context
    else:
        return redirect('/logout/')
    return render(request, "dashboard.html", context)
    # def get_success_url(self):
    #   return reverse("A1:dashboard")

def user_blogs(request):
    query = request.GET.get("q", None)

    qs = MyUser.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(username__icontains=query) 
                #Q(content__icontains=query) |
                #Q(slug__icontains=query)

            )
    
    context = {
            "qs" : qs
    }
    return render(request, 'user_blogs.html', context)




def list_view(request, username):
    try:

        qs = Post.objects.filter(slug  = username)
        

        template = "list.html"
        context = {
            "object_list":qs
        }
        return render(request, template, context)
    except:
        return Http404("page not found")


def detail_view(request, user_id):
    #obj = UsersInfom.objects.get(id=user_id)
    # qs = UsersInfom.objects.get(id=id)
    # obj=None
    # if not qs.exists() and qs.count() != id:
    #     raise Http404
    # else:
    #     obj = qs.first()
    #obj = UsersInfom.objects.all()
    obj = get_object_or_404(Post, id=user_id)
    # print(obj)

    template = "detail-view.html"
    # try:
    #     obj = PostModel.objects.get(id=user_id)
    # except PostModel.DoesNotExist:
    #     raise Http404('this book does not exists')
    context = {
        "object" : obj,
    }

    #return render(request, 'firstapp/details.html', {'obj':obj})
    return render(request, template, context)

def post_model_delete_view(request, user_id):
    obj = get_object_or_404(Post, id=user_id)
    # print(obj)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "POST DELETED")
        return HttpResponseRedirect("/dashboard/")

    template = "blog_confirm_delete.html"
    context = {
        "object" : obj,
    }
    return render(request, template, context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login")

def index(request):
    #if request.user.is_authenticated:
       # print(request.user.profile.city)

    return render(request, "index.html", {})


# def formset_view(request):
#     print(request.user.username)
#     try:
#         if request.user.is_authenticated:
           
#             PostModelFormset = modelformset_factory(Post, form=PostModelForm)
#             #formset = PostModelFormset(request.POST or None)
#             # PostModelFormset = modelformset_factory(Post, form=PostModelForm)
#             # formset = PostModelFormset(request.POST or None, 
#             #         queryset=Post.objects.filter(user=request.user))
#             queryset= Post.objects.filter(user=request.user)
#             formset = PostModelFormset(request.POST or None, queryset=queryset)
#             if formset.is_valid():
#                 instances = formset.save(commit=False)
#                 for instance in instances:
#                     instance.user = request.user
#                     instance.save()
#         #         print(form.cleaned_data)
#         #         obj = form.save(commit=False)
#         #         if form.cleaned_data:
#         #         # #     #obj.title = "This title %s" %(obj.id)
#         #         #     if not form.cleaned_data.get("publish"):
#         #         #         obj.publish = timezone.now()
#         #             obj.save()
#         #     return redirect("/")
#             #print(formset.cleaned_data)
#             context = {
#             "formset": formset

#                 }
#             return render(request, "formset_view.html", context)
    
#         else:
#             raise Http404
#     except:
#         messages.success(request, "ughh")
#         return HttpResponseRedirect("/dashboard/")


class BlogDeleteView(DeleteView):
    model = Post

    def get_success_url(self):
        return reverse("A1:list")


def post_model_create_view(request):

    if request.user.is_authenticated:
        #context = {}
        print(request.user.id)  
        #a = request.user.id
        #print (a)
        # data = {
        #     'user': request.user
        # }
        #if request.method=='POST': 
        print("hello")
        form = PostModelForm(request.POST or None,request.user)
        #form = form1(queryset=Post.objects.filter(user=request.user))

        context = {
            "form":form
        }
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            print(obj.title)
            obj.save()
            messages.success(request, "Created a new blog")
            context={
            #"form":PostModelForm()
              "form":PostModelForm()#request.POST or None
            }
            #return HttpResponseRedirect("/blog/{num}".format(num=obj.id))

        template = "create-view.html"
        return render(request, template, context)


class BlogUpdateView(SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = "A1/form.html"


class BlogDetail(SuccessMessageMixin, DetailView):
    model = Post


def post_model_update_view(request, user_id):
    obj = get_object_or_404(Post, id=user_id)
    form = PostModelForm(request.POST or None, instance=obj)
    context = {
        #"object":obj,
        "form":form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        print(obj.title)
        obj.save()
        messages.success(request, "updated blog")
        context={
            #"form":PostModelForm()
            "form":PostModelForm()#request.POST or None
        }
        return HttpResponseRedirect("/blog/{num}".format(num=obj.id))

    template = "update-view.html"
    return render(request, template, context)



class BlogList(SuccessMessageMixin, ListView):
    model = Post


# def manage_blogs(request, author_id):
#     user = MyUser.objects.get(user = request.user)
#     PostInlineFormset = inlineformset_factory(MyUser, POST, fields=('title',))
#     if request.method == "POST":
#         formset = PostInlineFormset(request.POST, request.FILES, instance=user)
#         if formset.is_valid():
#             formset.save()
#             # Do something. Should generally end with a redirect. For example:
#             return HttpResponseRedirect(user.get_absolute_url())
#     else:
#         formset = BookInlineFormSet(instance=user)
#     return render(request, 'create-view.html', {'formset': formset})

