from myapp.models import Expense

from django import forms



# Create your views here.


class ExpenseForm(forms.ModelForm):

    class Meta:

        model=Expense

        fields="__all__"

        exclude=("created_date",)

        widgets={

            "title":forms.TextInput(attrs={"class":"form-control"}),

            "amount":forms.NumberInput(attrs={"class":"form-control"}),

            "category":forms.Select(attrs={"class":"form-control"}),

            "user":forms.TextInput(attrs={"class":"form-control"}),
        }




