import json

from django.db import models
from rest_framework import serializers
from .models import Card, ColorVariant, ProductItem, Color, Brand, Kind


class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kind
        fields = ['id', 'name']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'brand']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name']


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = ['id', 'size_name', 'orig_name', 'price']


class ColorVariantSerializer(serializers.ModelSerializer):
    kinds = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    brand = serializers.CharField(source='card.brand', read_only=True)
    color_name = serializers.SerializerMethodField()

    class Meta:
        model = ColorVariant
        fields = ['id', 'card', 'brand', 'name', 'color_name', 'img_main', 'price', 'kinds']

    def get_color_name(self, obj):
        return ";".join([color.name for color in obj.colors.all()])


class ColorVariantDetailsSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='card.brand', read_only=True)
    color_name = serializers.SerializerMethodField()
    other_colors = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    grouped_options = serializers.SerializerMethodField()

    class Meta:
        model = ColorVariant
        fields = ['id', 'card', 'brand', 'name', 'color_name', 'img_main', 'price', 'sizes', 'other_colors', 'desc', 'grouped_options']

    def get_color_name(self, obj):
        return ";".join([color.name for color in obj.colors.all()])

    def get_grouped_options(self, obj):
        return json.loads(obj.grouped_options)

    def get_sizes(self, obj):
        sizes_qs = obj.sizes.all()
        return [
            {
                'id': size.id,
                'size_name': size.size_name,
                'orig_name': size.orig_name,
                'price': size.price,
                'quantity': size.quantity,
                'in_stock': size.in_stock,
            }
            for size in sizes_qs
        ]

    def get_other_colors(self, obj):
        variants = ColorVariant.objects.filter(card=obj.card).exclude(id=obj.id)

        result = [{
            'id': obj.id,
            'name': obj.name,
            'color_name': self.get_color_name(obj),
            'img_main': obj.img_main,
            'total_quantity': obj.total_quantity,
            'in_stock': obj.in_stock,
        }]

        result += [
            {
                'id': variant.id,
                'name': variant.name,
                'color_name': ";".join([color.name for color in variant.colors.all()]),
                'img_main': variant.img_main,
                'total_quantity': variant.total_quantity,
                'in_stock': variant.in_stock,
            }
            for variant in variants
        ]

        return result


class CardSerializer(serializers.ModelSerializer):
    variant = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ['id', 'brand', 'name']
