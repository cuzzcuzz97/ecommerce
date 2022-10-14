from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderedItem, Order, LABEL_CHOICES, CATEGORY_CHOICE 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

class HomeView(ListView):
    model = Item
    # paginate_by = 10
    template_name = 'core/home.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['category_list'] = CATEGORY_CHOICE
        cate = self.request.GET.get('category')
        values = []
        for key, value in CATEGORY_CHOICE:
            values.append(key)
        if cate in values:
            context['object_list'] = Item.objects.filter(category=cate)
        return context

class ItemDetailView(DetailView):
    model = Item
    template_name = 'core/product.html'

class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered =False)
            context = {
                'object': order,
            }
            return render(self.request, 'core/order-summary.html', context)
        except ObjectDoesNotExist:
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderedItem.objects.get_or_create(
        item = item,
        ordered = False,
        user = request.user,
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            # return success added quantity . 
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            # return success added item 
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date,)
        order.items.add(order_item)
        #
        return redirect("core:order-summary")

@login_required
def increase_quantity(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderedItem.objects.get_or_create(
    item = item,
    ordered = False,
    user = request.user,)
    order_item.quantity += 1
    order_item.save()
    # return success added quantity . 
    return redirect("core:order-summary")

@login_required
def decrease_quantity(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderedItem.objects.get_or_create(
    item = item,
    ordered = False,
    user = request.user,)
    order_item.quantity -= 1
    if order_item.quantity == 0:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        order = order_qs[0]
        order.items.remove(order_item)
    else:
        order_item.save()
    # return success added quantity . 
    return redirect("core:order-summary")

@login_required
def delete_item(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderedItem.objects.get_or_create(
    item = item,
    ordered = False,
    user = request.user,)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    order_item.quantity = 1
    order_item.save()
    order.items.remove(order_item)

    return redirect("core:order-summary")

