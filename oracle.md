# 📘 Инструкция по подключению базы данных Oracle (Omega) к Django-проекту

## 🧱 Используемые технологии

- Oracle Database 12.2.0.1.0
- Oracle Instant Client 19.26
- Django 5.x
- Python 3.12
- `cx_Oracle` для Python
- Кастомный backend на основе `django.db.backends.oracle`

---

## 📁 1. Установка Oracle Instant Client

1. Скачать архив Oracle Instant Client 19.26 (нужен пакет `basic`).
2. Распаковать архив в удобное место, например:  
   ```bash
   sudo mkdir -p /opt/oracle
   unzip instantclient-basic-linux.x64-19.26.0.0.0dbru.zip -d /opt/oracle
   ```
3. Добавить путь к библиотекам в переменную окружения:
   ```bash
   export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_26
   ```
4. Для постоянного использования — добавить в `~/.bashrc` или `~/.zshrc`:
   ```bash
   echo 'export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_26' >> ~/.bashrc
   source ~/.bashrc
   ```

---

## ⚙️ 2. Установка зависимостей Python

Установить библиотеку для работы с Oracle:
```bash
pip install cx_Oracle
```
> Убедитесь, что используется 64-битная версия Python и Instant Client.

Создать ссылку на библиотеку:
```bash
sudo ln -s /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /usr/lib/x86_64-linux-gnu/libaio.so.1
```

---

## 🔧 3. Настройка кастомного Oracle backend

Django 5.x требует Oracle 19+. Для обхода проверки создается собственный backend.

Создайте файл `apps/omega/oracle_12/base.py` со следующим содержимым:

```python
from django.db.backends.oracle.base import DatabaseWrapper as OracleDatabaseWrapper

class DatabaseWrapper(OracleDatabaseWrapper):
    def get_database_version(self):
        if not hasattr(self, "_custom_database_version"):
            cursor = self.cursor()
            cursor.execute("SELECT * FROM v$version")
            version_line = cursor.fetchone()[0]
            version_string = version_line.split(" ")[-1]
            self._custom_database_version = tuple(map(int, version_string.split(".")[:3]))
        return self._custom_database_version
```

---

## ⚙️ 4. Настройки подключения в `settings.py`

```python
DATABASES = {
    'default': {
        # основная БД
    },
    'oracle_db': {
        'ENGINE': 'apps.omega.oracle_12',
        'NAME': '192.168.2.200:1521/omega',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
    },
}
```

---

## 🛠️ 5. Пример модели с использованием Oracle

```python
class VzNorm(models.Model):
    code = models.BigIntegerField(primary_key=True)
    plcode = models.CharField(max_length=30)
    ko_sign = models.CharField(max_length=100)
    old_ko_sign = models.CharField(max_length=100)
    norm = models.DecimalField(max_digits=30, decimal_places=15, blank=True, null=True)
    mass = models.DecimalField(max_digits=13, decimal_places=7, blank=True, null=True)
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
```

---

## 🧪 6. Проверка подключения

Выполните в Django Shell:
```bash
python manage.py shell
```
```python
from apps.omega.models import VzNorm
VzNorm.objects.using('oracle_db').all()[:5]
```
Если всё настроено верно — получите объекты из таблицы.

---

## 🛠️ 7. Часто встречающиеся ошибки

| Ошибка | Причина / Решение |
|--------|--------------------|
| `DPI-1047: Cannot locate a 64-bit Oracle Client library` | Не найден `libclntsh.so`. Проверьте `LD_LIBRARY_PATH`. Убедитесь, что клиент 64-битный. |
| `ORA-12514: TNS:listener does not currently know of service requested` | Неправильный `service_name` или `SID`. Проверьте у администратора БД. |
| `ORA-00942: table or view does not exist` | Неправильное имя таблицы или у пользователя нет прав доступа. |
| `django.db.utils.DatabaseError: DPI-1047` | Не найден Instant Client. Убедитесь, что он установлен и путь прописан. |

---

## ✅ 8. Команды для диагностики

Проверка переменной окружения:
```bash
echo $LD_LIBRARY_PATH
# /opt/oracle/instantclient_19_26
```

Проверка cx_Oracle:
```bash
python3 -c "import cx_Oracle; print(cx_Oracle.clientversion())"
```

Проверка соединения:
```bash
python manage.py dbshell --database=oracle_db
```

