import os
import tempfile
import shutil
import zipfile
import logging

from apps.sez.clearance_workflow.create_dbf.norm import generate_norm_dbf
from apps.sez.clearance_workflow.create_dbf.prihod import generate_prihod_decl_dbf
from apps.sez.clearance_workflow.create_dbf.rashod import generate_rashod_decl_dbf
from apps.sez.clearance_workflow.create_dbf.rashod_tovar import generate_rashod_tovar_decl_dbf
from apps.sez.clearance_workflow.create_dbf.prihod_tovar import generate_prihod_tovar_decl_dbf

logger = logging.getLogger(__name__)


def generate_all_dbf_zip(
    clearance_invoice_id: int,
    zip_output_path: str,
) -> None:
    """
    Generate NORM, PRIHOD_DECL and RASHOD_DECL DBF files for a given ClearanceInvoice,
    package them into a ZIP archive with the following structure:

      <zip>/
        norm/
          norm.dbf
        prihod/
          decl.dbf
          tovar.dbf
        rashod/
          decl.dbf
          tovar.dbf

    Args:
        clearance_invoice_id (int): PK of the ClearanceInvoice.
        zip_output_path (str): Full file path for the resulting .zip.
        encoding (str, optional): Code page for all DBF files. Defaults to 'cp866'.

    Raises:
        ValueError: if any of the underlying generators raises ValueError.
        OSError: on file I/O errors.
        Exception: propagates any unexpected errors from DBF generation or zipping.
    """
    logger.info(f"Starting full DBF ZIP generation for invoice id={clearance_invoice_id}")

    # Create a temporary working directory
    temp_dir = tempfile.mkdtemp(prefix=f"dbf_zip_{clearance_invoice_id}_")
    try:
        # Prepare subdirectories
        norm_dir = os.path.join(temp_dir, 'norm')
        prihod_dir = os.path.join(temp_dir, 'prihod')
        rashod_dir = os.path.join(temp_dir, 'rashod')
        os.makedirs(norm_dir)
        os.makedirs(prihod_dir)
        os.makedirs(rashod_dir)

        # Generate each DBF into its folder
        norm_path = os.path.join(norm_dir, 'norm.dbf')
        generate_norm_dbf(clearance_invoice_id, norm_path)

        prihod_path = os.path.join(prihod_dir, 'decl.dbf')
        generate_prihod_decl_dbf(clearance_invoice_id, prihod_path)

        prihod_tovar_path = os.path.join(prihod_dir, 'tovar.dbf')
        generate_prihod_tovar_decl_dbf(clearance_invoice_id, prihod_tovar_path)

        rashod_path = os.path.join(rashod_dir, 'decl.dbf')
        generate_rashod_decl_dbf(clearance_invoice_id, rashod_path)

        rashod_tovar_path = os.path.join(rashod_dir, 'tovar.dbf')
        generate_rashod_tovar_decl_dbf(clearance_invoice_id, rashod_tovar_path)

        # Create the ZIP archive
        # Ensure parent dir exists
        os.makedirs(os.path.dirname(zip_output_path), exist_ok=True)
        with zipfile.ZipFile(zip_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through temp_dir and add files preserving the folder names
            for folder_name in ('norm', 'prihod', 'rashod'):
                folder_path = os.path.join(temp_dir, folder_name)
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    arcname = os.path.join(folder_name, filename)
                    zipf.write(file_path, arcname)
        logger.info(f"ZIP archive written to {zip_output_path}")

    except Exception as e:
        logger.exception(f"Failed to generate DBF ZIP for invoice id={clearance_invoice_id}: {e}")
        # Optionally, wrap or re-raise
        raise
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir)
            logger.debug(f"Cleaned up temp dir {temp_dir}")
        except Exception as cleanup_err:
            logger.warning(f"Failed to remove temp dir {temp_dir}: {cleanup_err}")
