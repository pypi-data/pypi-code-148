import os
import sys

from boltons import fileutils
from jinja2 import BaseLoader, Environment, StrictUndefined
from prompt_toolkit import prompt as user_input
from prompt_toolkit.validation import ValidationError, Validator

from . import template
from .utils import var2bool


def clone_tree(args, questions):
    # copy tree from source to dest, rendering templates
    # along the way.
    env = Environment(loader=BaseLoader())
    env.undefined = StrictUndefined
    ctx = {}

    # Seed the context
    for question in questions:
        name = question["name"]
        # value can be missing because of "when" clause
        value = question.get("value")
        if name is not None and value is not None:
            ctx[name] = value

    # Get the template source directory (from command line)
    # It's the folder container another folder named "template"
    template_dir = args["template"]
    template_dir = os.path.join(template_dir, "template")
    template_dir = os.path.abspath(template_dir)

    # For every source file, replace templates, and create file
    for src in fileutils.iter_find_files(template_dir, "*", include_dirs=True):
        dst = os.path.relpath(src, template_dir)
        dst = env.from_string(dst).render(**ctx)
        dst = os.path.join(args.get("output", "."), dst)

        if os.path.islink(src):
            # TODO: Change destination
            pass
        elif os.path.isdir(src):
            fileutils.mkdir_p(dst)
        else:
            fileutils.mkdir_p(os.path.dirname(dst))
            with open(src, encoding="UTF-8") as fd:
                dst_contents = fd.read()
            dst_contents = env.from_string(dst_contents).render(**ctx)
            with open(dst, mode="w", encoding="UTF-8") as fd:
                fd.write(str(dst_contents))


def validate_answer(text, schema, defaultable=True):
    text = text.strip()

    # Default is valid when pressing enter, but not when pressing ctrl-D
    if defaultable is True:
        defaultable = schema.get("default", False)

    # nullable only makes sense with a default, and ctrl-d to
    # obtain the null value which is in fact an empty
    # string
    nullable = schema.get("nullable", False)
    if len(text) == 0:
        if defaultable or nullable:
            return True
        raise ValidationError(message="Answer is required")

    vartype = schema.get("type", "string")
    if vartype == "boolean":
        try:
            var2bool(text)
            return True
        except ValueError:
            raise ValidationError(message="Answer must be a boolean (true/false, yes/no)") from None

    if vartype == "string":
        min_length = schema.get("minLength", None)
        if min_length and len(text) < min_length:
            raise ValidationError(message=f"Answer cannot be shorter than {min_length} characters")

        max_length = schema.get("maxLength", None)
        if max_length and len(text) > max_length:
            raise ValidationError(message=f"Answer cannot be longer than {max_length} characters")

    return True


def prettify_answer(answer, vartype):
    if isinstance(answer, str):
        answer = answer.strip()

    if vartype == "string":
        return answer
    if vartype == "boolean":
        return var2bool(answer)
    return None


def prompt_question(question):
    # Get question details
    name = question["name"]
    prompt = question["prompt"] + ": "
    description = question.get("description")
    schema = question.get("schema", {})
    default = schema.get("default")
    vartype = schema.get("type", "string")

    validator = Validator.from_callable(lambda x: validate_answer(x, schema))

    while True:
        try:
            if sys.stdin.isatty():
                answer = user_input(
                    prompt,
                    validator=validator,
                    bottom_toolbar=description,
                    validate_while_typing=False,
                )
                answer = answer.strip() or default
            else:
                answer = input(prompt)
                validate_answer(answer.strip(), schema)
            return name, prettify_answer(answer, vartype)

        except EOFError:
            # ctrl-d was used, don't set default if string
            if vartype == "boolean":
                continue
            try:
                validate_answer("", schema, False)
            except ValidationError:
                continue
            return name, prettify_answer("", vartype)


def prepare_question(question, env, ctx):
    def templatize(what):
        if isinstance(what, str):
            return env.from_string(what).render(**ctx)
        return what

    # Get question details
    schema = question.get("schema", {})

    # Will we prompt this question?
    when = question.get("when")
    when = templatize(when)
    if when is not None:
        when = var2bool(when)
        question["when"] = when
        if not when:
            return False

    # Build prompt
    name = question["name"]
    default = schema.get("default")
    default = templatize(default)
    if default is not None:
        vartype = schema.get("type", "string")
        if vartype == "boolean":
            default = var2bool(default)
        prompt = f"{name} [{default}]"
        schema["default"] = default
    else:
        prompt = f"{name}"
    question["prompt"] = prompt
    return True


def prompt_questions(questions):
    env = Environment()
    env.undefined = StrictUndefined
    ctx = {}

    for question in questions:
        if not prepare_question(question, env, ctx):
            continue
        name, answer = prompt_question(question)
        if name is not None:
            question["value"] = answer
            ctx[name] = answer

    return questions


def clone(args):
    # Get local folder from which we can load files from
    data = template.get_data(args["template"])
    data = data.get("questions") or []
    prompt_questions(data)

    clone_tree(args, data)


#    print(json.dumps(data, indent=2))
