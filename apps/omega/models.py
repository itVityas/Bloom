from django.db import models


class Konstrobj(models.Model):
    unvcode = models.BigIntegerField(primary_key=True, db_comment='Уникальный код')
    itemcode = models.BigIntegerField(db_comment='Код элемента')
    # itemtype = models.ForeignKey(KoTypes, models.DO_NOTHING, db_column='itemtype', db_comment='Тип элемента')
    sign = models.CharField(max_length=200, db_comment='Обозначение')
    name = models.CharField(max_length=200, blank=True, null=True, db_comment='Наименование')
    notice = models.CharField(max_length=255, blank=True, null=True, db_comment='Примечание')
    attr = models.BigIntegerField(db_comment='Признак типа')
    supplytype = models.BigIntegerField(db_comment='Признак изготовления')
    owner = models.BigIntegerField(db_comment='Владелец')
    protection = models.BigIntegerField(db_comment='Признак закрытости')
    recdate = models.DateField(db_comment='Дата записи')
    # meascode = models.ForeignKey('Measures', models.DO_NOTHING, db_column='meascode', db_comment='Единица измерения')
    revision = models.BigIntegerField(db_comment='Ревизия')
    # prodcode = models.ForeignKey(BoProduction, models.DO_NOTHING, db_column='prodcode', db_comment='Код продукта')
    planningtype = models.BigIntegerField(db_comment='Тип планирования')
    # docletter = models.ForeignKey('Letters', models.DO_NOTHING, db_column='docletter', blank=True, null=True, db_comment='Литера документаци')
    format = models.CharField(max_length=15, blank=True, null=True, db_comment='Формат')
    # formedfrom = models.ForeignKey('self', models.DO_NOTHING, db_column='formedfrom', blank=True, null=True, db_comment='Сформирована из')
    formedtype = models.BigIntegerField(blank=True, null=True, db_comment='Сформирована как')
    # kind = models.ForeignKey(KoDocumentsKinds, models.DO_NOTHING, db_column='kind', blank=True, null=True, db_comment='Вид документа')
    # bocode = models.OneToOneField(BusinessObjects, models.DO_NOTHING, db_column='bocode')
    # prodsupplytype = models.ForeignKey('ProductionSupplyType', models.DO_NOTHING, db_column='prodsupplytype', db_comment='Производственный признак изготовления')

    class Meta:
        managed = False
        db_table = 'konstrobj'
        # unique_together = (('unvcode', 'itemtype'), ('unvcode', 'attr'), ('itemtype', 'itemcode'), ('sign', 'itemtype', 'revision', 'attr'),)
        db_table_comment = 'Конструкторские объекты'


class VzNorm(models.Model):
    code = models.BigIntegerField(primary_key=True)
    # mat_code = models.ForeignKey(Materials, models.DO_NOTHING, db_column='mat_code')
    plcode = models.CharField(max_length=30)
    ko_sign = models.CharField(max_length=100)
    old_ko_sign = models.CharField(max_length=100)
    unvcode = models.ForeignKey(Konstrobj, models.DO_NOTHING, db_column='unvcode')
    norm = models.DecimalField(max_digits=30, decimal_places=15, blank=True, null=True)
    # meascode = models.ForeignKey(Measures, models.DO_NOTHING, db_column='meascode', blank=True, null=True)
    mass = models.DecimalField(max_digits=13, decimal_places=7, blank=True, null=True)
    # tp_code = models.ForeignKey(Techprocesses, models.DO_NOTHING, db_column='tp_code', blank=True, null=True)
    # norm_code = models.ForeignKey(DetExpense, models.DO_NOTHING, db_column='norm_code', blank=True, null=True)
    # aux_code = models.ForeignKey(AuxMaterialRates, models.DO_NOTHING, db_column='aux_code', blank=True, null=True)
    color_code = models.BigIntegerField(blank=True, null=True)
    schema_code = models.BigIntegerField(blank=True, null=True)
    wssign = models.CharField(max_length=10, blank=True, null=True)
    dobjcode = models.BigIntegerField(blank=True, null=True)
    tp2ko2ri = models.BigIntegerField(blank=True, null=True)
    sect_sign = models.CharField(max_length=20, blank=True, null=True)
    sect_code = models.BigIntegerField(blank=True, null=True)
    zagweight = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    zagsize = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vz_norm'
        db_table_comment = 'Нормы витязя'


class VzNab(models.Model):
    code = models.BigIntegerField(primary_key=True, db_comment='код')
    pkey = models.BigIntegerField(db_comment='Код строки спецификации')
    spc_sign = models.CharField(max_length=100, db_comment='Обозначение спецификации')
    spc_unv = models.ForeignKey(Konstrobj, models.DO_NOTHING, db_column='spc_unv', db_comment='Код спецификации')
    item_sign = models.CharField(max_length=100, db_comment='Обозначение элемента спецификации')
    item_unv = models.ForeignKey(Konstrobj, models.DO_NOTHING, db_column='item_unv', related_name='vznab_item_unv_set',
                                 db_comment='Код элемента спецификации')
    # color_code = models.ForeignKey(ColorSchema, models.DO_NOTHING, db_column='color_code', blank=True, null=True,
    #                                db_comment='Код схемы цвета')
    all9999 = models.BigIntegerField(db_comment='Признак -9999')
    pos = models.CharField(max_length=10, blank=True, null=True, db_comment='Позиция')
    cntnum = models.BigIntegerField(db_comment='Количество числитель')
    cntdenom = models.BigIntegerField(db_comment='Количество знаменатель')
    kpr = models.CharField(max_length=5, blank=True, null=True, db_comment='Код принадлежности')
    # meas_code = models.ForeignKey(Measures, models.DO_NOTHING, db_column='meas_code', blank=True, null=True,
    #                               db_comment='Код единицы измерения')
    kdd = models.DateField(blank=True, null=True, db_comment='Дата исключения')
    dvi = models.DateField(blank=True, null=True, db_comment='DVI')
    iz = models.CharField(max_length=25, blank=True, null=True, db_comment='IZ')
    change_mark = models.BigIntegerField(blank=True, null=True, db_comment='Код блока замен')
    elem_unv = models.ForeignKey(Konstrobj, models.DO_NOTHING, db_column='elem_unv', related_name='vznab_elem_unv_set',
                                 blank=True, null=True, db_comment='Koд перечня элементов')
    spc_color_code = models.BigIntegerField(blank=True, null=True, db_comment='Цвет узла')
    item_sign_old = models.CharField(max_length=100, blank=True, null=True, db_comment='Старое обозначение элемента')
    ndd = models.DateField(blank=True, null=True, db_comment='Дата начала')

    class Meta:
        managed = False
        db_table = 'vz_nab'
        db_table_comment = 'Импорт спецификаций для витязя (от нас к ним)'
        