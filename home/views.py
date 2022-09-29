from contextlib import nullcontext
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView

class IndexView(ListView):
    queryset = nullcontext
    template_name = 'home/index.html'

    method_decorator(csrf_protect)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context
