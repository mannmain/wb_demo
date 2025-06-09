from django.db.models import Q, OuterRef, Subquery, F
from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import ColorVariant, Brand, Color, Kind
from .paginations import ColorVariantPagination
from .serializers import ColorVariantSerializer, ColorSerializer, BrandSerializer, KindSerializer, \
    ColorVariantDetailsSerializer
from .filters import ColorVariantFilter


class KindViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Kind.objects.all().order_by('name')
    serializer_class = KindSerializer


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all().order_by('brand')
    serializer_class = BrandSerializer


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.all().order_by('name')
    serializer_class = ColorSerializer


class ColorVariantViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # queryset = ColorVariant.objects.all()

    serializer_class = ColorVariantSerializer
    pagination_class = ColorVariantPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ColorVariantFilter
    ordering_fields = ['name', 'card__brand', 'price']
    search_fields = ['name', 'card__brand']

    def get_queryset(self):
        base_qs = ColorVariant.objects.all().annotate(
            brand=F('card__brand')
        )
        search = self.request.query_params.get('search')
        if search:
            base_qs = base_qs.filter(
                Q(name__icontains=search) |
                Q(card__brand__icontains=search)
            )

        filterset = self.filterset_class(self.request.GET, queryset=base_qs)
        if not filterset.is_valid():
            return ColorVariant.objects.none()

        filtered_qs = filterset.qs

        subquery = ColorVariant.objects.filter(
            card=OuterRef('card')
        ).order_by(F('price').asc(nulls_last=True)).values('id')[:1]

        qs = filtered_qs.filter(id__in=Subquery(subquery))

        ordering = self.request.query_params.get('ordering')
        if ordering:
            qs = qs.order_by(ordering)

        return qs


class ColorVariantDetailsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ColorVariant.objects.all()

    serializer_class = ColorVariantDetailsSerializer