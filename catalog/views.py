from django.shortcuts import render

# Create your views here.
from .models import Mugalim, Mamandyk, Kurs


def num_mamandyks():
    pass
def num_mugalims():
    pass

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Mamandyk.objects.all().count()
    num_instances=Kurs.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=Kurs.objects.filter(status__exact='a').count()
    num_authors=Mugalim.objects.count()  # The 'all()' is implied by default.
    
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_mamandyks':num_mamandyks,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_mugalims':num_mugalims,
            'num_visits':num_visits}, # num_visits appended
    )
from django.views import generic

class MamandykListView(generic.ListView):
    model = Mamandyk
    paginate_by = 2
class MamandykDetailView(generic.DetailView):
    model = Mamandyk
from django.views import generic

class MugalimListView(generic.ListView):
    model = Mugalim
class MugalimDetailView(generic.DetailView):
    model = Mugalim
    model2=Mamandyk
    paginate_by = 2
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedMamandyksByUserListView(LoginRequiredMixin,generic.ListView):

    model =Kurs
    template_name ='catalog/kurs_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Kurs.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewMamandykForm


def mamandyk_inst(args):
    pass


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    mamandyk_inst=get_object_or_404(Kurs, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewMamandykForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            mamandyk_inst.due_back = form.cleaned_data['renewal_date']
            mamandyk_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewMamandykForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/mamandyk_renew_librarian.html', {'form': form, 'mamandykinst':mamandyk_inst})