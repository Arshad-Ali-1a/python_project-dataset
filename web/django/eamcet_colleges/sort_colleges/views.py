from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from pathlib import Path
import sys
from .forms import FormStudent
from json import loads
# Create your views here.

_pp = str(Path().resolve()).split("\\")
_ind = len(_pp)-1-(_pp[::-1].index("python_project-dataset"))
base_path = "\\".join(_pp[:_ind+1])
print(base_path)
sys.path.append(base_path)

from colleges import *


def index(request):
        if request.method == "POST":

            try:
                filled_form = FormStudent(request.POST)

                if filled_form.is_valid():
                    form_data = filled_form.cleaned_data
                    print(form_data)
                    return display(form_data,request)

                else: return render(request,r"sort_colleges\index3.html",{"form":FormStudent(filled_form)})


            except AttributeError as er:
                er=str(er) 
                if "FormStudent"in er and "get" in er:
                    return render(request,r"sort_colleges\index3.html",{"warning":"please select at least one category","form":FormStudent()})
                else:return HttpResponse("Errrrrr")
        else:
            return render(request,r"sort_colleges\index3.html",{"form":FormStudent()})
            

def display(data,request):
    College.calculate_dist((data["form_latitude"],data["form_longitude"]))
    College.chance_college(data["form_rank"],data["form_gender"],data["form_category"],loads(data["form_branch_categories"].replace("'",'"')))
    colleges=College.sort_colleges(data["form_sorting_key"])
    # return HttpResponse(data["form_branch_categories"].replace("'",'"'))
    detailed_colleges=[]
    for i,college in enumerate(colleges):
        detailed_colleges.append((i,college,getattr(college,data["form_sorting_key"])))
        

    return render(request,r"sort_colleges\display.html",{"key":data["form_sorting_key"],"data_list":detailed_colleges})

