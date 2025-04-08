from django.db.backends.oracle.base import DatabaseWrapper as OracleDatabaseWrapper


class DatabaseWrapper(OracleDatabaseWrapper):
    def check_database_version_supported(self):
        version_str = self.connection.version
        version = version_str.split('.')
        major = int(version[0])
        minor = int(version[1]) if len(version) > 1 else 0
        print("⚙️ Custom Oracle 12 backend loaded with version:", version_str)

        if major < 12:
            raise Exception(f"Unsupported Oracle version: {version_str}")
