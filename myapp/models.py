from django.db import models

# Create your models here.

class Expense(models.Model):

    title=models.CharField(max_length=200)

    amount=models.IntegerField()

    created_date=models.DateTimeField(auto_now_add=True)


    category_choices=(
        ("food","food"),
        ("travel","travel"),
        ("helath","health"),
        ("others","others")
    )

    category=models.CharField(max_length=200,choices=category_choices,default="others")

    user=models.CharField(max_length=200)

    def __str__(self):

       return self.title


        