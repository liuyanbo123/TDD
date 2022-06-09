#from django.http import HttpResponse
# Create your views here.
#from django.shortcuts import render

from django.shortcuts import redirect, render
from lists.models import Item, List

def new_list(request):
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect(f'/lists/{list_.id}/')

def home_page(request):
#	if request.method == 'POST':
#		Item.objects.create(text=request.POST['item_text'])
#		return redirect('/lists/the-only-list-in-the-world/')
	return render(request,'home.html')
#	items = Item.objects.all()
#	return render(request, 'home.html',{'items':items})

def view_list(request, list_id):
#	pass
	list_ = List.objects.get(id=list_id)
#	items = Item.objects.filter(list=list_)
	return render(request, 'list.html',{'list':list_})

def add_item(request, list_id):
	list_ = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect(f'/lists/{list_.id}/')













#	if request.method == 'POST':
#		return HttpResponse(request.POST['item_text'])
#	item = Item()
#	item.text = request.POST.get('item_text', '')
#	item.save()

#	return render(request, 'home.html',{
#		'new_item_text': item.text
#		})
# request.POST.get('item_text','')