from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Blog
from django.shortcuts import render
from vendors.models import Vendor
from products.models import Product, Category  


def Home(request):
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category')

    vendor = None
    products = Product.objects.filter(vendor__is_approved=True)

     # 🔍 SEARCH
    if search_query:
        products = products.filter(name__icontains=search_query)

    # 📂 CATEGORY FILTER
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    if request.user.is_authenticated:
        vendor = Vendor.objects.filter(user=request.user).first()

    return render(request, 'index.html', {
        'vendor': vendor,
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id
    })


def About(request):
    return render(request,'about.html')

def Blogs(request):
    blogsdata=Blog.objects.all().order_by('title')[:1]
    for blog in blogsdata:
        print(blog.image)        # file name
        print(blog.image.url)    # URL path
        print(blog.image.path)
    return render(request,'blog.html',{'blogs':blogsdata})

def BlogDetail(request):
    return render(request,'blog-details.html')

def Contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        date=request.POST.get('date')
        query=request.POST.get('query')

        print(name,email,phone,date,query)

        data={
            "name":name,
            "email":email,
            "phone":phone,
            "date":date,
            "query":query

        }
            
        # return HttpResponse("form submitted")
        return render(request,'contact.html',{"data":data})
    return render(request,'contact.html')

def marksheet(request):
    result = None

    if request.method == "POST":
        name = request.POST.get('name')
        sub1 = request.POST.get('sub1')
        sub2 = request.POST.get('sub2')
        sub3 = request.POST.get('sub3')
        sub4 = request.POST.get('sub4')
        sub5 = request.POST.get('sub5')
        sub6 = request.POST.get('sub6')

        try:
            sub1 = int(sub1)
            sub2 = int(sub2)
            sub3 = int(sub3)
            sub4 = int(sub4)
            sub5 = int(sub5)
            sub6 = int(sub6)

            total = sub1 + sub2 + sub3 + sub4 + sub5 + sub6
            percentage = total / 6

            # Division logic
            if percentage >= 60:
                division = "First Division"
            elif percentage >= 50:
                division = "Second Division"
            elif percentage >= 40:
                division = "Third Division"
            else:
                division = "Fail"

            result = {
                "name": name,
                "total": total,
                "percentage": percentage,
                "division": division
            }

        except:
            result = {"error": "Invalid input"}

    return render(request, "marksheet.html", {"result": result})