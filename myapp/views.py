from django.shortcuts import render,redirect

from django.contrib import messages

from myapp.forms import ExpenseForm,RegisterForm,LoginForm

from myapp.models import Expense

from django.views.generic import View

from django import forms

from django.db.models import Q

from django.contrib.auth.models import User

from django.db.models import Count

from django.contrib.auth import authenticate,login,logout

from myapp.decorators import signin_required

from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache

decs=[signin_required,never_cache]



@method_decorator(decs,name="dispatch")

class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=ExpenseForm()

        return render(request,"expense_create.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=ExpenseForm(request.POST)

        form_instance.instance.user=request.user  

        if form_instance.save():

            form_instance.save()

            messages.success(request,"created successfully")

            return redirect("expense-create")

        else:

            messages.error(request,"failed") 

            return redirect("expense_create")

@method_decorator(decs,name="dispatch")

class ExpenseListView(View):

    def get(self,request,*args,**kwargs):

        search_text=request.GET.get("search_text")

        selected_category=request.GET.get("category","all")

        if selected_category =="all":

            qs=Expense.objects.filter(user=request.user)

        else:

            qs=Expense.objects.filter(category=selected_category,user=request.user)        

        if search_text!=None:

            qs=Expense.objects.filter(user=request.user)

            qs=Expense.objects.filter(Q(title__icontains=search_text)) 
       
        return render(request,"expense_list.html",{"expe":qs,"selected":selected_category})

@method_decorator(decs,name="dispatch")

class ExpenseDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Expense.objects.all(id=id)

        return render(request,"expense_detail.html",{"expen":qs})         
        
@method_decorator(decs,name="dispatch")

class ExpenseUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expen_obj=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=expen_obj)

        return render(request,"expense_update.html",{"form":form_instance})


    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expen_obj=Expense.objects.get(id=id)

        form_instance=ExpenseForm(request.POST,instance=expen_obj)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"updation sucessfullyyyyyy")

            return redirect("expense_list")

        else:

            messages.error(request,"updation failedddd")

            return render(request,"exepnse_update.html",{"form":form_instance})  
    

@method_decorator(decs,name="dispatch")

class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Expense.objects.all()

        total_expense_count=qs.count()
        
        category_summary=Expense.objects.all().values("category").annotate(cat_count=Count("category"))

        print(category_summary)

        context={

            "total_expense_count":total_expense_count,

            "category_summary":category_summary
        }

        return render(request,"expense_summary.html",context)



@method_decorator(decs,name="dispatch")

class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        Expense.objects.get(id=kwargs.get("pk")).delete()    

        messages.error(request,"deleted!!!!!!!!!!!!!!!")      

        return redirect("expense_list")   


class SignUpView(View):

    template_name="register.html"

    def get(self,request,*args,**kwargs):

        form_instance=RegisterForm()

        return render(request,self.template_name,{"form":form_instance})  

    def post(self,request,*args,**kwargs):

        print(request.POST)

        form_instance=RegisterForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            return redirect("login")   

        else:

            print("here ")

            return render(request,self.template_name,{"form":form_instance})     
    



class SignInView(View):

    template_name="login.html"

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,self.template_name,{"form":form_instance})


    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")

            pswd=form_instance.cleaned_data.get("password")

            user_obj=authenticate(request,username=uname,password=pswd)  

            if user_obj:

                login(request,user_obj)

                return redirect("expense_list") 

        return render(request,self.template_name,{"form":form_instance}) 

@method_decorator(decs,name="dispatch")

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request) 

        return redirect("login")               



        