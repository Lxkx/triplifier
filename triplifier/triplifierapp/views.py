from typing import cast
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import uploadCsvForm, convertForm
from .models import csvModel, ttlModel
from utils.triplificator import Triplificator
from django.core.files import File
from django.contrib import messages
import os

# Create your views here.

def triplifier(request):
    if request.method == 'POST':
        if "uploadBut" in request.POST:
            form2 = convertForm()
            form1 = uploadCsvForm(request.POST, request.FILES)
            if form1.is_valid:
                document = form1.save(commit=False)
                if document.csvFileName != "":
                    document.csvFile.name = document.csvFileName+".csv"
                else:
                    document.csvFile.name = str(request.FILES["csvFile"])
                    document.csvFileName = str(request.FILES["csvFile"]).replace(".csv","")

                if (document.csvFileName in list(csvModel.objects.all().values_list('csvFileName',flat=True))):
                    messages.add_message(request, messages.ERROR, 'CSV name already exists !')
                    return redirect('/')
                messages.add_message(request, messages.INFO, 'CSV added !')
                document.save()
                #once saved, the attributes for csvFile change, name and url adapt to the path
                #where it is located (tpData/csv/...) and adapt if file is in duplicate (ex test1_ze24GEZdz.csv)
                return redirect('/')

        elif "convertBut" in request.POST:
            form1 = uploadCsvForm()
            form2 = convertForm(request.POST)
            if form2.is_valid():
                print("POST REQUEST")
                print(form2.cleaned_data.get("title"))
                print(form2.cleaned_data.get("titleRow"))
                print(form2.cleaned_data.get("fileToConvert"))
                print(type(form2.cleaned_data.get("newFileName")))
                print(str(form2.cleaned_data.get("newFileName")))
                print(request.POST.get("newFileName"))
                trpObj = Triplificator("tpData/csv/"+str(form2.cleaned_data.get("fileToConvert"))+".csv"
                , form2.cleaned_data.get("titleRow"), form2.cleaned_data.get("firstDataRow")
                , form2.cleaned_data.get("lastDataRow"), form2.cleaned_data.get("separator")
                , form2.cleaned_data.get("prefixData"), form2.cleaned_data.get("predicatData"), form2.cleaned_data.get("title"))

                trpObj.writeFile("tpData/ttl/"+str(form2.cleaned_data.get("newFileName"))+".ttl")

                ttlObj = ttlModel()
                ttlObj.ttlFileName = str(form2.cleaned_data.get("newFileName"))

                local_file = open("tpData/ttl/"+str(form2.cleaned_data.get("newFileName"))+".ttl", 'rb')
                ttlObj.ttlFile.save(str(form2.cleaned_data.get("newFileName"))+".ttl", File(local_file)) #getting duplicated file in cd
                os.remove(ttlObj.ttlFileName+".ttl") #so we delete this file
                local_file.close()

                ttlObj.save()

                return redirect('/')
    else:
        form1 = uploadCsvForm()
        form2 = convertForm()

    csvObjs = csvModel.objects.all()
    ttlObjs = ttlModel.objects.all()

    return render(request, 'triplifier.html', {"form":form1, "csvFiles":csvObjs, "ttlFiles":ttlObjs, "formConvert":form2})

def exportCSV(request, filename):
    content = open("tpData/csv/"+filename, "r", encoding="utf-8")
    response = HttpResponse(content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

def exportTTL(request, filename):
    content = open("tpData/ttl/"+filename+".ttl", "r", encoding="utf-8")
    response = HttpResponse(content, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)+".ttl"
    return response


def delete_csv_file(request, csvName):
    if request.method == "POST":
        csvFile = csvModel.objects.get(csvFileName=csvName)
        try:
            os.remove("tpData/csv/"+str(csvFile.csvFileName)+".csv") #so we delete this file
            csvFile.delete()
        except:
            print("cannot delete the file as it is still open")
    return redirect('/')

def delete_ttl_file(request, ttlName):
    if request.method == "POST":
        ttlFile = ttlModel.objects.get(ttlFileName=ttlName)
        try:   
            os.remove("tpData/ttl/"+str(ttlFile.ttlFileName)+".ttl") #so we delete this file
            ttlFile.delete()
        except:
            print("cannot delete the file as it is still open")
    return redirect('/')