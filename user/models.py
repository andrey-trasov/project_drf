from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None  # обязательные параметры

    email = models.EmailField(unique=True, verbose_name="Email")  # поле для авторизации
    phone = models.CharField(
        max_length=50,
        verbose_name="Телефон",
        help_text="Введите свой телефон",
        blank=True,
        null=True,
    )
    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите свой аватар",
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        help_text="Введите свой город проживания",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"  # обязательные параметры, поле для авторизации
    REQUIRED_FIELDS = []  # обязательные параметры

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    method_choices = [
        ("CASH", "Наличными"),
        ("TRANSFER", "Перевод на счет"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    date_payment = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата оплаты", **NULLABLE
    )
    paid_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс"
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок"
    )
    payment_sum = models.PositiveIntegerField(verbose_name="Cумма платежа")
    payment_method = models.CharField(
        max_length=50, choices=method_choices, verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user} - {self.paid_course}"
