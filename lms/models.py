from django.db import models

NULLABLE = {"null": True, "blank": True}


class Course(models.Model):
    name = models.CharField(verbose_name="название", max_length=150)
    preview = models.ImageField(
        upload_to="product/photo", verbose_name="превью", **NULLABLE
    )
    description = models.TextField(verbose_name="описание")

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
    course = models.ForeignKey(Course, verbose_name="курс", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
