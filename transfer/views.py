import json

from django.db.transaction import atomic
from django.http import HttpResponse
from django.views.generic import FormView

from transfer.forms import TransferForm
from transfer.models import UserCard, BillRub


class CreateTransfer(FormView):
    """Представление создания денежного перевода."""

    form_class = TransferForm
    template_name = 'transfer_form.html'
    success_url = '/transfer/success'

    @atomic
    def form_valid(self, form):
        user = form.cleaned_data['user']
        inn = form.cleaned_data['inn']
        transfer_sum = form.cleaned_data['transfer_sum']

        users_cards = UserCard.objects.filter(inn=inn)

        # Разделяем сумму, на количество найденных счетов для перевода
        transfer_summa = transfer_sum / users_cards.count()

        # Переводим средства на счета
        for bill in BillRub.objects.filter(user_card__in=users_cards):
            bill.total += transfer_summa
            bill.save()

        # Обновляем счет отправителя
        user.billrub.total = user.billrub.total - transfer_sum
        user.billrub.save()

        return super(CreateTransfer, self).form_valid(form)

    def form_invalid(self, form):
        messages = '\n'.join(
            [error.message for error in form.errors['__all__'].as_data()])
        return HttpResponse(
            json.dumps({
                'success': 'false',
                'message': messages
            }),
            content_type='application/json')


def transfer_success(request):
    """Представление успешного создания денежного перевода."""
    return HttpResponse(
        json.dumps({
            'success': 'true',
            'message': 'Перевод выполнен успешно'
        }),
        content_type='application/json')
