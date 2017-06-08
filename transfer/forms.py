from django import forms

from transfer.models import UserCard


class TransferForm(forms.Form):
    """Форма перевода денежных средств."""

    user = forms.ModelChoiceField(
        label='Отправитель', queryset=UserCard.objects.all())
    inn = forms.CharField(
        label='ИНН получателей', max_length=12, min_length=12)
    transfer_sum = forms.DecimalField(
        label='Сумма перевода', max_digits=12, decimal_places=2)

    def clean(self):
        cleaned_data = super(TransferForm, self).clean()
        user = cleaned_data.get('user')
        inn = cleaned_data.get('inn')
        transfer_sum = cleaned_data.get('transfer_sum')

        if not inn or len(inn) != 12:
            raise forms.ValidationError('Длина ИНН должна быть 12 символов')

        receivers = UserCard.objects.filter(inn=inn)
        if not receivers.exists():
            raise forms.ValidationError(
                'Не найдены получатели с ИНН'.format(inn))

        for receiver in receivers:
            if getattr(receiver, 'billrub', None) is None:
                raise forms.ValidationError(
                    'У пользователя {} не заведен счет'.format(receiver))

        if not transfer_sum or transfer_sum < 0:
            raise forms.ValidationError(
                'Сумма перевода должна быть больше 0 '
                'и содеражить не более 10 знаков')

        if transfer_sum > user.billrub.total:
            raise forms.ValidationError(
                'На счету пользователя {} не хватает средств'.format(user))
