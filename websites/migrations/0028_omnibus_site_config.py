# Generated by Django 3.1 on 2021-02-03 21:39
import yaml
from django.db import migrations


OMNIBUS_STARTER_SLUG = "omnibus-starter"
OMNIBUS_STARTER_NAME = "Omnibus Starter"
OMNIBUS_STARTER_CONFIG = """
content-dir: content
collections:
  - name: page
    label: Page
    category: Content
    folder: content
    fields:
      - {"label": "Title", "name": "title", "widget": "string", "required": true}
      - {"label": "Body", "name": "body", "widget": "markdown"}
      - {
        "label": "Tags",
        "default": [ "Design" ],
        "max": 2,
        "min": 1,
        "multiple": true,
        "name": "tags",
        "options": [ "Design", "UX", "Dev" ],
        "widget": "select"
        }
      - {
        "label": "PDFs",
        "name": "pdfs",
        "widget": "relation",
        "collection": "resource",
        "display_field": "title",
        "multiple": true,
        "max": 10,
        "min": 1,
        "filter": { field: "filetype", filter_type: "equals", value: "PDF"}
        }
      - name: address
        label: Address
        widget: object
        required: false
        fields:
          - { label: "Street Address", name: "street_address", widget: "string", required: false }
          - { label: "City", name: "city", widget: "string", required: false }
          - { label: "State", name: "state", widget: "string", required: false }
          - { label: "Zip Code", name: "zip", widget: "string", required: false }

  - name: resource
    label: Resource
    category: Content
    folder: content
    fields:
      - {"label": "Title", "name": "title", "widget": "string", "required": true}
      - {"label": "Description", "name": "description", "widget": "text"}
      - {"label": "File", "name": "file", "widget": "file"}
      - {
        "label": "File Type",
        "required": true,
        "name": "filetype",
        "options": [ "PDF", "Word Doc", "PPT" ],
        "widget": "select"
        }

  - name: metadata
    label: Metadata
    category: Settings
    files:
      - file: data/metadata.json
        name: sitemetadata
        label: Site Metadata
        fields:
          - {
            "label": "Item Description",
            "name": "description",
            "widget": "markdown",
            "minimal": true,
            "help": "A description of the item."
          }
          - { "label": "Tags", "default": [ "Design" ], "max": 3, "min": 1, "multiple": true, "name": "tags", "options": [ "Design", "UX", "Dev" ], "widget": "select" }
          - { label: "Align Content", name: "align", widget: "select", options: [ "left", "center", "right" ] }
          - {
            "label": "Comes with fries",
            "name": "fries",
            "widget": "boolean",
            "help": "Whether the course includes fries or not."
          }
      - file: data/metadata.json
        name: othermetadata
        label: Other Metadata
        fields:
          - {
            "label": "Item Description",
            "name": "description",
            "widget": "markdown",
            "minimal": true,
            "help": "A description of the item."
          }
"""


def add_omnibus_starter_repo(apps, schema_editor):
    WebsiteStarter = apps.get_model("websites", "WebsiteStarter")
    WebsiteStarter.objects.get_or_create(
        slug=OMNIBUS_STARTER_SLUG,
        defaults=dict(
            name=OMNIBUS_STARTER_NAME,
            source="local",
            commit=None,
            config=yaml.load(OMNIBUS_STARTER_CONFIG, Loader=yaml.Loader),
        ),
    )


class Migration(migrations.Migration):

    dependencies = [
        ("websites", "0027_websitecollection_websitecollectionitem"),
    ]

    operations = [
        migrations.RunPython(add_omnibus_starter_repo, migrations.RunPython.noop),
    ]
