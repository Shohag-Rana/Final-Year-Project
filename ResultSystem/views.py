from django.shortcuts import render, HttpResponseRedirect

def home_page(request):
	
	return render(request, 'base.html')