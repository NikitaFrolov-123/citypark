from django.shortcuts import render, redirect
from .forms import ContactMessageForm

def contacts_view(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacts')
    else:
        form = ContactMessageForm()
    return render(request, 'contacts.html', {'form': form})