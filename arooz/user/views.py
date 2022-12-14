import uuid

from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .helper import send_forget_password_mail
from .models import AddToCart, AdminNumber, Category, ChangePassword, Event, Login, MainBanner, Measurements, Product, Size, SubBanners1, SubBanners2, SubCategory, Wishlist


def logout_view(request):
    logout(request)
    return redirect("user:login")


@csrf_exempt
def login_views(request):
    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("pass")
        user = Login.get(customer_name=username, password=password)
        if user is not None:
            return redirect("/")
        else:
            messages.info(request, "Invalid Credentials")
    return render(request, "web/login.html")


def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user_obj = Login.objects.get(email=email)

        token = str(uuid.uuid4())
        ChangePassword.objects.create(user=user_obj, forgot_password_token=token)
        send_forget_password_mail(user_obj.email, token)

        messages.warning(request, "An email is sent")
        return redirect("user:forgot password")
    context = {}
    return render(request, "web/forgot.html", context)


def change_password(request, token):

    context = {}
    change_password_obj = ChangePassword.objects.get(forgot_password_token=token)

    if change_password_obj.status:
        messages.error(request, "Link expired...")
        return redirect("web:forget password")

    if change_password_obj.user:

        customer = Login.objects.all()
        for customer in customer:
            if change_password_obj.user == customer:
                if change_password_obj.user.email == customer.email:

                    user_id = Login.objects.filter(email=change_password_obj.user.email).first()

                    if request.method == "POST":
                        new_password = request.POST.get("new_password")
                        confirm_password = request.POST.get("confirm_password")
                        user_id = request.POST.get("user_id")

                        if user_id is None:
                            messages.error(request, "User not found...")
                            return redirect(f"/change password/{token}/")

                        if new_password != confirm_password:
                            messages.error(request, "Your Password and confirm Password dosen't match")
                            return redirect(f"/change password/{token}/")

                        user_obj = Login.objects.get(email=change_password_obj.user.email)
                        user_obj.set_password(new_password)
                        user_obj.save()
                        ChangePassword.objects.filter(forgot_password_token=token).update(status=True)
                        messages.success(request, "Your password is updated")
                        return redirect("/")
                context = {"manager_id": change_password_obj.user.id}
    return render(request, "web/change-password.html", context)


def index(request):
    mainbanner = MainBanner.objects.last()
    subbanners1 = SubBanners1.objects.last()
    subbanners2 = SubBanners2.objects.last()
    topsave = Product.objects.filter(is_top_save_today=True)
    bestseller = Product.objects.filter(is_best_seller=True).count()
    bestseller1 = Product.objects.filter(is_best_seller=True)[::-1]
    bestseller2 = Product.objects.filter(is_best_seller=True)[::-1]
    context = {"mainbanner": mainbanner, "subbanner1": subbanners1, "subbanner2": subbanners2, "topsave": topsave, "bestseller1": bestseller1, "bestseller2": bestseller2}
    return render(request, "web/index.html", context)


def product(request, id):
    products = Product.objects.get(id=id)
    products.get_sizes()
    sub = products.subcategory
    percentage = ((products.price - products.offer_price) / products.price) * 100
    context = {"products": products, "subcategory": sub, "percentage": percentage}
    return render(request, "web/product-slider.html", context)


def shop(request, id):
    category = Category.objects.get(id=id)
    products = Product.objects.filter(subcategory__category=category)
    context = {"category": category, "products": products}
    return render(request, "web/shop-left-sidebar.html", context)


# @csrf_protect
# @login_required(login_url='login')


def addtowishlist(request, id):

    if request.user.is_authenticated:
        if Login.objects.get(user=request.user):
            print(request.user)
            product = Product.objects.get(id=id)
            if product:
                cust = Login.objects.get(user=request.user)
                if Wishlist.objects.filter(user=cust, product=product):

                    messages.warning(request, "product is already in wishlist...")
                    return redirect("/")
                else:
                    user = Login.objects.get(user=request.user)
                    Wishlist.objects.create(user=user, product=product)
                    messages.warning(request, "Product added successfully...")
                    return redirect("/")
                # return JsonResponse({'status':"Product added successfully"})
            else:

                messages.error(request, "No such product found...")

        else:

            messages.error(request, "Login to continue")
            return redirect("user:login")
    else:

        messages.error(request, "Login to continue")
        return redirect("user:login")


def viewwishlist(request):
    if request.user.is_authenticated:
        if Login.objects.get(user=request.user):

            my_p = Login.objects.get(user=request.user)
            wished_item = Wishlist.objects.filter(user=my_p)

            context = {"wished_items": wished_item}
            return render(request, "web/wishlist.html", context)
        else:
            messages.error(request, "pls login to continue")
            return redirect("user:login")
    else:
        messages.error(request, "pls login to continue")
        return redirect("user:login")


