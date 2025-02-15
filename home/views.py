from django.shortcuts import render
def index(request):
<<<<<<< HEAD
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html', {
        'template_data': template_data})
def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html',
                  {'template_data': template_data})
def empty(request):
    return redirect('movies.index')
=======
    return render(request, 'home/index.html')
    
def about(request):
    return render(request, 'home/about.html')
    
>>>>>>> 2d8d7379ff945c4af224060bc4b8edd596a37b39
