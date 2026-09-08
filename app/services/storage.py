import boto3
from datetime import timedelta
from math import floor
from app.config.settings import get_settings
from app.core.convert import Storage

settings = get_settings()
s3 = boto3.client('s3')

def presign_get(key: str, expires: timedelta = timedelta(hours=1)) -> str:
    return s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': settings.s3_bucket,
            'Key': key
        },
        ExpiresIn=expires.seconds
    )

def presign_put(key: str, expires: timedelta = timedelta(minutes=1)) -> str:
    return s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': settings.s3_bucket,
            'Key': key
        },
        ExpiresIn=expires.seconds
    )

def presign_post(
    key: str,
    max_size: Storage | None = None,
    content_type: str | None = None,
    expires: timedelta = timedelta(minutes=1)
):
    fields = {}
    conditions = []

    if content_type is not None:
        fields['Content-Type'] = content_type
        conditions.append(['eq', '$Content-Type', content_type])
    else:
        conditions.append(['starts-with', '$Content-Type', ''])

    if max_size is not None:
        conditions.append(['content-length-range', 1, floor(max_size.bytes)])

    return s3.generate_presigned_post(
        Bucket=settings.s3_bucket,
        Key=key,
        Fields=fields,
        Conditions=conditions,
        ExpiresIn=expires.seconds
    )