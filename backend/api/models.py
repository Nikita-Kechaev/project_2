from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from .managers import UserManager


class User(AbstractUser):
    class ROLE(models.TextChoices):
        ADMIN = "ADMIN", "Администратор",
        MODERATOR = "MODERATOR", "Модератор",
        USER = "USER", "Пользователь"
    username = None,
    email = models.EmailField(
        "Email адрес",
        unique=True,
        validators=[validators.validate_email],
        error_messages={
            "unique": "Пользователь с таким email уже существует."
        }
    )
    first_name = models.CharField("Имя", max_length=100, blank=True)
    last_name = models.CharField("Фамилия", max_length=100, blank=True)
    role = models.CharField(
        "Роль",
        max_length=60,
        choices=ROLE.choices,
        default=ROLE.USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='пользователь'
    )
    text = models.TextField(
        verbose_name='текст комментария'
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='дата публикации'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return (f'комментарий от {self.author}: {self.text[:10]}... . '
                f'создан {self.created_at}.')


class Tag(models.Model):
    text = models.CharField(
        max_length=255,
        verbose_name='тег'
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.text


class GalleryFile(models.Model):
    type = models.CharField(
        max_length=255,
        verbose_name='тип',
    )
    file = models.FileField(
        upload_to='GalleryFiles',
        verbose_name='загружаемый файл для галлереи'
    )

    class Meta:
        verbose_name = 'файл для галлереи'
        verbose_name_plural = 'файлы для галлереи'

    def __str__(self):
        return f'файл для галлереи {self.type}'


class Journal(models.Model):
    slug = models.SlugField(
        unique=True,
    )
    tags = models.ManyToManyField(
        Tag,
        through='JournalTag',
        verbose_name="Теги новостей",
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='journals',
        verbose_name='автор'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='загаловок'
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='дата публикации'
    )
    file = models.FileField(
        upload_to='JournalFiles/',
        verbose_name='файл журнала',
        blank=True
    )
    image = models.FileField(
        upload_to='JournalImages/',
        verbose_name='изображние журнала',
        blank=True
    )
    banner = models.FileField(
        upload_to='JournalBanners/',
        verbose_name='баннер журнала',
        blank=True
    )
    description = models.TextField(
        verbose_name='описние журнала'
    )
    short_description = models.TextField(
        verbose_name='краткое описание журнала'
    )
    comments = models.ManyToManyField(
        Comment,
        through='JournalComment',
        verbose_name='комментарии журнала'
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'журнал'
        verbose_name_plural = 'журналы'

    def __str__(self):
        return f'Журнал: {self.title}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("api:projects-detail", kwargs={"slug": self.slug})


class JournalComment(models.Model):
    journal = models.ForeignKey(
        Journal,
        on_delete=models.CASCADE,
        verbose_name='журнал'
        )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        verbose_name='комментарий'
    )

    class Meta:
        verbose_name = 'комментарий к журналу'
        verbose_name_plural = 'комментарии к журналу'

    def __str__(self):
        return f'комментарий к журналу: {self.comment.text[:10]}'


class JournalReview(models.Model):
    journal = models.ForeignKey(
        Journal,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='журнал'
        )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='journalreviews',
        verbose_name='пользователь'
    )
    rate = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
        verbose_name='оценка: 1 - 5'
        )

    class Meta:
        verbose_name = 'ревью к журналу'
        verbose_name_plural = 'ревью к журналу'

        constraints = [
            models.UniqueConstraint(
                fields=['journal', 'user'],
                name='unique_journal_user_review'
            )
        ]

    def __str__(self):
        return f'ревью к журналу: {self.rate} {self.journal}.'


class JournalTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'теги журналов'
        verbose_name_plural = 'теги журналов'

        unique_together = ('tag', 'journal')

    def __str__(self):
        return f'{self.tag} {self.journal}'


