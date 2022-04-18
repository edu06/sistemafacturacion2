from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout
from usuarios.forms import formulariologin
from django.http import HttpResponseRedirect

class Login(FormView):
    template_name='login.html'
    form_class = formulariologin
    success_url= reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self,request,*args,**kwargs): # Metodo que valida o verifica el metodo o la peticion a la cual sera delegada.
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,**kwargs)

    def form_valid(self,form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)
    
def logoutusuario(request):
    logout(request)
    return HttpResponseRedirect('/')

