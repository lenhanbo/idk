from django.shortcuts import render
from django.views import generic
from django.template import loader
from django.http import HttpResponse, Http404, FileResponse
from .models import document, comment
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import os
# from .models import 
from .forms import create_blog, create_comment
# Create your views here.

class homepage(LoginRequiredMixin, generic.ListView):
    model = document
    template_name = 'blog/homepage.html'
    context_object_name = 'document' 
    paginate_by = 12
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Trang chủ'
        return context
    

class document_detail(LoginRequiredMixin, generic.DetailView):
    model = document
    template_name = 'blog/document_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_comment = create_comment()
        context['comments'] = self.object.comment_set.order_by('-upload_date')
        context['form'] = my_comment
        return context
    
#them 1 blog moi
@login_required
def submit_blog_form(request):
    if request.method == "POST":
        my_object = create_blog(request.POST, request.FILES)
        if my_object.is_valid():
            my_blog = my_object.save(commit = False) #Lưu từ form -> object của model để chỉnh sửa sau đó mới save
            my_blog.author = request.user
            my_blog.save()
        else : 
            print(my_object.errors)
    return redirect("/homepage/")

#them comment
@login_required
def submit_comment_form(request, pk):
    if request.method == "POST":
        object = create_comment(request.POST)
        if object.is_valid():
            my_comment= object.save(commit = False) #Lưu từ form -> object của model để chỉnh sửa sau đó mới save
            my_comment.author = request.user
            my_blog = document.objects.get(id=pk)
            my_comment.blog = my_blog
            my_comment.save()
        else : 
            print(object.errors)
    return redirect(f"/document/{pk}/")


#xóa comment
@login_required
def delete_comment(request, pk, id):
    if request.method == "POST":
        object = comment.objects.get(id = id)
        object.delete()
    return redirect(f"/document/{pk}/")
#xóa blog
@login_required
def delete_blog(request, pk):
    if request.method == "POST":
        object = document.objects.get(id = pk)
        object.delete()
    return redirect("/homepage")

@login_required
def create_blog_form(request):
    template = loader.get_template('blog/create_blog_form.html')
    my_form = create_blog()
    context = {
        'form' : my_form, 
    }
    return HttpResponse(template.render(context, request))





def download_file(request, pk):
    if request.method == "POST":
        my_document = document.objects.get(pk = pk)
        if not my_document.file:
            raise Http404("Không tìm thấy file.")
        file_path = my_document.file.path
        return FileResponse(open(file_path,'rb'), as_attachment=1,filename=os.path.basename(file_path))
    
        