# import json
from django.db.models.loading import get_model
from django.core.management.base import BaseCommand, CommandError
from django.db.models.fields import EmailField

# from http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
# def convert(name):
    # s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    # return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def convert(name):
    return name.replace('_', ' ').capitalize()

bs_form = """\
<form role="form" class="form-horizontal">
%s\
  <div class="form-group">
    <div class="col-sm-offset-2 col-sm-10">
      <button class="btn btn-primary"><i class="fa fa-save"></i> Save</button>
    </div>
  </div>
</form>
"""

bs_field = """\
  <div class="form-group">
    <label for="%(id)s" class="col-sm-2 control-label">%(label)s</label>
    <div class="col-sm-10">
%(field)s
    </div>
  </div>
"""

bs_input = """\
      <input type="%(input_type)s" class="form-control" id="%(id)s"/>"""

bs_select = """\
      <select class="form-control" id="%(id)s">%(options)s
      </select>"""

bs_option = """
        <option value="%(value)s">%(label)s</option>"""


def format_bs_field(model_name, field):

    field_id_html = model_name + '-' + field.name

    if field.choices:
        field_html = bs_select % {
            'id': field_id_html,
            'options': "".join([bs_option % {'value': value, 'label': label} for value, label in field.choices])
        }
    elif isinstance(field, EmailField):
        field_html = bs_input % {
            'id': field_id_html,
            'input_type': 'email'
        }
    else:
        field_html = bs_input % {
            'id': field_id_html,
            'input_type': 'text'
        }

    return bs_field % {
        'id': field_id_html,
        'label': convert(field.name),
        'field': field_html,
    }

class Command(BaseCommand):
    args = '<app_name> <model_name>'
    help = 'Prints a bootstrap form for the supplied app & model'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError('Please supply an app name & model name')

        app_name = args[0]
        model_name = args[1]

        model_class = get_model(app_name, model_name)
        fields = [format_bs_field(model_name, field) for field in model_class._meta.fields if field.name != 'id']
        self.stdout.write(bs_form % "".join(fields))
