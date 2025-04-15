from django.db import models

class Greeting(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class Order(models.Model):
    link = models.URLField()  # Will validate proper URLs
    count = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default="registered")
    result_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.link} with count {self.count}"
