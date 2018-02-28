from django.db import models


# class Category(models.Model):
#     category = models.CharField(max_length=30)
#
#     def __str__(self):
#         return self.category


class List(models.Model):
    todo_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    complete = models.BooleanField(default='false')
    private_id = models.IntegerField(unique=True)
    user_name = models.CharField(max_length=30)
    # category = models.ManyToManyField(Category)

    def __str__(self):
        return self.todo_text
