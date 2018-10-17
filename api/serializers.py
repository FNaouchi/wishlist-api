from rest_framework import serializers
from items.models import Item, FavoriteItem
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description']


class FavItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = FavoriteItem
        fields = ['user']


class ItemListSerializer(serializers.ModelSerializer):
    fav = serializers.SerializerMethodField()
    detail = serializers.HyperlinkedIdentityField(
        view_name = "api-detail",
        lookup_field = "id",
        lookup_url_kwarg = "item_id"
        )
    class Meta:
        model = Item
        fields = [
            'name',
            'description',
            'added_by',
            'fav',
            'detail',
            ]
    def get_fav(self, obj):
        return obj.favoriteitem_set.count()

class ItemDetailSerializer(serializers.ModelSerializer):
    faved_by = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = [
                'faved_by'
            ]
    def get_faved_by(self, obj):
        faved = obj.favoriteitem_set.all()
        return FavItemSerializer(faved, many=True).data