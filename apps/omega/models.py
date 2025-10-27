from django.db import models


class Materials(models.Model):
    code = models.FloatField(primary_key=True, db_comment='Код')
    plcode = models.CharField(unique=True, max_length=30, blank=True, null=True, db_comment='Заводской код')
    okpcode = models.CharField(max_length=20, blank=True, null=True, db_comment='Код ОКП')
    tnvedcode = models.CharField(max_length=10, blank=True, null=True, db_comment='Код ТНВЭД')
    name = models.CharField(max_length=255, blank=True, null=True, db_comment='Наименование')
    matname = models.CharField(max_length=100, blank=True, null=True, db_comment='Марка')
    namestd = models.CharField(max_length=150, blank=True, null=True, db_comment='Стандарт на марку')
    profile = models.CharField(max_length=80, blank=True, null=True, db_comment='Профиль')
    profstd = models.CharField(max_length=50, blank=True, null=True, db_comment='Стандарт на профиль')
    tu = models.CharField(max_length=50, blank=True, null=True, db_comment='Технические условия')
    recdate = models.DateField(blank=True, null=True, db_comment='Дата записи')
    notice = models.CharField(max_length=255, blank=True, null=True, db_comment='Примечание')
    # meascode = models.ForeignKey('Measures', models.DO_NOTHING, db_column='meascode', blank=True, null=True, db_comment='Код первой единицы измерения')
    ivccode = models.CharField(max_length=10, blank=True, null=True, db_comment='Код ИВЦ')
    ivcgroupcode = models.BigIntegerField(blank=True, null=True, db_comment='Код калькуляционной группы ИВЦ')
    ivcname = models.CharField(max_length=75, blank=True, null=True, db_comment='Наименование ИВЦ')
    # meascode2 = models.ForeignKey('Measures', models.DO_NOTHING, db_column='meascode2', related_name='materials_meascode2_set', blank=True, null=True, db_comment='Код второй единицы измерения')
    # owner = models.ForeignKey('OwnerName', models.DO_NOTHING, db_column='owner', db_comment='Владелец материала')
    profname = models.CharField(max_length=80, blank=True, null=True, db_comment='Наименование профиля')
    gabarit = models.CharField(max_length=50, blank=True, null=True, db_comment='Габариты')
    updatedate = models.DateField(blank=True, null=True, db_comment='Дата изменения')
    # updateuser = models.ForeignKey('UserList', models.DO_NOTHING, db_column='updateuser', blank=True, null=True, db_comment='Пользователь')
    # meascode3 = models.ForeignKey('Measures', models.DO_NOTHING, db_column='meascode3', related_name='materials_meascode3_set', blank=True, null=True, db_comment='Код балансовой единицы измерения')
    # matmark_code = models.ForeignKey(MaterialMarks, models.DO_NOTHING, db_column='matmark_code', blank=True, null=True, db_comment='Код марки')
    # matname_code = models.ForeignKey(MaterialNames, models.DO_NOTHING, db_column='matname_code', blank=True, null=True, db_comment='Код наименования')
    # namestd_code = models.ForeignKey(MaretialGosts, models.DO_NOTHING, db_column='namestd_code', blank=True, null=True, db_comment='Код стандарта на марку')
    # profstd_code = models.ForeignKey(MaretialGosts, models.DO_NOTHING, db_column='profstd_code', related_name='materials_profstd_code_set', blank=True, null=True, db_comment='Код стандарта на профиль')
    # tu_code = models.ForeignKey(MaretialGosts, models.DO_NOTHING, db_column='tu_code', related_name='materials_tu_code_set', blank=True, null=True, db_comment='Код технических условий')
    # profile_code = models.ForeignKey(MaterialShapes, models.DO_NOTHING, db_column='profile_code', blank=True, null=True, db_comment='Код профиля')
    # profname_code = models.ForeignKey(MaterialShapeNames, models.DO_NOTHING, db_column='profname_code', blank=True, null=True, db_comment='Код наименования профиля')
    density = models.DecimalField(max_digits=14, decimal_places=6, blank=True, null=True, db_comment='Плотность')
    # socode = models.OneToOneField('OmpObjects', models.DO_NOTHING, db_column='socode', db_comment='Код объекта системы')
    state = models.BigIntegerField(db_comment='Статус материала')
    is_product = models.BigIntegerField(db_comment='Признак продукта')
    mattype = models.BigIntegerField(db_comment='Тип материала')
    # dobjcode = models.ForeignKey(Divisionobj, models.DO_NOTHING, db_column='dobjcode', blank=True, null=True, db_comment='Подразделение')

    class Meta:
        managed = False
        db_table = 'materials'
        db_table_comment = 'Справочник материалов'


