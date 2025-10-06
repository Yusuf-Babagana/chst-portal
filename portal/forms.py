from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import Application, SchoolAttended, SSCEResult, UploadedDocument


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ReferralCodeForm(forms.Form):
    code = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter referral code (optional)',
            'class': 'form-control'
        })
    )


class SectionAForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'passport_photo', 'first_name', 'surname', 'other_names',
            'date_of_birth', 'phone', 'email', 'address', 'lga', 'state_of_origin',
            'guardian_name', 'guardian_phone', 'guardian_address', 'guardian_relationship'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'guardian_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['passport_photo', 'date_of_birth', 'address', 'guardian_address']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})


class SchoolAttendedForm(forms.ModelForm):
    class Meta:
        model = SchoolAttended
        fields = ['school_name', 'from_year', 'to_year']
        widgets = {
            'school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'from_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY'}),
            'to_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY'}),
        }


SchoolAttendedFormSet = inlineformset_factory(
    Application,
    SchoolAttended,
    form=SchoolAttendedForm,
    extra=3,
    max_num=3,
    can_delete=True
)


class SSCEResultForm(forms.ModelForm):
    class Meta:
        model = SSCEResult
        fields = [
            'exam_type', 'exam_number', 'centre_number', 'centre_name', 'year',
            'awaiting_result', 'english', 'mathematics', 'biology', 'chemistry',
            'physics', 'subject_6', 'grade_6', 'subject_7', 'grade_7',
            'subject_8', 'grade_8', 'subject_9', 'grade_9'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'awaiting_result':
                self.fields[field].widget.attrs.update({'class': 'form-control'})


SSCEResultFormSet = inlineformset_factory(
    Application,
    SSCEResult,
    form=SSCEResultForm,
    extra=2,
    max_num=2,
    can_delete=True
)


class SectionDForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_choice', 'second_choice']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class SectionEForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['declaration_text']
        widgets = {
            'declaration_text': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Type your full name and declaration statement here...'
            })
        }


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedDocument
        fields = ['document_type', 'document_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['document_type'].widget.attrs.update({'class': 'form-control'})


DocumentUploadFormSet = inlineformset_factory(
    Application,
    UploadedDocument,
    form=DocumentUploadForm,
    extra=5,
    max_num=10,
    can_delete=True
)
