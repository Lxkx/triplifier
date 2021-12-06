import re
from django import forms
from django.db.models import fields

from .models import csvModel, ttlModel

class uploadCsvForm(forms.ModelForm):
    class Meta:
        model = csvModel
        fields = ('csvFileName', 'csvFile')
        labels = {
            "csvFileName": "CSV file name",
            "csvFile": "Choose a file to upload"
        }
    
    def __init__(self, *args, **kwargs):
        super(uploadCsvForm, self).__init__(*args, **kwargs)
        self.fields['csvFileName'].required = False


class convertForm(forms.Form):
    
    fileToConvert = forms.ModelChoiceField(queryset=csvModel.objects.all(), label="Choose a CSV file to convert")

    choicesTitle = [('select1','Yes, with titles'),
                    ('select2','No, without titles')]
    title = forms.ChoiceField(choices=choicesTitle, widget=forms.RadioSelect, label="Does your file have a title row ?")

    titleRow = forms.IntegerField(min_value=0, required=False, label="Title row number")
    firstDataRow = forms.IntegerField(min_value=0, required=False, label="First data row number")
    lastDataRow = forms.IntegerField(min_value=0, required=False, label="Last data row number")
    separator = forms.CharField(max_length=1, required=False, label="Separator")
    prefixData = forms.CharField(max_length=100, required=False, label="Data prefix")
    predicatData = forms.CharField(max_length=100, required=False, label="Predicat prefix")

    newFileName = forms.CharField(max_length=30, label="TTL file name")

    def clean(self):
        cleaned_data = super().clean()
        print("CLEAN TOUT COURT")
        title = self.cleaned_data.get("title")
        titleRow = self.cleaned_data.get("titleRow")
        firstDataRow = self.cleaned_data.get("firstDataRow")
        lastDataRow = self.cleaned_data.get("lastDataRow")
        
        if (title=="select2" and titleRow!=None):
            raise forms.ValidationError("No title row needed")
        
        if ( (titleRow!=None and firstDataRow!=None) and titleRow > firstDataRow):
            raise forms.ValidationError("Title Row should be < to First Row")

        if ( (titleRow!=None and lastDataRow!=None) and titleRow > lastDataRow):
            raise forms.ValidationError("Title Row should be < to Last Row")

        if ( (lastDataRow!=None and firstDataRow!=None) and firstDataRow > lastDataRow):
            raise forms.ValidationError("First Row should be < to Last Row")

    def clean_fileToConvert(self):
        return self.cleaned_data.get("fileToConvert")

    #best way to handle the form
    def clean_separator(self): #when empty in form, here not None
        separator = self.cleaned_data.get("separator")
        if (separator != ""):
            X = re.search(r"[A-Za-z0-9]", separator)
            if (X!=None):
                raise forms.ValidationError("This is not a valid separator")
            else:
                return separator
        else:
            return None

    def clean_prefixData(self):
        prefixData = self.cleaned_data.get("prefixData")
        if (prefixData!=""):
            X = re.search(r'^[a-zA-Z]*: ', prefixData)
            if (X==None):
                raise forms.ValidationError("Data prefix invalid")

    def clean_predicatData(self):
        predicatData = self.cleaned_data.get("predicatData")
        if (predicatData!=""):
            X = re.search(r'^[a-zA-Z]*: ', predicatData)
            if (X==None):
                raise forms.ValidationError("Predicat prefix invalid")

    def clean_newFileName(self):
        newFileName = self.cleaned_data.get("newFileName")
        if (newFileName!=None):
            X = re.search(r'^[a-zA-Z0-9]', newFileName)
            if (X==None):
                raise forms.ValidationError("Put a simple name")



    def __init__(self, *args, **kwargs):
        super(convertForm, self).__init__(*args, **kwargs)
        self.initial['title'] = 'select1'