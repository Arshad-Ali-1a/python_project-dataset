from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path
import sys
# Create your views here.

_pp = str(Path().resolve()).split("\\")
_ind = len(_pp)-1-(_pp[::-1].index("python_project-dataset"))
base_path = "\\".join(_pp[:_ind+1])
print(base_path)
sys.path.append(base_path)

from colleges import *

def index(request):
    sorted_colleges=College.sort_colleges("closing_rank")
    return render(request,r"home\index2.html",{"data_list": enumerate(sorted_colleges)})
    # return HttpResponse(KMIT.name)


def homepage(request):
    return render(request,r"home\homepage.html",{})



