from masonite.environment import env
from masonite.utils.location import base_path


DISKS = {
    "default": "local",
    "local": {
        "driver": "file",
        "path": base_path("tests/integrations/storage/framework/filesystem"),
    },
    "s3": {
        "driver": "s3",
        "client": env("S3_CLIENT"),
        "secret": env("S3_SECRET"),
        "bucket": env("S3_BUCKET"),
    },
}

STATICFILES = {
    # folder          # template alias
    "tests/integrations/storage/static": "static/",
    "tests/integrations/storage/compiled": "assets/",
    "tests/integrations/storage/public": "/",
}
