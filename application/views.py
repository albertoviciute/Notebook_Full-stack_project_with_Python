from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import SignUpForm, CreateCategoryForm, CreateNoteForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Note
from django.db.models import Q


# Create your views here.

def home(request):
    return render(request, 'home.html')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('home'))
    else:
        form = SignUpForm()
    return render(request, 'registration/sign_up.html', context={'form': form})


@login_required()
def show_user_categories(request):
    categories = Category.objects.filter(user=request.user.id) \
        .values('category', 'id')
    context = {
        'categories': categories
    }
    return render(request, 'categories.html', context=context)


@method_decorator(login_required, name='dispatch')
class CreateCategoryView(LoginRequiredMixin, CreateView):
    form_c = CreateCategoryForm
    context = {}
    template_name = 'create_category.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        self.context['form'] = self.form_c(initial={'user': user})
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_c(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_user_categories')
        else:
            self.context['form'] = form
            return render(request, self.template_name, self.context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class EditCategory(CreateCategoryView, UpdateView):
    form_c = CreateCategoryForm
    context = {}
    template_name = 'edit_category.html'

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        categories = get_object_or_404(Category, pk=id)
        form = self.form_c(instance=categories)
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')
        categories = get_object_or_404(Category, pk=id)
        form = self.form_c(instance=categories, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_category', id=id)
        else:
            self.context['form'] = form
            return render(request, self.template_name, self.context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteCategory(DeleteView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        categories = get_object_or_404(Category, pk=id)
        categories.delete()
        return redirect('show_user_categories')


def show_category(request, id):
    category = get_object_or_404(Category, pk=id)
    return render(request, 'show_category.html', {'category': category})


@method_decorator(login_required, name='dispatch')
class CreateNote(LoginRequiredMixin, CreateView):
    form_c = CreateNoteForm
    context = {}
    template_name = 'create_note.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        self.context['form'] = self.form_c(initial={'user': user})
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_c(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('show_user_notes')
        else:
            self.context['form'] = form
            return render(request, self.template_name, self.context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class EditNote(CreateNote, UpdateView):
    form_c = CreateNoteForm
    context = {}
    template_name = 'edit_note.html'

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        notes = get_object_or_404(Note, pk=id)
        form = self.form_c(instance=notes)
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')
        notes = get_object_or_404(Note, pk=id)
        form = self.form_c(data=request.POST, files=request.FILES, instance=notes)
        if form.is_valid():
            form.save()
            return redirect('show_note', id=id)
        else:
            self.context['form'] = form
            return render(request, self.template_name, self.context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteNote(DeleteView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        categories = get_object_or_404(Note, pk=id)
        categories.delete()
        return redirect('show_user_notes')


def show_note(request, id):
    note = get_object_or_404(Note, pk=id)
    return render(request, 'show_note.html', {'note': note})


@login_required()
def show_user_notes(request):
    notes = Note.objects.filter(user=request.user.id) \
        .values('title', 'id', 'category')
    context = {
        'notes': notes
    }
    return render(request, 'notes.html', context=context)


def search(request):
    query = request.GET.get('query')
    search_results = Note.objects.filter(Q(title__icontains=query))
    return render(request, 'search.html', {'notes': search_results, 'query': query})