def deletefromwishlist(request, id):

    user = Login.objects.get(user=request.user)
    product = Wishlist.objects.get(user=user, id=id)

    product.delete()
    messages.warning(request, "Product removed successfully...")
    return redirect("/")

    # return JsonResponse({'status':"Product added successfully"})


def addtocart(request, id):
    if request.user.is_authenticated:
        print(request.user)
        if Login.objects.get(user=request.user):
            product = Product.objects.get(id=id)
            price = product.price
            if product:
                my_p = Login.objects.get(user=request.user)
                if AddToCart.objects.filter(user=my_p, product=product):
                    messages.warning(request, "product is already in cart")
                    return redirect("/")
                else:
                    my_p = Login.objects.get(user=request.user)
                    AddToCart.objects.create(user=my_p, product=product, total=price)
                    messages.warning(request, "Product added successfully")
                return redirect("/")
            else:
                messages.error(request, "product is not available")
                return redirect("/")
        else:
            messages.warning(request, "Login to Continue")
            return redirect("user:login")
    else:
        messages.warning(request, "Login to Continue")
        return redirect("user:login")


def addQuantity(request):
    quantity = request.GET["quantity"]
    print(quantity, "%" * 20)
    my_p = Login.objects.get(user=request.user)
    id = request.GET["id"]
    print(id)
    cart_obj = AddToCart.objects.get(id=id, user=my_p)

    print("########")

    new_quantity = int(quantity) + 1
    product_total = float(new_quantity) * float(cart_obj.product.offer_price)
    print(cart_obj.product.offer_price)

    print("*****")

    cart_obj.total = product_total
    print(cart_obj.total)

    cart_obj.save()
    AddToCart.objects.filter(id=id).update(quantity=new_quantity, total=product_total)
    print("success")
    data = {"total": cart_obj.total}
    return JsonResponse(data)


def lessQuantity(request):
    quantity = request.GET["quantity"]

    my_p = Login.objects.get(user=request.user)

    id = request.GET["id"]
    cart_obj = AddToCart.objects.get(id=id, user=my_p)
    new_quantity = int(quantity) - 1
    product_total = float(new_quantity) * float(cart_obj.product.offer_price)
    cart_obj.total = product_total
    cart_obj.save()
    AddToCart.objects.filter(id=id).update(quantity=new_quantity, total=product_total)
    data = {"total": cart_obj.total}
    return JsonResponse(data)


def viewcart(request):
    if request.user.is_authenticated:
        if request.user:

            my_p = Login.objects.get(user=request.user)
            sub_total = AddToCart.objects.filter(user__user=(request.user)).aggregate(Sum("total"))
            carted_item = AddToCart.objects.filter(user=my_p)

            context = {"carted_item": carted_item, "sub_total": sub_total}
            return render(request, "web/cart.html", context)
        else:
            messages.warning(request, "Login to Continue")
            return redirect("user:login")
    else:
        messages.warning(request, "Login to Continue")
        return redirect("user:login")


