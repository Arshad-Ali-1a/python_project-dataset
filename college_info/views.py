from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from pandas import read_excel
# Create your views here.

from colleges import *

#TODO check whether we can import using exec, to just import the college needed.
#TODO fix the back button... and add that clicking college name takes to this page in a new tab.
def index(request,college:str):
    college=college.upper()
    college=College.instances.get(college,None)
    if not college: return HttpResponse("""Error 404 ....................wrong college..""")

    return render(request,'college_info/index.html',{"college":college})


def sections(request,section:str,college_code:str):

    college=college_code.upper()
    college=College.instances.get(college,None)
    if not college: return HttpResponse("""Error 404 ....................wrong college for section..""")

    
    #placement analysis and details.
    placement_analysis_available=all((college.highest_salary,college.salary_mean,college.companies_visited,college.total_offers))
    placement_details_available=any((college.highest_salary,college.salary_mean,college.companies_visited,college.total_offers))

    if placement_details_available:

        file_placement_detail=f"Files/college_info/all_colleges/{college.code}/{college.code}_placements.xlsx"

        df=read_excel(file_placement_detail,index_col=0)
        placement_data=enumerate((df.to_dict('split'))["data"],1)
    else:
        placement_data=None





    #sections.
    match(section):
        case "demo":
            return render(request,'college_info/demo.html')
        case "eamcet":
            return render(request,'college_info/section_eamcet.html',{"college":college})
        case "placement":
            return render(request,'college_info/section_placement.html',{"college":college, "placement_analysis_available":placement_analysis_available, "placement_details_available":placement_details_available,"placement_data":placement_data})
        case "clsrnk":
            return render(request,'college_info/section_clsrnk.html',{"college":college})
        
        case _ :
            raise Http404 #404 page not found web error..
            
    