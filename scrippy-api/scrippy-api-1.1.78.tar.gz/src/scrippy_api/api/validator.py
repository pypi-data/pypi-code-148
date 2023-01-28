import logging
import jsonschema


def validate(instance, schema):
  logging.info("[+] Validation des parametres")
  try:
    jsonschema.validate(instance=instance, schema=schema)
  except Exception:
    logging.info(" '-> Parametres invalides")
    return False
  logging.info(" '-> Parametres valides")
  return True
