import cerberus
import yaml
from jinja2 import Environment, StrictUndefined

from . import template

# https://docs.python-cerberus.org/en/stable/validation-rules.html
SCHEMA = r"""
---
questions:
  type: list
  default: []
  schema:
    type: dict
    default: {}
    nullable: true
    schema:
      name:
        type: string
        regex: '^\S+$'
        required: true
      value:
        type: [string, boolean]
      when:
        type: [string, boolean]
      schema:
        type: dict
        default: {}
        nullable: true
        schema:
          type:
            type: string
            allowed: ["string", "boolean"]
          default:
            type: [string, boolean]
          nullable:
            type: boolean
            default: true
          minLength:
            type: integer
            min: 0
          maxLength:
            type: integer
            min: 0
"""


def validate_schema(args):
    data = template.get_data(args.get("template", ""))
    schema = yaml.safe_load(SCHEMA)
    validator = cerberus.Validator(schema)
    if not validator.validate(data):
        raise Exception("YAML schema validation error: " + str(validator.errors))
    return data


def validate_templates(data):
    env = Environment()
    env.undefined = StrictUndefined
    ctx = {}

    def templatize(what):
        if isinstance(what, str):
            return env.from_string(what).render(**ctx)
        return what

    for question in data.get("questions", {}):
        name = question["name"]

        when = question.get("when", True)
        when = templatize(when)

        schema = question.get("schema", {})
        default = schema.get("default")
        default = templatize(default)

        # Give a value to the context value
        value = question.get("value")
        value = templatize(value)
        ctx[name] = value or default or name


def validate(args):
    data = validate_schema(args)
    validate_templates(data)
