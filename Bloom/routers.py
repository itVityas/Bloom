# class OracleReadOnlyRouter:
#     """
#     Router for app 'omega'. Oracle read-only access.
#     """
#     def db_for_read(self, model, **hints):
#         # Если модель принадлежит приложению omega, использовать базу oracle_db
#         if model._meta.app_label == 'omega':
#             return 'oracle_db'
#         return None
#
#     def db_for_write(self, model, **hints):
#         # Запрещаем запись в базу oracle_db для моделей из omega
#         if model._meta.app_label == 'omega':
#             return None
#         return None
#
#     def allow_relation(self, obj1, obj2, **hints):
#         # Разрешаем отношения, если обе модели либо из omega, либо обе не из omega
#         if (obj1._meta.app_label == 'omega' and obj2._meta.app_label == 'omega'):
#             return True
#         elif (obj1._meta.app_label != 'omega' and obj2._meta.app_label != 'omega'):
#             return True
#         return False
#
#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         # Не выполнять миграции для приложения omega на базе oracle_db
#         if app_label == 'omega':
#             # Если база данных не oracle_db, то миграции не нужны
#             return db != 'oracle_db'
#         # Для остальных приложений — мигрировать как обычно
#         return None
