from django import forms
from django.contrib.auth.models import User
from ems.models import Event, Location, Reservation, Category

class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    """
    first_name = forms.CharField(label="First Name", max_length=30,  
                                                        widget=forms.TextInput(attrs={'class':'form-control ', 'placeholder':'First Name'}),
                                                        error_messages={'required': 'No first name entered'})
    last_name = forms.CharField(label="Last Name" , max_length=30,  
                                                        widget=forms.TextInput(attrs={'class':'form-control ', 'placeholder':'Last Name'}),
                                                        error_messages={'required': 'No last name entered'})
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label="Username",
                                error_messages={'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters", 'required':'No username entered'},
                                widget=forms.TextInput(attrs={'class':'form-control ', 'placeholder':'Username'}))
    email = forms.EmailField(label="E-mail",  widget=forms.EmailInput(attrs={'class':'form-control ', 'placeholder':'Email'}),
                                error_messages={'required': 'No email entered'})
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'class':'form-control ', 'placeholder':'Password'}),
                                error_messages={'required': 'No password entered'})
    password2 = forms.CharField(label="Password (again)",
                                widget=forms.PasswordInput(attrs={'class':'form-control ', 'placeholder':'Re-Type Password'}),
                                error_messages={'required': 'Password not confirmed'})

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError("A user with that username already exists.")
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("This email address is already in use. Please supply a different email address.")
        return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The two password fields didn't match.")
        return self.cleaned_data


class EventCreationForm(forms.Form):
    name = forms.CharField(label='Name', max_length=255, widget=forms.TextInput(attrs={'class':'form-control '}))
    category =  forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class':'form-control',} ),)
    description = forms.CharField(label='Description', max_length=1000, widget=forms.Textarea(attrs={'class':'form-control'}))
    location =  forms.ModelChoiceField(queryset=Location.objects.all(), widget=forms.Select(attrs={'class':'form-control',} ),)
    start_datetime = forms.DateTimeField(label='Start Date/Time',  widget=forms.DateTimeInput(attrs={'class':'form-control ', 'placeholder':'mm/dd/yy hh:mm'}))
    end_datetime = forms.DateTimeField(label='End Date/Time',  widget=forms.DateTimeInput(attrs={'class':'form-control ', 'placeholder':'mm/dd/yy hh:mm',}))
    is_public = forms.BooleanField(label='Public Event', required=False)
    student_fee = forms.DecimalField(max_digits=4, decimal_places=2, widget=forms.NumberInput(attrs={'value':'0'}))
    staff_fee = forms.DecimalField(max_digits=4, decimal_places=2, widget=forms.NumberInput(attrs={'value':'0'}))
    public_fee = forms.DecimalField(max_digits=4, decimal_places=2, widget=forms.NumberInput(attrs={'value':'0'}))


class EventEditForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=255, widget=forms.TextInput(attrs={'class':'form-control '}))
    category =  forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class':'form-control',} ),)
    description = forms.CharField(label='Description', max_length=1000, widget=forms.Textarea(attrs={'class':'form-control '}))
    is_public = forms.BooleanField(label='Public Event', required=False)
    student_fee = forms.DecimalField(max_digits=4, decimal_places=2)
    staff_fee = forms.DecimalField(max_digits=4, decimal_places=2)
    public_fee = forms.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        model = Event
        fields = ('name', 'category', 'description', 'is_public', 'student_fee', 'staff_fee', 'public_fee')

class ReservationEditForm(forms.ModelForm):
    location =  forms.ModelChoiceField(queryset=Location.objects.all(), widget=forms.Select(attrs={'class':'form-control',} ),)
    start_datetime = forms.DateTimeField(label='Start Date/Time',  widget=forms.DateTimeInput(attrs={'class':'form-control','placeholder':'mm/dd/yy hh:mm'}))
    end_datetime = forms.DateTimeField(label='End Date/Time',  widget=forms.DateTimeInput(attrs={'class':'form-control', 'placeholder':'mm/dd/yy hh:mm'}))
    class Meta:
        model = Reservation
        fields = ('location', 'start_datetime', 'end_datetime')


class SummaryReportForm(forms.Form):
    week_start_datetime = forms.DateTimeField(label='Week Starting Date/Time',  widget=forms.DateTimeInput(attrs={'class':'form-control ', 'placeholder':'mm/dd/yy hh:mm'}))

class QueryForm(forms.Form):
	query = forms.CharField(label='SQL SELECT Statement', widget=forms.Textarea(attrs={'class':'form-control '}))

	def clean(self):
	    if self.cleaned_data['query'][:6].lower() != 'select':
	        raise forms.ValidationError("The query must be a SELECT statement.")
	    return self.cleaned_data