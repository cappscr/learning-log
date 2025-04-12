from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from utils.helpers import sendGaEvent

# Create your views here.
def register(request):
  """Register a new user."""
  if request.method != 'POST':
    # Display a blank registration form.
    form = UserCreationForm()
  else:
    # Process completed form.
    form = UserCreationForm(data=request.POST)

    if form.is_valid():
      new_user = form.save()

      if request.POST["ga_client_id"]:
          sendGaEvent(request.POST["ga_client_id"], "user_registration", {
              "username": str(new_user)
          })
      else:
        print(f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] ga_client_id not received')

      # Log the user in and then redirect to the home page.
      login(request, new_user)
      return redirect('learning_logs:index')
  
  # Display a blank or invalid form
  context = {'form': form}
  return render(request, 'registration/register.html', context)
