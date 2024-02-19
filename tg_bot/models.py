from django.db import models


class TgBot(models.Model):
    tg_id = models.BigIntegerField(
        verbose_name='tg_id'
    )
    name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=225,
    )
    username = models.CharField(
        verbose_name='Username пользователя',
        max_length=225,
        null=True
    )
    phone = models.CharField(
        'Номер телефона',
        max_length=18,
        # unique=True
        null=True
    )
    get_bonus = models.BooleanField(
        verbose_name='Получил бонус',
        null=True, blank=True, default=False
    )

    def __str__(self):
        return f'#{self.tg_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ["name"]

