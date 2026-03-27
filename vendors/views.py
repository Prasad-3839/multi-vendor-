from django.shortcuts import render, redirect
from .forms import VendorForm
from .models import Vendor

# Create Vendor Profile
def become_vendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.save()
            return redirect('vendor_dashboard')
    else:
        form = VendorForm()

    return render(request, 'vendors/become_vendor.html', {'form': form})



def vendor_dashboard(request):
    vendor = Vendor.objects.get(user=request.user)
    return render(request, 'vendors/vendor_dashboard.html', {'vendor': vendor})

