from django.db import models

from myproject import settings

NULLABLE = {"null": True, "blank": True}


class Course(models.Model):
    name = models.CharField(verbose_name="название", max_length=150)
    preview = models.ImageField(
        upload_to="product/photo", verbose_name="превью", **NULLABLE
    )
    description = models.TextField(verbose_name="описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(verbose_name="название", max_length=150)
    description = models.TextField(verbose_name="описание")
    preview = models.ImageField(
        upload_to="product/photo", verbose_name="превью", **NULLABLE
    )
    link_to_video = models.CharField(
        max_length=150,
        **NULLABLE,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )
    course = models.ForeignKey(
        Course, verbose_name="курс", on_delete=models.CASCADE, related_name="lessons"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Пользователь"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="Курс")

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
