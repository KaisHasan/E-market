from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect


class ResetView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request.user.reset()
        return redirect('account-info')



class AccountInfoView(TemplateView):
    template_name = 'accounts/account.html'

