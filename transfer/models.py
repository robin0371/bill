from django.db import models


class UserCard(models.Model):
    """Карточка пользователя."""

    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)
    patronymic = models.CharField('Отчество', max_length=50)
    inn = models.CharField('ИНН', max_length=12)

    class Meta:
        db_table = 'user_card'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return '{self.surname} {self.name} {self.patronymic}'.format(self=self)


class BillRub(models.Model):
    """Счет в рублях."""

    user_card = models.OneToOneField(UserCard, verbose_name='Пользователь')
    total = models.DecimalField(
        'Счет в рублях', max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'bill_rub'
        verbose_name = 'Счет в рублях'
        verbose_name_plural = 'Счета в рублях'

    def __str__(self):
        return '{self.user_card}: {self.total}'.format(self=self)
