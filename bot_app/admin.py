import json
import traceback

from django.contrib import admin
from django.contrib.admin.widgets import AdminURLFieldWidget
from django.forms import widgets, ModelForm
from django.utils.safestring import mark_safe

from .models import Error


class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):
        try:
            new_value = json.dumps(json.loads(value), indent=2, sort_keys=True, ensure_ascii=False)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in new_value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return new_value
        except Exception as e:
            print(traceback.format_exc())
            return super(PrettyJSONWidget, self).format_value(value)


class ClickableURLFieldWidget(AdminURLFieldWidget):
    def render(self, name, value, attrs=None, renderer=None):
        return mark_safe(f'<a href=\"{value}\" style="padding: 5px 6px">{value}</a>')


class ErrorAdminForm(ModelForm):
    class Meta:
        model = Error
        widgets = {
            'details': PrettyJSONWidget(),
            'traceback_page': ClickableURLFieldWidget()
        }
        fields = '__all__'


# Register your models here.
@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ["id", ]
    form = ErrorAdminForm
