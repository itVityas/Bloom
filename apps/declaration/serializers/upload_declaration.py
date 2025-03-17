from rest_framework import serializers

class ZipFileUploadSerializer(serializers.Serializer):
    """
    Serializer for uploading a zip file containing DBF files.

    The uploaded zip file must contain the following files (with exact names):
    DECL.DBF, G18.DBF, G40.DBF, G44.DBF, G47.DBF, G48.DBF, G313, GB.DBF, TOVAR.DBF.

    Optionally, a container_id can be provided to associate declarations (from DECL.DBF)
    with a specific container.
    """
    file = serializers.FileField()
    container_id = serializers.IntegerField(required=False, allow_null=True)
