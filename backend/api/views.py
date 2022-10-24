from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core import serializers


from .models import Comment, Gallery, Journal, New
from .serializers import (GalleryCreateSerializer, GalleryDetailSerializer,
                          GalleryListSerializer, GalleryReviewSerializer,
                          JournalCreateSerializer, JournalDetailSerializer,
                          JournalListSerializer, JournalReviewSerializer,
                          NewCreateSerializer, NewDetailSerializer,
                          NewListSerializer, NewReviewSerializer, CommentSerializer)


class NewViewSet(viewsets.GenericViewSet):
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = New.objects.all()

        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(created_at=date)

        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(newtags__tag__text__in=tags)

        rating = self.request.query_params.get("rating")
        if rating:
            queryset = queryset.filter(rating=rating)

        order = self.request.query_params.getlist("order")
        if order:
            if 'date' in order:
                queryset = queryset.order_by('created_at')
            if 'rating' in order:
                queryset = queryset.order_by('rating')
            if 'comments' in order:
                queryset = queryset.order_by('comments')

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return NewListSerializer
        elif self.action == 'retrieve':
            return NewDetailSerializer
        elif self.action == 'create':
            return NewCreateSerializer
        elif self.action == 'rating':
            return NewReviewSerializer

    def list(self, request):
        serializer = self.get_serializer_class()
        qs = self.get_queryset()
        serializer = serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug=None):
        serializer = self.get_serializer_class()
        news = self.get_object()
        serializer = serializer(news)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data.copy()
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST'],
        url_name='comments',
        url_path='comments'
    )
    def comments(self, request, slug=None):
        user, new, text = request.user, self.get_object(), request.POST['text']
        comment = Comment.objects.create(author=user, text=text)
        new.comments.add(comment)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST'],
        url_name='rating',
        url_path='rating'
    )
    def rating(self, request, slug=None):
        data = request.data.copy()
        data['user'], data['new'] = request.user.id, self.get_object().id
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GalleryViewSet(viewsets.GenericViewSet):
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Gallery.objects.all()

        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(created_at=date)

        #  tags указаны в фильтрции, но в структуре БД их нет.

        rating = self.request.query_params.get("rating")
        if rating:
            queryset = queryset.filter(rating=rating)

        order = self.request.query_params.getlist("order")
        if order:
            if 'date' in order:
                queryset = queryset.order_by('created_at')
            if 'rating' in order:
                queryset = queryset.order_by('rating')
            if 'comments' in order:
                queryset = queryset.order_by('comments')

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return GalleryListSerializer
        elif self.action == 'create':
            return GalleryCreateSerializer
        elif self.action == 'retrieve':
            return GalleryDetailSerializer
        elif self.action == 'rating':
            return GalleryReviewSerializer

    def list(self, request):
        serializer = self.get_serializer_class()
        qs = self.get_queryset()
        serializer = serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data.copy()
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, slug=None):
        serializer = self.get_serializer_class()
        gallery = self.get_object()
        serializer = serializer(gallery)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['POST'],
        url_name='comments',
        url_path='comments'
    )
    def comments(self, request, slug=None):
        user, gallery, text = request.user, self.get_object(), request.POST['text']
        comment = Comment.objects.create(author=user, text=text)
        gallery.comments.add(comment)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST'],
        url_name='rating',
        url_path='rating'
    )
    def rating(self, request, slug=None):
        data = request.data.copy()
        data['user'], data['gallery'] = request.user.id, self.get_object().id
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JornalViewSet(viewsets.GenericViewSet):
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Journal.objects.all()

        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(created_at=date)

        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(newtags__tag__text__in=tags)

        rating = self.request.query_params.get("rating")
        if rating:
            queryset = queryset.filter(rating=rating)

        order = self.request.query_params.getlist("order")
        if order:
            if 'date' in order:
                queryset = queryset.order_by('created_at')
            if 'rating' in order:
                queryset = queryset.order_by('rating')
            if 'comments' in order:
                queryset = queryset.order_by('comments')

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return JournalListSerializer
        elif self.action == 'retrieve':
            return JournalDetailSerializer
        elif self.action == 'create':
            return JournalCreateSerializer
        elif self.action == 'rating':
            return JournalReviewSerializer

    def list(self, request):
        serializer = self.get_serializer_class()
        qs = self.get_queryset()
        serializer = serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data.copy()
        serializer = self.get_serializer_class()
        data['author'] = self.request.user.id
        serializer = serializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, slug=None):
        serializer = self.get_serializer_class()
        gallery = self.get_object()
        serializer = serializer(gallery)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['POST'],
        url_name='comments',
        url_path='comments'
    )
    def comments(self, request, slug=None):
        user, journal, text = request.user, self.get_object(), request.POST['text']
        comment = Comment.objects.create(author=user, text=text)
        journal.comments.add(comment)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST'],
        url_name='rating',
        url_path='rating'
    )
    def rating(self, request, slug=None):
        data = request.data.copy()
        data['user'], data['journal'] = request.user.id, self.get_object().id
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
