from django.db import models


class Kind(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    id = models.BigIntegerField(primary_key=True)
    brand = models.CharField(max_length=255)

    def __str__(self):
        return f"Brand: {self.brand}"


class Card(models.Model):
    id = models.BigIntegerField(primary_key=True)
    brand = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} - {self.name}"


class Color(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Color: {self.name}"


class ColorVariant(models.Model):
    id = models.BigIntegerField(primary_key=True)
    card = models.ForeignKey(Card, related_name='color_variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    colors = models.ManyToManyField(Color, related_name='colors')
    kinds = models.ManyToManyField(Kind, related_name='kinds', blank=True)
    desc = models.TextField(blank=True)
    grouped_options = models.TextField(blank=True)
    pics = models.IntegerField()
    price = models.IntegerField(null=True, blank=True)
    total_quantity = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=False)
    img_main = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Card ID: {self.card.id})"


class ProductItem(models.Model):
    id = models.BigIntegerField(primary_key=True)
    color_variant = models.ForeignKey(ColorVariant, related_name='sizes', on_delete=models.CASCADE)
    size_name = models.CharField(max_length=50)
    orig_name = models.CharField(max_length=50)
    optionId = models.CharField(max_length=50)
    price = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.size_name} - {self.price} ₽"

