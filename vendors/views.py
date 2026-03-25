from django.shortcuts import render, redirect
from .forms import VendorForm
from .models import Vendor

# Create Vendor Profile
def create_vendor(request):
    if request.user.user_type != 'vendor':
        print(request.user.user_type)
        return redirect('home')


    form = VendorForm()

    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.save()
            return redirect('vendor_dashboard')

    return render(request, 'vendors/create_vendor.html', {'form': form})


# Vendor Dashboard
def vendor_dashboard(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        return redirect('create_vendor')

    if not vendor.is_approved:
        return render(request, 'vendors/not_approved.html')

    return render(request, 'vendors/dashboard.html', {'vendor': vendor})
