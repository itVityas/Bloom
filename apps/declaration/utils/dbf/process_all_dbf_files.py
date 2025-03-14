import os
import zipfile
from tempfile import NamedTemporaryFile

from .decl import process_decl_dbf_file
from .tovar import process_tovar_dbf_file
# from .g18 import process_g18_dbf_file
# from .g40 import process_g40_dbf_file
from .g44 import process_g44_dbf_file
# from .g47 import process_g47_dbf_file
# from .g48 import process_g48_dbf_file
from .g313 import process_g313_dbf_file
# from .gb import process_gb_dbf_file


PROCESSING_FUNCTIONS = {
    'DECL.DBF': process_decl_dbf_file,
    'TOVAR.DBF': process_tovar_dbf_file,
    # 'G18.DBF': process_g18_dbf_file,
    # 'G40.DBF': process_g40_dbf_file,
    # 'G44.DBF': process_g44_dbf_file,
    # 'G47.DBF': process_g47_dbf_file,
    # 'G48.DBF': process_g48_dbf_file,
    # 'G313': process_g313_dbf_file,
    # 'GB.DBF': process_gb_dbf_file,
}


def process_all_dbf_files(zip_file_path, container=None):
    """
    Process all DBF files contained in the provided zip archive.

    The zip archive must contain the following files (with exact names):
    DECL.DBF, G18.DBF, G40.DBF, G44.DBF, G47.DBF, G48.DBF, G313, GB.DBF, TOVAR.DBF.

    For each file present in the archive, the corresponding processing function is called
    with the path to the extracted temporary file. For the file 'DECL.DBF', the provided container
    instance is also passed to associate the declarations with that container.
    All temporary files (including the original zip file) are removed after processing.

    Args:
        zip_file_path (str): The file system path to the uploaded zip archive.
        container (Optional[Container]): An optional container instance to associate with declarations.

    Raises:
        Exception: If one or more required files are missing or if any exception occurs during extraction or processing.
    """
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        archive_files = zip_ref.namelist()

        missing_files = [file_name for file_name in PROCESSING_FUNCTIONS if file_name not in archive_files]
        if missing_files:
            raise Exception(f"Missing required files: {', '.join(missing_files)}")

        for file_name, process_func in PROCESSING_FUNCTIONS.items():
            with NamedTemporaryFile(delete=False, suffix=".dbf") as tmp_file:
                tmp_file.write(zip_ref.read(file_name))
                tmp_file_path = tmp_file.name
            try:
                if file_name == 'DECL.DBF':
                    process_func(tmp_file_path, container=container)
                else:
                    process_func(tmp_file_path)
            finally:
                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)