@csrf_exempt
def whatsappFun(request):
    messagestring = ""
    grandtotal = 0
    customer = Login.objects.get(user=request.user)
    cart_obj = AddToCart.objects.filter(user=customer)
    if Measurements.objects.filter(user=customer):
        measurement = Measurements.objects.filter(user=customer)
        print(measurement.values(), "measurement")
        for i in measurement.values():
            print(i["hip"], "measurement")
            measurement = i["hip"]
    if Size.objects.filter(user=customer):
        size = Size.objects.filter(user=customer)
        for i in size.values():
            print(i["size"], "size")
            size = i["size"]
    grandtotal = AddToCart.objects.filter(user=customer).aggregate(Sum("total"))
    rentalsecurity = 0
    for i in cart_obj:
        rentalsecurity += int(i.product.rentalsecurity)
        print(i.product.rentalsecurity)
    amount = grandtotal["total__sum"] + int(rentalsecurity)
    data = []

    if request.user is not None:
        print(request.user, "#" * 10)
        number_obj = AdminNumber.objects.all().last()
        number = number_obj.phone_number
    else:
        number = 0

    try:
        messagestring = "https://wa.me/+91" + number + "?text=Table Name :" + "Items" + "%0a------Order Details------"
        for i in cart_obj:
            data1 = {"name": i.product.product, "quantity": i.quantity, "price": i.product.price, "sub_total": i.total, "rent_security": i.product.rentalsecurity, "amount": amount}
            data.append(data1)

        for i in data:
            messagestring += (
                "%0aProduct-Name:"
                + str(i["name"])
                + "%0aQuantity:"
                + str(i["quantity"])
                + "%0aUnit-Price:"
                + str(i["price"])
                + "%0aTotal :"
                + str(i["sub_total"])
                + "%0aRent-Security :"
                + str(i["rent_security"])
                + "%0aAmount-To-Pay :"
                + str(i["amount"])
                + "%0a-----------------------------"
            )

        messagestring += (
            "%0a-----------------------------%0a\
            Grand Total :"
            + str(amount)
            + "%0a-----------------------------"
        )

        if Measurements.objects.filter(user=customer):
            measurement = Measurements.objects.filter(user=customer)
            print(measurement.values(), "measurement")
            for i in measurement.values():
                print(i["hip"], "measurement")
                messagestring += (
                    "%0aSleeve-length:"
                    + str(i["sleevelength"])
                    + "%0aChest-around:"
                    + str((i["chestaround"]))
                    + "%0aWaist-Around:"
                    + str((i["waistAround"]))
                    + "%0a-----------------------------"
                )
                messagestring += (
                    "%0aLength-Pant:"
                    + str(i["LengthTrouser"])
                    + "%0aHip:"
                    + str(i["hip"])
                    + "%0aWaist-For-Trouser:"
                    + str(i["WaistForTrouser"])
                    + "%0aThighs:"
                    + str(i["thighs"])
                    + "%0aHem:"
                    + str(i["hem"])
                )
            messagestring += "%0a-----------------------------%0a"
        else:
            messagestring += "%0a-----------------------------%0a"
        if Size.objects.filter(user=customer):
            size = Size.objects.filter(user=customer)
            for i in size.values():
                print(i["size"], "size")
                size = i["size"]
                messagestring += "%0aSize:" + str(i["size"])
                messagestring += "%0a-----------------------------%0a"
        else:
            messagestring += "%0a-----------------------------%0a"
    except Exception:
        pass
    data = {"link": messagestring}
    return JsonResponse(data)


def deletefromcart(request, id):

    user = Login.objects.get(user=request.user)
    product = AddToCart.objects.get(user=user, id=id)
    product.delete()
    messages.warning(request, "Product removed successfully...")
    return redirect("/cart")


def checkout(request):
    return render(request, "web/checkout.html")
    # if request.user.is_authenticated:
    #     if Login.objects.get(user = request.user):

    #         my_p = Login.objects.get(user=request.user)
    #         carted_item = AddToCart.objects.filter(user=my_p)

    #         context= {
    #             'carted_item':carted_item
    #         }
    #         return render(request,'web/cart.html',context)
    #     else:
    #         messages.warning(request,"Login to Continue")
    #         return redirect('user:login')
    # else:
    #         messages.warning(request,"Login to Continue")
    #         return redirect('user:login')


def about_us(request):
    context = {}
    return render(request, "web/about-us.html", context)


def blog_detail(request):
    context = {}
    return render(request, "web/blog-detail.html", context)


def blog_grid(request):
    context = {}
    return render(request, "web/blog-grid.html", context)


def blog_list(request):
    context = {}
    return render(request, "web/blog-list.html", context)


def coming_soon(request):
    context = {}
    return render(request, "web/coming-soon.html", context)


def compare(request):
    context = {}
    return render(request, "web/compare.html", context)


def contact_us(request):
    context = {}
    return render(request, "web/contact-us.html", context)


def faq(request):
    context = {}
    return render(request, "web/faq.html", context)


# def forgot(request):
#     context = {}
#     return render(request, "web/forgot.html", context)


def index_2(request):
    context = {}
    return render(request, "web/index-2.html", context)


def index_3(request):
    context = {}
    return render(request, "web/index-3.html", context)


def index_4(request):
    context = {}
    return render(request, "web/index-4.html", context)


def index_5(request):
    context = {}
    return render(request, "web/index-5.html", context)


def index_6(request):
    context = {}
    return render(request, "web/index-6.html", context)


def index_7(request):
    context = {}
    return render(request, "web/index-7.html", context)


def index_8(request):
    context = {}
    return render(request, "web/index-8.html", context)


def index_9(request):
    context = {}
    return render(request, "web/index-9.html", context)


def order_success(request):
    context = {}
    return render(request, "web/order-success.html", context)


def order_tracking(request):
    context = {}
    return render(request, "web/order-tracking.html", context)


def otp(request):
    context = {}
    return render(request, "web/otp.html", context)


def product_4_image(request):
    context = {}
    return render(request, "web/product-4-image.html", context)


def product_bottom_thumbnail(request):
    context = {}
    return render(request, "web/product-bottom-thumbnail.html", context)


def product_bundle(request):
    context = {}
    return render(request, "web/product-bundle.html", context)


