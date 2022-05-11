from dataclasses import field
from re import template
from django.http import HttpResponseRedirect
from .models import Review
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from products.models import Product


# Create your views here.


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = r"reviews/add_review.html"
    fields = ['stars', 'comment']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(
            id=self.kwargs['pk']
        )
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = Product.objects.get(
            id=self.kwargs['pk']
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        product = Product.objects.get(
            id=self.kwargs['pk']
        )
        return product.get_absolute_url() + '#' + str(self.object.id)


class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review

    def post(self, request, *args, **kwargs):
        review_id = self.kwargs['pk']
        review = Review.objects.get(
            id=review_id
        )
        product = review.product
        review.delete()
        return HttpResponseRedirect(product.get_absolute_url())

    def test_func(self):
        review_id = self.kwargs['pk']
        review = Review.objects.get(
            id=review_id
        )
        return self.request.user == review.user


class EditReviewView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['stars', 'comment']
    template_name = r'reviews/add_review.html'

    def test_func(self):
        review_id = self.kwargs['pk']
        review = Review.objects.get(
            id=review_id
        )
        return self.request.user == review.user

    def get_success_url(self):
        product = Product.objects.get(
            id=self.kwargs['product_pk']
        )
        return product.get_absolute_url() + '#' + str(self.object.id)