class Gallery(models.Model):
    slug = models.SlugField(
        unique=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='galleries',
        verbose_name='автор'
    )
    title = models.CharField(
        verbose_name='загаловок',
        max_length=255
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='дата публикации'
    )
    file = models.FileField(
        upload_to='GalleryFiles/',
        verbose_name='файл галереи'
    )
    image = models.FileField(
        upload_to='GalleryImage/',
        verbose_name='изображение',
        blank=True
    )
    photo = models.FileField(
        upload_to='GalleryPhoto/',
        verbose_name='фото',
        blank=True
    )
    banner = models.FileField(
        upload_to='GalleryBanners/',
        verbose_name='обложка',
        blank=True
    )
    video = models.FileField(
        upload_to='GalleryVideo/',
        verbose_name='видео',
        blank=True
    )
    short_description = models.TextField(
        verbose_name='описние галереи'
    )
    soft = models.CharField(
        max_length=255,
        verbose_name='софт',
        blank=True
    )
    type = models.CharField(
        max_length=255,
        verbose_name='тип',
        blank=True
    )
    comments = models.ManyToManyField(
        Comment,
        through='GalleryComment',
        verbose_name='комментарии галереи'
        )

    class Meta:
        verbose_name = 'галерея'
        verbose_name_plural = 'галереи'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Галерея: {self.title}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("api:projects-detail", kwargs={"slug": self.slug})


class GalleryComment(models.Model):
    gallery = models.ForeignKey(
        Gallery,
        on_delete=models.CASCADE,
        verbose_name='галерея'
        )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        verbose_name='комментарий'
    )

    class Meta:
        verbose_name = 'комментарий к галерее'
        verbose_name_plural = 'комментарии к галерее'

    def __str__(self):
        return f'комментарий к галерее: {self.comment.text[:10]}'


class GalleryReview(models.Model):
    gallery = models.ForeignKey(
        Gallery,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='журнал'
        )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='galleryreviews',
        verbose_name='пользователь'
    )
    rate = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
        verbose_name='оценка: 1 - 5'
        )

    class Meta:
        verbose_name = 'ревью к галерее'
        verbose_name_plural = 'ревью к галерее'

        constraints = [
            models.UniqueConstraint(
                fields=['gallery', 'user'],
                name='unique_gallery_user_review'
            )
        ]

    def __str__(self):
        return f'ревью к галерее: {self.rate} {self.gallery}.'


class New(models.Model):
    slug = models.SlugField(
        unique=True,
    )
    tags = models.ManyToManyField(
        Tag,
        through='NewTag',
        verbose_name="Теги новостей"
    )
    title = models.CharField(
        verbose_name='загаловок',
        max_length=255
    )
    heading = models.CharField(
        verbose_name='рубрика',
        max_length=255
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='дата публикации',
    )
    banner = models.FileField(
        upload_to='NewBanners/',
        verbose_name='баннер новости',
        blank=True
    )
    description = models.TextField(
        verbose_name='описние новости'
    )
    soft = models.CharField(
        max_length=255,
        verbose_name='софт',
        blank=True
    )
    comments = models.ManyToManyField(
        Comment,
        through='NewComment',
        verbose_name='комментарии новости'
        )

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'новость: {self.title}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("api:projects-detail", kwargs={"slug": self.slug})


class NewComment(models.Model):
    new = models.ForeignKey(
        New,
        on_delete=models.CASCADE,
        verbose_name='новость'
        )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        verbose_name='комментарий'
    )

    class Meta:
        verbose_name = 'комментарий к новости'
        verbose_name_plural = 'комментарии к новости'

    def __str__(self):
        return f'комментарий к новости: {self.comment.text[:10]}'


class NewReview(models.Model):
    new = models.ForeignKey(
        New,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='новость'
        )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='newreviews',
        verbose_name='пользователь'
    )
    rate = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
        verbose_name='оценка: 1 - 5'
        )

    class Meta:
        verbose_name = 'ревью к галерее'
        verbose_name_plural = 'ревью к новости'

        constraints = [
            models.UniqueConstraint(
                fields=['new', 'user'],
                name='unique_new_user_review'
            )
        ]

    def __str__(self):
        return f'ревью к новости: {self.rate} {self.new}.'


class NewTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    new = models.ForeignKey(New, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Теги новости'
        verbose_name_plural = 'Теги новостей'

        unique_together = ('tag', 'new')

    def __str__(self):
        return f'{self.tag} {self.new}'
