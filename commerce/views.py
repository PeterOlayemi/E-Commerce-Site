from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import *
from .forms import *

# Create your views here.

def CategoryView(request, category):
    obj = Product.objects.filter(category__name=category)
    obj_c = Product.objects.filter(category__name=category).count()
    context = {'obj':obj, 'obj_c':obj_c}
    return render(request, 'category.html', context)

@login_required
def QueryView(request, pk):
    obj = Order.objects.filter(buyer=request.user).get(id=pk)
    form = QueryForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.buyer = request.user
            data.order = obj
            data.save()
            obj.queried = True
            obj.save()
            return redirect(reverse('detailorder', args=[obj.pk]))
    context = {'form':form, 'obj':obj}
    return render(request, 'addreview.html', context)

@login_required
def AddReviewView(request, pk):
    obj = Product.objects.get(id=pk)
    form = ReviewForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data=form.save(commit=False)
            data.buyer = request.user
            data.product=obj
            data.save()
            return redirect(reverse('detail', args=[obj.pk]))
    context = {'form':form, 'obj':obj}
    return render(request, 'addreview.html', context)

@login_required
def LikeView(request, pk):
    obj = Product.objects.get(id=pk)
    if obj.likes.filter(id=request.user.id).exists():
        obj.likes.remove(request.user)
    else:
        obj.likes.add(request.user)
    return redirect(reverse('detail', args=[obj.pk]))

def PrivacyView(request):
    return render(request, 'privacy.html')

def TermView(request):
    return render(request, 'term.html')

def AboutView(request):
    return render(request, 'about.html')

def ContactView(request):
    return render(request, 'contact.html')

def RegisterView(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request, 'registration/register.html', context)

@login_required
def DetailOrderView(request, pk):
    obj = Order.objects.filter(buyer=request.user).get(id=pk)
    if request.method != 'POST':
        form = ReceiptForm()
    else:
        form = ReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.order = obj
            data.save()
            obj.sent_receipt = True
            obj.save()
            return redirect(reverse('detailorder', args=[obj.pk]))
    context = {'obj':obj, 'form':form}
    return render(request, 'detailorder.html', context)

@login_required
def OrderView(request):
    obj = Order.objects.filter(buyer=request.user).order_by('-date_added')
    context = {'obj':obj}
    return render(request, 'cart.html', context)

@login_required
def AddOrderView(request, name):
    obj = Product.objects.get(name = name)
    form = OrderForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.buyer = request.user
            data.product = obj
            data.price = obj.price * data.quantity
            data.save()
            return redirect(reverse('detailorder', args=[data.pk]))
    context = {'form':form, 'obj':obj}
    return render(request, 'addcart.html', context)

def DetailView(request, pk):
    obj = Product.objects.all().get(id=pk)
    data = Review.objects.filter(product=obj)
    data_c = Review.objects.filter(product=obj).count()
    liked = False
    if obj.likes.filter(id=request.user.id).exists():
        liked = True
    context={'obj':obj, 'liked':liked, 'data':data, 'data_c':data_c}
    return render(request, 'detail.html', context)

def HomeView(request):    
    q = request.POST.get('q') if request.POST.get('q') != None else ''
    obj = Product.objects.filter( Q(search_tag1__icontains=q) | Q(search_tag2__icontains=q) | Q(search_tag3__icontains=q) | Q(category__name__icontains=q) | Q(name__icontains=q))
    obj_c=Product.objects.all().count()
    data=Category.objects.all()
    data_c=Category.objects.all().count()
    context={'obj':obj, 'obj_c':obj_c, 'data_c':data_c, 'data':data}
    return render(request, 'index.html', context)
