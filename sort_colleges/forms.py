from logging import PlaceHolder
from django import forms

class FormStudent(forms.Form):
    form_rank= forms.IntegerField(required=True,max_value=100000,min_value=1,label="Eamcet Rank")
    form_gender=forms.CharField(required=True,label="Gender",widget=forms.RadioSelect(choices=[("Boys","Male"), ("Girls","Female")]))
    
    form_category=forms.CharField(required=True,label="Category",widget=forms.RadioSelect(choices=[("OC","OC"),("BC_A","BC_A"),("BC_B","BC_B"),("BC_C","BC_C"),("BC_D","BC_D"),("BC_E","BC_E"),("SC","SC"),("ST","ST")]))
    form_branch_categories=forms.CharField(required=True,label="Branch Categories",widget=forms.CheckboxSelectMultiple(choices=[('COMPUTER','COMPUTER'), ('COMPUTER_2','COMPUTER_2'), ('ELECTRICAL','ELECTRICAL'), ('COMPUTER_3','COMPUTER_3'),
             ('ELECTRICAL_2','ELECTRICAL_2'), ('MECHANICAL','MECHANICAL'), ('MECHANICAL_2','MECHANICAL_2'), ('CHEMICAL','CHEMICAL'), ('PHARMACY','PHARMACY')]))
    
    form_latitude=forms.FloatField(required=True, label="Latitude",min_value=15,max_value=20)
    form_longitude=forms.FloatField(required=True, label="Longitude",min_value=77 ,max_value=82)

    form_sorting_key=forms.CharField(required=True,label="Sorting Key",widget=forms.RadioSelect(choices=[('placement_percent','placement_percent'), ('highest_salary','highest_salary'), 
    ('lowest_salary','lowest_salary'), ('salary_mode','salary_mode'), ('salary_mean','salary_mean'), ('salary_median','salary_median'), ('total_offers','total_offers'), ('companies_visited','companies_visited'), ('year','year'), 
            ('total_intake','total_intake'), ('fees','fees'), ('probability','probability'), ('closing_rank','closing_rank'), ('distance','distance')]))