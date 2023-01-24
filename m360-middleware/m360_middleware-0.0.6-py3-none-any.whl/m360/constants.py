"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import os

GATEWAY_MAINTENANCE_IP = os.environ["GATEWAY_MAINTENANCE_IP"] if os.environ.get("GATEWAY_MAINTENANCE_IP") \
    else "127.0.0.1"
GATEWAY_MAINTENANCE_PORT = int(os.environ["GATEWAY_MAINTENANCE_PORT"]) if os.environ.get("GATEWAY_MAINTENANCE_PORT") \
    else 5000

SVC_ACCOUNT_TOKEN_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/token"

RESERVED_ROUTES = ["/heartbeat", "/registry/reload", "/awareness/reload"]

APP_AUTOREGISTER = True if os.environ.get("APP_AUTOREGISTER") is None or \
                           os.environ.get("APP_AUTOREGISTER").lower() in ["true", "yes", "1"] else False

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
MW_TESTING = True if os.environ.get("MW_TESTING") else False

DEFAULT_AWARENESS_TTL_MS = 3600000  # 1 hour
DEFAULT_RETRY_DELAY_SEC = 2  # 2 seconds


