import os

ENV_LOCAL = os.getenv("ENV_LOCAL", "local")
SERVICE_NAME = os.getenv("SERVICE_NAME", "RCTI_PLUS")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "AKIATO2X45HJ55CUJWON")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "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")
REGION_NAME = os.getenv("REGION_NAME", "ap-southeast-1")
BUCKET_NAME = os.getenv("BUCKET_NAME", "dev-rctiplus")