class Stockobj(models.Model):
    code = models.BigIntegerField(primary_key=True, db_comment='Код ТМЦ')
    basecode = models.BigIntegerField(db_comment='Код базовой таблицы')
    basetype = models.BigIntegerField(db_comment='Тип базовой таблицы')
    drmet = models.BigIntegerField(blank=True, null=True, db_comment='Признак драгметалла')
    # subcontocode = models.ForeignKey('Subconto', models.DO_NOTHING, db_column='subcontocode', blank=True, null=True, db_comment='Код субконто')
    description = models.CharField(max_length=1024, blank=True, null=True, db_comment='Описание ТМЦ')
    desc_date = models.DateField(blank=True, null=True, db_comment='Дата форм. описания')
    desc_fmt = models.CharField(max_length=30, blank=True, null=True, db_comment='Формат описания')
    # dobj_code = models.ForeignKey(Divisionobj, models.DO_NOTHING, db_column='dobj_code', blank=True, null=True, db_comment='Код подразделения')
    # group_code = models.ForeignKey(GroupsInClassify, models.DO_NOTHING, db_column='group_code', blank=True, null=True, db_comment='Код класификатора')
    # subconto_usercode = models.ForeignKey('UserList', models.DO_NOTHING, db_column='subconto_usercode', blank=True, null=True, db_comment='Пользователь манявший субконто')
    subconto_userdate = models.DateField(blank=True, null=True, db_comment='Дата изменения субконто')
    # fk_bo_production = models.ForeignKey(BoProduction, models.DO_NOTHING, db_column='fk_bo_production', blank=True, null=True, db_comment='FK_BO_PRODUCTION')
    subtype = models.BigIntegerField(blank=True, null=True, db_comment='Подтип')
    # meascode = models.ForeignKey(Measures, models.DO_NOTHING, db_column='meascode', blank=True, null=True, db_comment='Ед. изм.')
    # owner = models.ForeignKey(OwnerName, models.DO_NOTHING, db_column='owner', blank=True, null=True, db_comment='Владелец')
    notice = models.CharField(max_length=100, blank=True, null=True, db_comment='Примечание')
    recdate = models.DateField(blank=True, null=True, db_comment='Дата записи')
    # fk_materials = models.ForeignKey(Materials, models.DO_NOTHING, db_column='fk_materials', blank=True, null=True, db_comment='FK_MATERIALS')
    # fk_stockother = models.ForeignKey(StockOther, models.DO_NOTHING, db_column='fk_stockother', blank=True, null=True, db_comment='FK_STOCKOTHER')
    # fk_tare = models.ForeignKey('Tare', models.DO_NOTHING, db_column='fk_tare', blank=True, null=True, db_comment='FK_TARE')
    # fk_kompspc = models.ForeignKey(Complspc, models.DO_NOTHING, db_column='fk_kompspc', blank=True, null=True, db_comment='FK_KOMPSPC')
    desc_update_check = models.BigIntegerField()
    sign = models.CharField(max_length=200, blank=True, null=True, db_comment='Обозначение')
    name = models.CharField(max_length=255, blank=True, null=True, db_comment='Наименование')
    unvcode = models.BigIntegerField(blank=True, null=True)
    attr = models.BigIntegerField(blank=True, null=True, db_comment='Признак типа КЭ')
    is_annul = models.BigIntegerField(blank=True, null=True, db_comment='Аннулировано')
    # min_leave_meas = models.ForeignKey(Measures, models.DO_NOTHING, db_column='min_leave_meas', related_name='stockobj_min_leave_meas_set', blank=True, null=True, db_comment='Минимальный отпуск(ед.изм.)')
    min_leave_value = models.FloatField(blank=True, null=True, db_comment='Минимальный отпуск')
    is_num = models.BigIntegerField(blank=True, null=True, db_comment='Номерной объект')
    mat_state = models.BigIntegerField(blank=True, null=True)
    # add_meas = models.ForeignKey(Measures, models.DO_NOTHING, db_column='add_meas', related_name='stockobj_add_meas_set', blank=True, null=True)
    nomsign = models.CharField(max_length=200, blank=True, null=True)
    # ch_code = models.ForeignKey(CustomsHouse, models.DO_NOTHING, db_column='ch_code', blank=True, null=True)
    params = models.BigIntegerField(blank=True, null=True)
    # socode = models.ForeignKey(OmpObjects, models.DO_NOTHING, db_column='socode', blank=True, null=True, db_comment='Код СО')
    min_leave_value_deviation = models.FloatField(blank=True, null=True, db_comment='Процент отклонения минимального отпуска')
    tnved_code = models.CharField(max_length=255, blank=True, null=True, db_comment='Код ТНВЭД')
    storage_period = models.BigIntegerField(blank=True, null=True, db_comment='Срок хранения (в днях)')
    expl_term = models.BigIntegerField(blank=True, null=True, db_comment='Срок эксплуатации')
    expl_term_change_date = models.DateField(blank=True, null=True, db_comment='Дата последнего изменения срока эксплуатации')
    # purchase_status = models.ForeignKey(PurchaseStatus, models.DO_NOTHING, db_column='purchase_status', blank=True, null=True, db_comment='Статус закупки')
    # serialobjs_docscheme = models.ForeignKey(SerialobjDocSchemes, models.DO_NOTHING, db_column='serialobjs_docscheme', blank=True, null=True, db_comment='Шаблон документов (для Серийных объектов)')
    gtin = models.CharField(unique=True, max_length=14, blank=True, null=True, db_comment='GTIN')

    class Meta:
        managed = False
        db_table = 'stockobj'
        unique_together = (('basetype', 'basecode'),)
        db_table_comment = 'Товарно-материальные ценности складского учета'


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
    mat_code = models.ForeignKey(Materials, models.DO_NOTHING, db_column='mat_code')
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


