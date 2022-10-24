from django.db.models import Avg
from djoser.serializers import (UserCreatePasswordRetypeSerializer,
                                UserSerializer)
from rest_framework import serializers

from .models import (Comment, Gallery, GalleryReview, Journal, JournalReview,
                     New, NewReview, NewTag, Tag, User)


class CustomUserSerializer(UserSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class CustomUserCreateSerializer(UserCreatePasswordRetypeSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['text', ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'author',
            'text',
        ]


class NewListSerializer(serializers.ModelSerializer):
    count_comments = serializers.IntegerField(source="comments.count")
    count_reviews = serializers.IntegerField(source="reviews.count")
    rating = serializers.SerializerMethodField()

    class Meta:
        model = New
        fields = [
            'id', 'title',
            'slug', 'description',
            'banner', 'count_comments',
            'count_reviews', 'rating'
            ]

    def get_rating(self, obj):
        qs = obj.reviews
        try:
            return int(qs.aggregate(rating=Avg('rate')).get('rating'))
        except:
            return 0


class NewCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    slug = serializers.SlugField(required=False)

    class Meta:
        model = New
        fields = [
            'id', 'slug', 'title', 'description', 'heading',
            'tags'
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        new = New.objects.create(**validated_data)
        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(**tag)
            NewTag.objects.get_or_create(
                tag=current_tag,
                new=new
            )
        return new


class NewDetailSerializer(serializers.ModelSerializer):
    count_comments = serializers.IntegerField(source="comments.count")
    count_reviews = serializers.IntegerField(source="newreviews.count")
    comments = CommentSerializer(many=True, read_only=True)
    tags = serializers.StringRelatedField(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = New
        fields = [
            'id', 'title',
            'slug', 'description',
            'banner', 'count_comments',
            'count_reviews', 'comments', 'tags', 'rating'
            ]

    def get_rating(self, obj):
        qs = obj.newreviews
        try:
            return int(qs.aggregate(rating=Avg('rate')).get('rating'))
        except:
            return 0


class NewReviewSerializer(serializers.ModelSerializer):
    rate = serializers.IntegerField(required=True)

    class Meta:
        model = NewReview
        fields = [
            'new', 'user', 'rate'
        ]


class GalleryListSerializer(serializers.ModelSerializer):
    count_comments = serializers.IntegerField(source="comments.count")
    count_reviews = serializers.IntegerField(source="reviews.count")
    author = serializers.StringRelatedField(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = [
            'id', 'author', 'title', 'slug', 'short_description',
            'count_comments', 'count_reviews', 'image', 'rating'
        ]

    def get_rating(self, obj):
        qs = obj.reviews
        try:
            return int(qs.aggregate(rating=Avg('rate')).get('rating'))
        except:
            return 0


class GalleryCreateSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Gallery
        fields = [
            'title', 'short_description', 'type', 'soft',
            'rating', 'banner', 'photo', 'video', 'author', 'slug'
        ]


class GalleryDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = '__all__'

    def get_rating(self, obj):
        qs = obj.galleryreviews
        try:
            return int(qs.aggregate(rating=Avg('rate')).get('rating'))
        except:
            return 0


class GalleryReviewSerializer(serializers.ModelSerializer):
    rate = serializers.IntegerField(required=True)

    class Meta:
        model = GalleryReview
        fields = [
            'gallery', 'user', 'rate'
        ]


class JournalListSerializer(serializers.ModelSerializer):
    count_comments = serializers.IntegerField(source="comments.count")
    count_reviews = serializers.IntegerField(source="reviews.count")
    author = serializers.StringRelatedField(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Journal
        fields = [
            'id', 'author', 'title', 'slug', 'short_description',
            'count_comments', 'count_reviews', 'image', 'rating'
        ]

    def get_rating(self, obj):
        qs = obj.reviews
        try:
            return int(qs.aggregate(rating=Avg('rate')).get('rating'))
        except:
            return 0


class JournalCreateSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Journal
        fields = [
            'title', 'short_description', 'description', 'rating',
            'banner', 'file', 'image', 'author', 'slug'
        ]


class JournalDetailSerializer(serializers.ModelSerializer):
    count_comments = serializers.IntegerField(source="comments.count")
    tags = serializers.StringRelatedField(many=True)
    author = serializers.StringRelatedField(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Journal
        fields = [
            'id', 'title',
            'slug', 'author',
            'count_comments',
            'image', 'tags'
            ]

    def get_rating(self, obj):
        qs = obj.journalreviews
        try:
            return int(qs.aggregate(rating=Avg('rate')).get('rating'))
        except:
            return 0


class JournalReviewSerializer(serializers.ModelSerializer):
    rate = serializers.IntegerField(required=True)

    class Meta:
        model = JournalReview
        fields = [
            'journal', 'user', 'rate'
        ]
