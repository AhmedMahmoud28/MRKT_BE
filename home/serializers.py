from rest_framework import serializers
from home import models

class StoreCategoryserializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreCategory
        fields = ['name', 'image']

class Storeserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = ['name', 'image']

class ProductCategoryserializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = ['name', 'image']

class Brandserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ['name', 'image']

class Productserializer(serializers.ModelSerializer):
    # store= serializers.StringRelatedField(many=True) # return manytomany related field name(string)
    # category = ProductCategoryserializer(many=False)
    
    class Meta:
        model = models.Product
        fields = ['name', 'image', 'final_price', 'brand']
    
        
    def to_representation(self, instance): # to change representation of related fields
        represent = super(Productserializer, self).to_representation(instance)
        # represent['category'] = instance.category.name
        represent['brand'] = instance.brand.name
        # represent['store'] = Storeserializer(instance.store.all(), many=True).data # return manytomany field with base instances in model
        return represent