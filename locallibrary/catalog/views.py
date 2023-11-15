from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from .models import Book, BookInstance, Author
from django.views import generic
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    
    # Example. Get 5 books containing the title war
    #def get_queryset(self):
    #    return Book.objects.filter(title__icontains='war')[:5] 
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['book_list'] = Book.objects.all()
        return context
    
    template_name="book_list.html"
    paginate_by = 2
    
class BookDetailView(generic.DetailView):
    model = Book

def book_detail_view(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')

    return render(request, 'book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
    model = Author
    template_name = "author_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author_list"] = Author.objects.all()
        return context
    
def author_detail_view(request, id):
    try:
        author = Author.objects.get(pk=id)
    except Author.DoesNotExist:
        raise Http404("Author does not exist")
    
    return render(request, 'author_detail.html', context={'author': author})

@login_required
def user_profile(request, username):
    user = User.objects.get(username=username)
    if not user:
        print("No user")
    else:
        print(f'Found user: {user.username}')
    return render(request, 'user_profile.html', {"user":user})