from ckeditor.widgets import CKEditorWidget
from django import forms
from project.models import Project, ProgrammingLanguage


class ProjectForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True,)
    last_name = forms.CharField(max_length=30, required=True,)
    email = forms.EmailField(max_length=254, required=True,)
    project_name = forms.CharField(max_length=30, required=True,)
    project_description = forms.CharField(widget=CKEditorWidget())
    project_notes = forms.CharField(widget=CKEditorWidget())
    select_lang = forms.MultipleChoiceField(
        label='Programda kulanilacak diller ',
        widget=forms.CheckboxSelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['select_lang'].choices = [
            (l.id, l.name) for l in ProgrammingLanguage.objects.all()
        ]

    class Meta:
        model = Project
        fields = (
            'first_name', 'last_name', 'email', 'project_name', 'project_description', 'project_notes', 'select_langs')
