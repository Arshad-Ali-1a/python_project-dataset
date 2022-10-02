from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from colleges import *

#TODO check whether we can import using exec, to just import the college needed.
#TODO fix the back button... and add that clicking college name takes to this page in a new tab.
def index(request,college:str):
    college=college.upper()
    college=College.instances.get(college,None)
    if not college: return HttpResponse("wrong college..")

    return render(request,'college_info/index.html',{"college":college})