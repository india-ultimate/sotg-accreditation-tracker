from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
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
            "date": DateInput(format="%Y-%m-%d"),
        }

    def has_changed(self):
        """Return True if any non auto filled in fields have changed, for new forms.

        This allows users to fill in partially filled-in formset, where only
        information for some players is filled in, and the rest is left blank.

        """
        # If we are updating an existing instance, just check if there's changed data
        if self.instance.id is not None:
            return bool(self.changed_data)

        # If we are creating a new instance, if any of the fields not filled in
        # using Ultimate Central data have changed, mark the form as changed
        non_auto_fields = {"date", "wfdf_userid", "type"}
        return set(self.changed_data).intersection(non_auto_fields)


def accreditationformset_factory(extra):
    return modelformset_factory(
        model=Accreditation, form=AccreditationForm, extra=extra
    )


class AccreditationFormSetHelper(FormHelper):
    form_tag = False
    template = "bootstrap4/table_inline_formset.html"


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "col-6"
        self.helper.add_input(
            Submit("login", "Login", css_class="btn btn-primary")
        )


class LoginView(auth_views.LoginView):
    authentication_form = LoginForm
