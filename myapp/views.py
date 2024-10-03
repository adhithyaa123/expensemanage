from django.shortcuts import render,redirect

from django.contrib import messages

from myapp.forms import ExpenseForm

from myapp.models import Expense

from django.views.generic import View

from django import forms

from django.db.models import Q



class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=ExpenseForm()

        return render(request,"expense_create.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=ExpenseForm(request.POST)  

        if form_instance.save():

            form_instance.save()

            messages.success(request,"created successfully")

            return redirect("expense-create")

        else:

            messages.error(request,"failed") 

            return redirect("expense_create")


class ExpenseListView(View):

    def get(self,request,*args,**kwargs):

        search_text=request.GET.get("search_text")

        selected_category=request.GET.get("category","all")

        if selected_category =="all":

            qs=Expense.objects.all()

        else:

            qs=Expense.objects.filter(category=selected_category)        

        if search_text!=None:

            qs=Expense.objects.filter(Q(title__icontains=search_text)) 
       
        return render(request,"expense_list.html",{"expe":qs,"selected":selected_category})


class ExpenseDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Expense.objects.all(id=id)

        return render(request,"expense_detail.html",{"expen":qs})         
        

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
    

      

class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        Expense.objects.get(id=kwargs.get("pk")).delete()    

        messages.error(request,"deleted!!!!!!!!!!!!!!!")      

        return redirect("expense_list")   



