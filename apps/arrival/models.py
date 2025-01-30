from django.db import models


# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Declaration(models.Model):
    # Порядок полей соответствует порядку столбцов в DBF

    # Внешний ключ (не из DBF)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True
    )

    # G011 / Код типа таможенной декларации
    type_code = models.CharField(max_length=3)
    # G012_1 / Вид таможенной декларации
    type = models.CharField(max_length=3)
    # G022 / Компания отправитель
    sender = models.CharField(max_length=38)
    # G023 / Адрес компании отправителя
    sender_address = models.CharField(max_length=250)
    # G20 / Краткое наименование условия поставки
    delivery_terms = models.CharField(max_length=3)
    # G21 (пропущено, так как нет данных)
    # G05 / Общее количество наименований товаров
    item_count = models.IntegerField()
    # G082 / Получатель
    receiver = models.CharField(max_length=38)
    # G083 / Адрес получателя
    receiver_address = models.CharField(max_length=250)
    # G15A / Код страны отправления
    sender_country_code = models.CharField(max_length=3)
    # G15A_0 / Буквенный код страны
    sender_alpha_country_code = models.CharField(max_length=2)
    # G15A_1 / ???(000 в примере)
    g15A_1 = models.CharField(max_length=4)
    # G17A, G17A_0, G17A_1 (пропущены, так как нет данных)
    # G221 / Код валюты платежа
    payment_currency_code = models.CharField(max_length=3)
    # G222 / Общая фактурная стоимость
    total_cost = models.DecimalField(max_digits=19, decimal_places=4)
    # G23 / Курс иностранной валюты
    currency_rate = models.DecimalField(max_digits=19, decimal_places=4)
    # G241 / Код внешнеэкономической операции
    foreign_economic_code = models.CharField(max_length=2)
    # G242 / Код вида расчета по сделке
    payment_type_code = models.CharField(max_length=3)
    # G542 / Дата представления ЭГТД
    provision_date = models.DateTimeField()
    # GBN / Количество записей в файле GB.dbf
    paid_payment_details_count = models.SmallIntegerField()
    # DECL_ID / ID декларации из таможни
    declaration_id = models.IntegerField()
    # NOM_REG / Регистрационный номер
    declaration_number = models.CharField(max_length=18)
    # GA / Номер свидетельства, номер разрешения
    permit_number = models.CharField(max_length=23)
    # G16 / Страна происхождения товаров
    country_name = models.CharField(max_length=17)
    # GE_A12, GE_A11, G142 (пропущены)
    # G545 / Должность работника
    declarant_position = models.CharField(max_length=250)
    # G546 / ФИО работника
    declarant_FIO = models.CharField(max_length=250)
    # DOCUMENTID / Уникальный номер документа
    document_id = models.CharField(max_length=36)
    # G15 / Краткое наименование страны отправления
    sender_country_name = models.CharField(max_length=17)
    # G544 / Исходящий номер в делах заявителя
    outgoing_number = models.CharField(max_length=50)
    # G47_KD / Курс доллара
    dollar_rate = models.DecimalField(max_digits=19, decimal_places=4)
    # G47_KS / Курс евро
    euro_rate = models.DecimalField(max_digits=19, decimal_places=4)
    # DATEC / Дата декларации
    declaration_date = models.DateTimeField()
    # G013 / Код вида таможенного разрешения
    permit_code = models.CharField(max_length=3)
    # G031, FORWCODE, FORWNAME, CONTRACT, COST, ST_CODE, ST_NAME, ADD_INFO, VID_CORR, CODE_CORR (пропущены)

    def __str__(self):
        return self.declaration_number or "Unnamed Declaration"