def product_left_thumbnail(request):
    context = {}
    return render(request, "web/product-left-thumbnail.html", context)


def product_right_thumbnail(request):
    context = {}
    return render(request, "web/product-right-thumbnail.html", context)


def product_sticky(request):
    context = {}
    return render(request, "web/product-sticky.html", context)


def search(request):
    # query = request.GET.get('search')
    # print(search)
    # allprod = []
    # catsubcats = SubCategory.objects.values('subcategory',id)
    # cats = {item['subcategory'] for item in catsubcats}
    # for cat in cats:
    #     prodtemp=Product.objects.filter(subcategory=cat)
    kw = request.GET.get("search")
    print(kw)
    if kw:
        if Product.objects.filter(Q(product__icontains=kw) or Q(description__icontains=kw)):
            results = Product.objects.filter(Q(product__icontains=kw) | Q(description__icontains=kw))
            print(kw)
            print(results)
            context = {"results": results, "status": 1}
            return render(request, "web/search.html", context)
        else:
            messages.error(request, "No matching products found...")
            context = {"status": 0}
            return render(request, "web/search.html", context)
    else:
        return render(request, "web/search.html")


def seller_become(request):
    context = {}
    return render(request, "web/seller-become.html", context)


def seller_dashboard(request):
    context = {}
    return render(request, "web/seller-dashboard.html", context)


def seller_detail_2(request):
    context = {}
    return render(request, "web/seller-detail-2.html", context)


def seller_detail(request):
    context = {}
    return render(request, "web/seller-detail.html", context)


def seller_grid_2(request):
    context = {}
    return render(request, "web/seller-grid-2.html", context)


def seller_grid(request):
    context = {}
    return render(request, "web/seller-grid.html", context)


def shop_banner(request):
    context = {}
    return render(request, "web/shop-banner.html", context)


def shop_category_slider(request):
    context = {}
    return render(request, "web/shop-category-slider.html", context)


def shop_category(request, id):
    subcategory = SubCategory.objects.filter(id=id)
    context = {"subcategory": subcategory}
    return render(request, "web/shop-category.html", context)


def shop_list(request):
    context = {}
    return render(request, "web/shop-list.html", context)


def shop_right_sidebar(request):
    context = {}
    return render(request, "web/shop-right-sidebar.html", context)


def shop_top_filter(request):
    context = {}
    return render(request, "web/shop-top-filter.html", context)


def sign_up(request):
    if request.method == "POST":
        customer_name = request.POST.get("fullname")
        email = request.POST.get("email")
        number = request.POST.get("number")
        address = request.POST.get("address")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password == password2:
            if Login.objects.get(customer_name=customer_name):
                messages.error(request, "username is exist please enter another name...")
            else:
                temp = Login.objects.create(customer_name=customer_name, password=password, phone_number=number, email=email, address=address)
                temp.save()
        else:
            messages.error(request, "password is not matching...")

    else:
        return render(request, "web/sign-up.html")


def user_dashboard(request):
    context = {}
    return render(request, "web/user-dashboard.html", context)


def error_404(request):
    context = {}
    return render(request, "web/404.html", context)


@csrf_exempt
def size(request):
    print("size")
    id = request.GET["id"]
    size = request.GET["sizeoption"]
    product = Product.objects.get(id=id)
    print(product, "product")
    customer = Login.objects.get(user=request.user)
    Size.objects.create(user=customer, product=product, size=size)
    data = {"ff": "hgyh"}
    return JsonResponse(data)


def measurements(request, id):
    product = Product.objects.get(id=id)
    if request.user.is_authenticated:
        if Login.objects.get(user=request.user):
            customer = Login.objects.get(user=request.user)
            sleevelength = request.POST.get("sleevelength")
            chestaround = request.POST.get("chestaround")
            waistAround = request.POST.get("waistAround")
            Length = request.POST.get("Length")
            Hip = request.POST.get("Hip")
            Waist = request.POST.get("Waist")
            Thighs = request.POST.get("Thighs")
            Hem = request.POST.get("Hem")
            Measurements.objects.create(
                user=customer,
                product=product,
                sleevelength=sleevelength,
                chestaround=chestaround,
                waistAround=waistAround,
                LengthTrouser=Length,
                hip=Hip,
                WaistForTrouser=Waist,
                thighs=Thighs,
                hem=Hem,
            )
            return redirect("user:product", id)
        else:
            return redirect("user:login")
    return redirect("user:login")


@csrf_exempt
def event(request):
    date = request.GET["eventdate"]
    id = request.GET["id"]
    customer = Login.objects.get(user=request.user)
    product = Product.objects.get(id=id)
    event = Event.objects.create(user=customer, product=product, date=date)
    event.save()
    date = {"total": date}
    return JsonResponse(date)
