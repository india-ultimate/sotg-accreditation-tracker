from django.forms import ModelForm, TextInput, DateInput as DI, modelformset_factory

from tracker.models import Accreditation


class DateInput(DI):
    input_type = "date"


class AccreditationForm(ModelForm):
    class Meta:
        model = Accreditation
        fields = [
            "name",
            "email",
            "type",
            "date",
            "uc_username",
            "wfdf_userid",
        ]
        widgets = {
            "name": TextInput(attrs={"readonly": "readonly"}),
            "email": TextInput(
                attrs={"readonly": "readonly", "type": "hidden"}
            ),
            "uc_username": TextInput(
                attrs={"readonly": "readonly", "type": "hidden"}
            ),
            "date": DateInput(),
        }

    def has_changed(self):
        """Return True if mandatory fields have changed."""
        mandatory_fields = {'date', 'wfdf_userid'}
        return set(self.changed_data).issuperset(mandatory_fields)

def accreditationformset_factory(extra):
    return modelformset_factory(model=Accreditation, form=AccreditationForm, extra=extra)