class AdmissibleSubst(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE')
    substfor = models.ForeignKey(Stockobj, models.CASCADE, related_name='substfor', db_column='SUBSTFOR')
    subst = models.ForeignKey(Stockobj, models.CASCADE, related_name='subst', db_column='SUBST')
    both_flag = models.IntegerField(db_column='BOTH_FLAG')
    koef = models.IntegerField(db_column='KOEF')
    # apply = models.IntegerField(db_column='APPLY', blank=True, null=True)
    # usercode = models.IntegerField(db_column='USERCODE')
    # userinsertdate = models.DateField(db_column='USEREINSERTDATE')
    # usereditdate = models.DateField(db_column='UESEREDITDATE', null=True, blank=True)
    datefrom = models.DateField(db_column='DATEFROM')
    dateto = models.DateField(db_column='DATETO', blank=True, null=True)
    # doccode = models.IntegerField(db_column='DOCCODE', blank=True, null=True)
    # doctype = models.IntegerField(db_column='DOCTYPE', blank=True, null=True)
    # notice = models.CharField(max_length=60, db_column='NOTICE', blank=True, null=True)
    # substdoc = models.CharField(max_length=255, db_column='SUBSTDOC', blank=True, null=True)
    # substdocdate = models.DateField(db_column='SUBSTDOCDATE', blank=True, null=True)
    # cl_group = models.IntegerField(db_column='CL_GROUP', blank=True, null=True)
    # inclusion = models.IntegerField(db_column='INCLUSION', blank=True, null=True)
    # substfor_meas = models.IntegerField(db_column='SUBSTFOR_MEAS', blank=True, null=True)
    # subst_meas = models.IntegerField(db_column='SUBST_MEAS', blank=True, null=True)
    # division = models.IntegerField(db_column='DIVISION', blank=True, null=True)
    # use_in_lc = models.IntegerField(db_column='USE_IN_LC', default=1)
    # use_in_bo_prod = models.IntegerField(db_column='USE_IN_BO_PROD', blank=True, null=True)
    # subst_norm = models.IntegerField(db_column='SUBST_NORM', default=1)

    class Meta:
        managed = False
        db_table = 'ADMISSIBLE_SUBST'
        db_table_comment = 'Аналоги'

    def __str__(self):
        return f'{self.code}: {self.substfor} -> {self.subst}'
