from django.forms import (
    ModelForm,
    TextInput,
    DateInput as DI,
    modelformset_factory,
)

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
        """Return True if mandatory fields have changed, for new forms.

        This allows users to fill in partially filled-in formset, where only
        information for some players is filled in, and the rest is left blank.

        """
        # If we are updating an existing instance, just check if there's changed data
        if self.instance.id is not None:
            return bool(self.changed_data)

        # If we are creating a new instance, ensure mandatory fields are filled
        # in to mark as a changed form. Other forms are ignored as unchanged.
        mandatory_fields = {"date", "wfdf_userid"}
        return set(self.changed_data).issuperset(mandatory_fields)


def accreditationformset_factory(extra):
    return modelformset_factory(
        model=Accreditation, form=AccreditationForm, extra=extra
    )
