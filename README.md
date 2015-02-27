This command will print bootstrap form snippets given a supplied app name & model name.  I use this to paste into Angular or React views so I can get something up quickly to show a client.

Installation
------------

`pip install git+git://github.com/rapilabs/django-bootstrap-generator.git`

or in your requirements.txt:

`-e git+git://github.com/rapilabs/django-bootstrap-generator.git#egg=django-bootstrap-generator`

and in your settings.py add:

```python
INSTALLED_APPS = (
    # ...
    'django_bootstrap_generator',
)
