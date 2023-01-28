import jinja2
from laboro.error import LaboroError
from laboro.module import Module


class Template(Module):
  """This module is derivated from the ``laboro.module.Module`` base class.

  Its purpose is to provide a easy way to create and use template files within Laboro worklows.

  Arguments:

    args: An optional dictionary representing all module args, their types and their values.
  """

  def __init__(self, context, args=None):
    jinja_loader = jinja2.FileSystemLoader(context.workspace.workspace_dir)
    self.env = jinja2.Environment(loader=jinja_loader, autoescape=True)
    super().__init__(filepath=__file__, context=context, args=args)

  @Module.laboro_method
  def render(self, template, params=None):
    try:
      return self.env.get_template(template).render(params=params)
    except jinja2.exceptions.TemplateNotFound as err:
      msg = f"[TemplateNotFoundError] No such file: {template}"
      raise LaboroError(msg) from err
    except jinja2.exceptions.UndefinedError as err:
      msg = f"[TemplateUndefinedError] {err.__class__.__name__}: {err}"
      raise LaboroError(msg) from err
    except jinja2.exceptions.TemplateSyntaxError as err:
      msg = f"[TemplateSyntaxError]: {err}"
      raise LaboroError(msg) from err
