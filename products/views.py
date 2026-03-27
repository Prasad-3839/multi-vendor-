from django.shortcuts import render ,redirect ,get_object_or_404
from .models import Product,Category
from vendors.models import Vendor
from .forms import ProductForm
from django.contrib.auth.decorators import login_required


def get_vendor(request):
    return Vendor.objects.filter(user=request.user).first()


@login_required
def add_product(request):
    vendor = get_vendor(request)

    if not vendor:
        return redirect('become_vendor')

    form = ProductForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        product = form.save(commit=False)
        product.vendor = vendor
        product.save()
        return redirect('product_list')

    return render(request, 'vendors/add_product.html', {'form': form})


@login_required
def product_list(request):
    vendor = get_vendor(request)

    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category')

    products = Product.objects.filter(vendor=vendor)

    # 🔍 SEARCH FILTER
    if search_query:
        products = products.filter(name__icontains=search_query)

    # 📂 CATEGORY FILTER
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, 'vendors/product_list.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id
    })



@login_required
def edit_product(request, id):
    vendor = get_vendor(request)

    product = get_object_or_404(Product, id=id, vendor=vendor)

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'vendors/add_product.html', {'form': form})


@login_required
def delete_product(request, id):
    vendor = get_vendor(request)

    product = get_object_or_404(Product, id=id, vendor=vendor)
    product.delete()

    return redirect('product_list')


def public_product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(request, 'vendors/public_product_detail.html', {
        'product': product
    })