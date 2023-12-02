from django.shortcuts import render, get_object_or_404
from .models import Group, GroupMember
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.db import IntegrityError
from . import models 
from django.shortcuts import redirect
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

# Create your views here.
def ListGroup(request):
    posts = Group.objects.order_by('-name')
    return render(request, "group.html", {'ups': posts})

def add_Group(request):
    if request.method=="POST":   
        name = request.POST['name']
        slug = request.POST['slug']
        avatar = request.FILES['avatar']
        description = request.POST['description']          
        group= Group(name=name, slug=slug, avatar=avatar,description=description)
        group.save()        
        messages.success(request, "Chỉnh sửa thành công!")    
        # return redirect('list_groups')
    return render(request, "add_new_group.html")

class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:group")
        # return reverse("/group")
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:group")

    def get(self, request, *args, **kwargs):

        try:

            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)