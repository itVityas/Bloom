from django.db import models


# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Declaration(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True)
    declaration_id = models.IntegerField() # DECL_ID  / ID декларации из таможни
    declaration_number = models.CharField(max_length=18) # NOM_REG / Регистрационный номер
    permit_number = models.CharField(max_length=23) # GA / Номер свидетельства, номер разрешения
    declaration_date = models.DateTimeField() # DATEC /
    provision_date = models.DateTimeField() # G542 / Дата представления ЭГТД
    document_id = models.CharField(max_length=36) # DOCUMNETID / Уникальный номер документа
    type_code = models.CharField(max_length=3) # G011 / Код типа таможенной декларации
    type = models.CharField(max_length=3) # G012_1 / Вид таможенной декларации
    permit_code = models.CharField(max_length=3) # G013 / Код вида таможенного разрешения
    country_name = models.CharField(max_length=17) # G16 / Страна происхождения товаров заявленных в ЭГТД
    sender = models.CharField(max_length=38) # G022 / Компания отправитель
    sender_address = models.CharField(max_length=250) # G023 / Адрес компании отправителя
    sender_country_code = models.CharField(max_length=3) # G15A / Код старны отправления
    sender_country_name = models.CharField(max_length=17) # G15 / Краткое наименования страны отправления товаров, заявленных в ЭГТД
    sender_alpha_country_code = models.CharField(max_length=2) # G15A_0 / Буквенный код страны
    g15A_1 = models.CharField(max_length=4) # G15A_1 / ???(000 в примере)
    delivery_terms = models.CharField(max_length=3) # G20 / Краткое наименование условия поставки(?)
    item_count = models.IntegerField() # G05 / Общее количество наименований товаров, заявленных в ЭГТД
    payment_currency_code = models.CharField(max_length=3) # G221 / Код валюты платежа в соответствии с условиями внешнеторговой сделки, объектами которой являются заявленные в ЭГТД товары
    total_cost = models.DecimalField(max_digits=19, decimal_places=4) # G222 / Общая фактурная стоимость всех заявленных в ЭГТД товаров в валюте платежа
    currency_rate = models.DecimalField(max_digits=19, decimal_places=4) # G23 / Курс иностранной валюты для фактурной стоимости, который устанавливается НБ РБ для внешнеторговых операций
    dollar_rate = models.DecimalField(max_digits=19, decimal_places=4) # G47_KD / Курс доллара
    euro_rate = models.DecimalField(max_digits=19, decimal_places=4) # G47_KS / Курс евро
    foreign_economic_code = models.CharField(max_length=2) # G241 / Код внешнеэкономической операции
    payment_type_code = models.CharField(max_length=3) # G 242 / Код вида расчета по сделке
    paid_payment_details_count = models.SmallIntegerField() # GNB / Количество записей в файле GB.dbf
    receiver = models.CharField(max_length=38) # G082 / Получатель
    receiver_address = models.CharField(max_length=250) # G083 / Адрес получателя
    declarant_position = models.CharField(max_length=250) # G545 / Должность работника
    declarant_FIO = models.CharField(max_length=250) # G546 / ФИО работника
    outgoing_number = models.CharField(max_length=50) # G544 / Исходящий номер в делах заявителя

    def __str__(self):
        return self.declaration_number or "Unnamed Declaration"
