from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Customer(models.Model):
    customer_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

class CustomerInfo(models.Model):
    customer_id = models.CharField(max_length=200)
    customer_info = models.CharField(max_length=200)

class CustomerHistory(models.Model):
    customer_id = models.CharField(max_length=200)
    customer_history = models.CharField(max_length=200)
