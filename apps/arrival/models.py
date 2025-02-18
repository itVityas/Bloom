from django.db import models


# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Container(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=30)
    suppose_date = models.DateField()
    exit_date = models.DateField()
    delivery = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=20, default="Created")
    invoice = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Content(models.Model):
    name = models.CharField(max_length=100)
    shot_name = models.CharField(max_length=30)
    count = models.PositiveIntegerField()
    container = models.ForeignKey(Container, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.shot_name


class Declaration(models.Model):
    # Порядок полей соответствует порядку столбцов в DBF

    # Внешний ключ (не из DBF)
    container = models.ForeignKey(
        Container, on_delete=models.SET_NULL, null=True, blank=True, related_name='container'
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
    provision_date = models.DateField()
    # GBN / Количество записей в файле GB.dbf
    paid_payment_details_count = models.SmallIntegerField()
    # DECL_ID / ID декларации из таможни
    declaration_id = models.IntegerField(unique=True)
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
    declaration_date = models.DateField()
    # G013 / Код вида таможенного разрешения
    permit_code = models.CharField(max_length=3)
    # G031, FORWCODE, FORWNAME, CONTRACT, COST, ST_CODE, ST_NAME,
    # ADD_INFO, VID_CORR, CODE_CORR (пропущены)

    def __str__(self):
        return self.declaration_number or "Unnamed Declaration"

    class Meta:
        ordering = ['-id']


class DeclaredItem(models.Model):
    declaration_id = models.ForeignKey(
        Declaration, on_delete=models.CASCADE, related_name='declared_items'
    )

    # G312 / Коммерческое или контрактное наименование товара
    name = models.CharField(max_length=250)
    # G314 / пропущен
    # G32 / Номер товара
    ordinal_number = models.IntegerField()
    # G34 / Код страны происхождения товара
    country_code = models.CharField(max_length=3)
    # G34A / Буквенный код страны происхождения товара
    alpha_country_code = models.CharField(max_length=3)
    # G38 / Брутто. Вес нетто в кг
    gross_weight = models.FloatField()
    # G41 / Количество товара в доп единицах измерения
    quantity = models.FloatField(null=True, blank=True)
    # G41A / Код доп единицы измерения
    unit_code = models.CharField(max_length=10, null=True, blank=True)
    # G41B / Наименование доп единицы измерения
    unit_name = models.CharField(max_length=20, null=True, blank=True)
    # G42 / Фактурная стоимость товара в валюте платежа, указанной в поле G221 в файле DECL.DBF(payment_currency_code)
    cost = models.DecimalField(max_digits=19, decimal_places=4)
    # G46 / Статистическая стоимость товара в долларах США
    statistical_cost = models.DecimalField(max_digits=19, decimal_places=4)
    # G47N / Связан с файлом G47.DBF, для чего не знаю
    payment_details_count = models.IntegerField()
    # G44N / Количество записей в файле G44.DBF
    document_details_count = models.IntegerField()
    # DECL_ID / номер декларации
    declaration = models.IntegerField()
    # G33 / Код товара по ТН ВЭД
    code = models.CharField(max_length=50)
    # G16 / Страна происхождения товаров, заявленных в ЭГТД
    country_name = models.CharField(max_length=17)
    # G37 / ??
    g37 = models.CharField(max_length=2)
    # G38A / Чистый вес нетто в кг
    net_weight = models.FloatField()
    # G372 / Код предшествующего таможенного режима, установленного ранее таможенным органом в отношении товара
    previous_customs_regime_code = models.CharField(max_length=2)
    # G373 / ???
    g373 = models.CharField(max_length=3)
    # G45 / Таможенная стоимость товара в белорусских рублях
    customs_cost = models.DecimalField(max_digits=19, decimal_places=4)
    # G31STZ / ???
    g31stz = models.CharField(max_length=50)
    # G311STZ / ???
    g311stz = models.CharField(max_length=3)
    # G312STZ / ???
    g312STZ = models.CharField(max_length=13)
    # G15, G15A, G15A_0, G15A_1 / пропущены
    # G17, G17A, G17A_0, G17A_1 / пропущены
    # CODE_CORR / пропущен
    # G43 / Метод определения таможенной стоимости
    valuation_method = models.CharField(max_length=2)
    # G21_A, G21_0, G21_1 / пропущены

    def __str__(self):
        return f'{self.declaration} - {self.ordinal_number}'
