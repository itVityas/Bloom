from rest_framework import serializers


class ZipFileUploadSerializer(serializers.Serializer):
    """
    Serializer for uploading a zip file containing DBF files.

    The uploaded zip file must contain the following files (with exact names):
    DECL.DBF, G18.DBF, G40.DBF, G44.DBF, G47.DBF, G48.DBF, G313, GB.DBF, TOVAR.DBF.
    """
    file = serializers.FileField()
