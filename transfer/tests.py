import json

from django.test import TestCase

from transfer.models import UserCard, BillRub


class SuccessTransferCase(TestCase):
    """Набор тестовых случаев успешного перевода средств."""

    def setUp(self):
        self.aleksandrov_ip = UserCard.objects.create(
            name='Иван', surname='Александров', patronymic='Петрович',
            inn='111111111111'
        )
        BillRub.objects.create(user_card=self.aleksandrov_ip, total=1000)

        self.kotov_pv = UserCard.objects.create(
            name='Котов', surname='Петр', patronymic='Вениаминович',
            inn='222222222222'
        )
        BillRub.objects.create(user_card=self.kotov_pv, total=500)

        super(SuccessTransferCase, self).setUp()

    def test_create_transfer(self):
        """Тест создания успешного перевода средств."""

        # Отправляем запрос на перевод 300 рублей с счета Александрова И.П.
        # на счет Котова П.В.
        response = self.client.post(
            '/transfer/new/',
            {
                'user': self.aleksandrov_ip.id,
                'inn': self.kotov_pv.inn,
                'transfer_sum': 300
            }
        )

        self.assertEqual(response.status_code, 302)

        aleksandrov_total = BillRub.objects.get(
            user_card=self.aleksandrov_ip).total
        kotov_total = BillRub.objects.get(user_card=self.kotov_pv).total

        self.assertEqual(aleksandrov_total, 700)
        self.assertEqual(kotov_total, 800)

    def test_create_transfer_inn(self):
        """Тест создания успешного перевода средств, на несколько ИНН."""

        # У Ивановой Н.Д. такой же ИНН как и у Котова П.В.
        self.ivanova_nd = UserCard.objects.create(
            name='Наталья', surname='Иванова', patronymic='Дмитриевна',
            inn='222222222222'
        )
        BillRub.objects.create(user_card=self.ivanova_nd, total=100)

        # Отправляем запрос на перевод 300 рублей с счета Александрова И.П.
        # на счет Котова П.В.
        response = self.client.post(
            '/transfer/new/',
            {
                'user': self.aleksandrov_ip.id,
                'inn': self.kotov_pv.inn,
                'transfer_sum': 300
            }
        )

        self.assertEqual(response.status_code, 302)

        aleksandrov_total = BillRub.objects.get(
            user_card=self.aleksandrov_ip).total
        kotov_total = BillRub.objects.get(user_card=self.kotov_pv).total
        ivanova_total = BillRub.objects.get(user_card=self.ivanova_nd).total

        self.assertEqual(aleksandrov_total, 700)
        self.assertEqual(kotov_total, 650)
        self.assertEqual(ivanova_total, 250)


class FailTransferCase(TestCase):
    """Набор тестовых случаев не проходящего перевода средств."""

    def setUp(self):
        self.aleksandrov_ip = UserCard.objects.create(
            name='Иван', surname='Александров', patronymic='Петрович',
            inn='111111111111'
        )
        BillRub.objects.create(user_card=self.aleksandrov_ip, total=1000)

        self.kotov_pv = UserCard.objects.create(
            name='Котов', surname='Петр', patronymic='Вениаминович',
            inn='222222222222'
        )
        BillRub.objects.create(user_card=self.kotov_pv, total=500)

        super(FailTransferCase, self).setUp()

    def test_create_transfer_failure_inn(self):
        """Тест создания перевода средств на некорректный ИНН."""

        # Отправляем запрос на перевод 300 рублей с счета Александрова И.П.
        # на счет Котова П.В.
        response = self.client.post(
            '/transfer/new/',
            {
                'user': self.aleksandrov_ip.id,
                'inn': 123,
                'transfer_sum': 300
            }
        )

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            content['message'], 'Длина ИНН должна быть 12 символов')

        aleksandrov_total = BillRub.objects.get(
            user_card=self.aleksandrov_ip).total
        kotov_total = BillRub.objects.get(user_card=self.kotov_pv).total

        self.assertEqual(aleksandrov_total, 1000)
        self.assertEqual(kotov_total, 500)

    def test_create_transfer_failure_no_inn(self):
        """Тест создания перевода средств, когда не найдены данные по ИНН."""

        # Отправляем запрос на перевод 300 рублей с счета Александрова И.П.
        # на счет Котова П.В.
        response = self.client.post(
            '/transfer/new/',
            {
                'user': self.aleksandrov_ip.id,
                'inn': 123456789012,
                'transfer_sum': 300
            }
        )

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            content['message'], 'Не найдены получатели с ИНН')

        aleksandrov_total = BillRub.objects.get(
            user_card=self.aleksandrov_ip).total
        kotov_total = BillRub.objects.get(user_card=self.kotov_pv).total

        self.assertEqual(aleksandrov_total, 1000)
        self.assertEqual(kotov_total, 500)

    def test_create_transfer_failure_no_bill(self):
        """Тест создания перевода средств, когда у пользователя нет счета."""

        # У Ивановой Н.Д. такой же ИНН как и у Котова П.В., но нет счета
        self.ivanova_nd = UserCard.objects.create(
            name='Наталья', surname='Иванова', patronymic='Дмитриевна',
            inn='222222222222'
        )

        # Отправляем запрос на перевод 300 рублей с счета Александрова И.П.
        # на счет Котова П.В.
        response = self.client.post(
            '/transfer/new/',
            {
                'user': self.aleksandrov_ip.id,
                'inn': 222222222222,
                'transfer_sum': 300
            }
        )

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            content['message'],
            'У пользователя {} не заведен счет'.format(self.ivanova_nd))

        aleksandrov_total = BillRub.objects.get(
            user_card=self.aleksandrov_ip).total

        self.assertEqual(aleksandrov_total, 1000)

    def test_create_transfer_failure_sum(self):
        """Тест создания перевода средств с некорректной суммой."""

        # Отправляем запрос на перевод None рублей с счета Александрова И.П.
        # на счет Котова П.В.
        response = self.client.post(
            '/transfer/new/',
            {
                'user': self.aleksandrov_ip.id,
                'inn': 222222222222,
                'transfer_sum': None
            }
        )

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            content['message'],
            'Сумма перевода должна быть больше 0 '
            'и содеражить не более 10 знаков')

        aleksandrov_total = BillRub.objects.get(
            user_card=self.aleksandrov_ip).total
        kotov_total = BillRub.objects.get(user_card=self.kotov_pv).total

        self.assertEqual(aleksandrov_total, 1000)
        self.assertEqual(kotov_total, 500)

    def test_create_transfer_failure_own_sum(self):
        """Тест создания перевода средств с некорректной суммой на счету.
        
        Когда на счету не хватает средств для перевода.
        """

        # Отправляем запрос на перевод 5000 рублей с счета Александрова И.П.
        # на счет Котова П.В., хотя на счету у Александрова И.П. 1000
        response = self.client.post(
            '/transfer/new/',
            {
                'user': self.aleksandrov_ip.id,
                'inn': 222222222222,
                'transfer_sum': 5000
            }
        )

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            content['message'],
            'На счету пользователя {} не хватает средств'.format(
                self.aleksandrov_ip))

        aleksandrov_total = BillRub.objects.get(
            user_card=self.aleksandrov_ip).total
        kotov_total = BillRub.objects.get(user_card=self.kotov_pv).total

        self.assertEqual(aleksandrov_total, 1000)
        self.assertEqual(kotov_total, 500)
