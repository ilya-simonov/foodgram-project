from django_filters import rest_framework as filter

from recipes.models import Tag, Recipe
from users.models import User


class TagsFilter(filter.FilterSet):
    tags = filter.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    author = filter.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filter.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filter.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(in_favorite__user=self.request.user)
        return queryset.exclude(in_favorite__user=self.request.user)

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(in_shopping_cart__user=self.request.user)
        return queryset.exclude(in_shopping_cart__user=self.request.user)
