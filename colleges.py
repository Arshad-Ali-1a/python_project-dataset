from json import load, dump
from requests import get
from matplotlib import pyplot
from pathlib import Path
from numpy import inf

# TODO add an encryption and decryption method to key.
# TODO add a function to display all the branches sorted properly in sorted colleges.
# Srikar
# monish
# arshad
# all backslashes in file paths are replaced by forward slash, for heroku... but it works in windows also.

# getting the base path..
# _pp = str(Path().resolve()).split("\\")
# _ind = len(_pp)-1-(_pp[::-1].index("python_project-dataset"))
# _base_path = "\\".join(_pp[:_ind+1])


class Branch():
    _file_all_branches = r"Files/college_info/branch/courses_detail.json"#removed _base_url from here..
    _file_all_branches_category = r"Files/college_info/branch/courses_category.json"

    with open(_file_all_branches, "r") as j1, open(_file_all_branches_category, "r") as j2:
        all_branches = load(j1)
        all_branches_category = load(j2)

    branches = tuple(all_branches.keys())  # to get the branch number.

    def __init__(self, code):

        assert code in Branch.all_branches, "Wrong branch name"

        self.code = code
        self.name = Branch.all_branches[code]["branch_name"]
        self.category = Branch.all_branches[code]["branch_category"]
        # +1 as index starts at 0.
        self.position = Branch.branches.index(self.code)+1

    def __repr__(self):
        return f"Branch({self.code})"

    def __str__(self):
        return self.code


class CollegeBranch(Branch):

    def __init__(self, code, college_code, eamcet_d="manual", placement_d="manual"):

        # to open files when eamcet_d or placement_d are not provided, eg: when creating a CollegeBranch individually(not from College class)
        if eamcet_d == "manual":
            with open(rf"Files/college_info/all_colleges/{college_code}/{college_code}_eamcet_info.json", "r") as j:#removed _base_url from here..
                eamcet_d = load(j)
        if placement_d == "manual":
            with open(rf"Files/college_info/all_colleges/{college_code}/{college_code}_placement_analysis.json", "r") as j:#removed _base_url from here..
                placement_d = load(j)

        # super().__init__(code)
        Branch.__init__(self, code)
        self.college = college_code

        # adding branch details.
        for branch in eamcet_d["branches_details"]:
            if branch["branch_code"] == code:
                self.intake = branch["branch_intake"]
                self.fees = branch["branch_fees"]
                break
        else:
            raise AttributeError(
                "The given branch is not present in the given college.")

        # closing ranks....'and' is used as some colleges have new courses that they did not have in 2019, or 2020.
        self.clsrnk21 = p[self.code] if (
            p := (placement_d["closing_ranks_2021"])) and self.code in p else None
        self.clsrnk20 = p[self.code] if (
            p := (placement_d["closing_ranks_2020"])) and self.code in p else None
        self.clsrnk19 = p[self.code] if (
            p := (placement_d["closing_ranks_2019"])) and self.code in p else None

    def __repr__(self):
        return f"CollegeBranch({self.code},{self.college})"

    def __str__(self):
        return f"{self.code}:{self.college}"


# TODO add __str__ to all the classes... in __repr__, add a proper representation to create a class like that again.

class College():

    instances = {}
    all_colleges = list()
    SORTING_KEYS = (
        "placement_percent",
        "highest_salary",
        "lowest_salary",
        "salary_mode",
        "salary_mean",
        "salary_median",
        "total_offers",
        "companies_visited",
        "year",
        "total_intake",
        "fees",
        "probability",
        "closing_rank",
        "distance",
    )
    CATEGORIES = (
        "OC",
        "BC_A",
        "BC_B",
        "BC_C",
        "BC_D",
        "BC_E",
        "SC",
        "ST",
    )
    FILTER_KEYS = {
        "coed": (True, False),
        "aided": (True, False),
        "pvt": (True, False),
        "affiliated": ("JNTUH", "OU", "KU", "SR UNIVERSITY", "ANURAG UNIVERSITY"),
        "year_before": (1925, 2021),
        "hostel": ((True, False), "gender"),
        "total_intake_greater": (149, 1740),
        "total_intake_lesser": (149, 1740),
        "fees_greater": (35000, 140000),
        "fees_lesser": (35000, 140000),
        "salary_mean_greater": (2.9, 7.14),
        "salary_median_greater": (2.87, 6.5),
        "salary_mode_greater": (2.87, 11.75),
        "highest_salary_greater": (3.5, 97),
        "total_offers_greater": (25, 2472),
        "companies_visited_greater": (7, 154),
        "district_in": ('HYDERABAD', 'JAGTIAL', 'SANGAREDDY', 'PEDDAPALLI', 'YADADRI BHUVANAGIRI', 'WARANGAL', 'HANAMKONDA', 'BHADRADRI KOTHAGUDEM', 'RAJANNA SIRCILLA', 'RANGAREDDY', 'MEDCHAL', 'MEDAK'),
        "distance_college_lesser": "in km",
        "probability_college_greater": (1, 100),
    }

    def __init__(self, code):
        if code in College.all_colleges:
            print("College already exists..")
            # return  #causing problems , as returning incomplete object.

        self.code = code

        _file_eamcet = rf"Files/college_info/all_colleges/{code}/{code}_eamcet_info.json"
        with open(_file_eamcet, "r") as j:
            eamcet_info = load(j)

        _file_placement = rf"Files/college_info/all_colleges/{code}/{code}_placement_analysis.json"
        with open(_file_placement, "r") as j:
            placement_info = load(j)

        self.eamcet_info = (eamcet_info, placement_info)
        self.placement_info = placement_info  # make @setter for this..
        College.instances[code] = self
        College.all_colleges += [code, ]

    #! __del__ is called just after all instances of an object is deleted...
    #! so __del__ will be called after the college is removed from Colleges.instances.

    def __del__(self):
        if "code" in dir(self):
            # College.instances.pop(self.code)
            College.all_colleges.remove(self.code)

    def __repr__(self): return f"College({self.code})"

    def __str__(self): return self.code

    @property
    def eamcet_info(self):
        # return self.college
        return {
            "code": self.code,
            "college": self.name,
            "coed": self.coed,
            "minority": self.minority,
            "region": self.region,
            "aided": self.aided,
            "pvt": self.pvt,
            "phone": self.phone,
            "address": self.address,
            "place": self.place,
            "hostel": self.hostel,
            "district": self.district,
            "year": self.year,
            "email": self.email,
            "affiliated": self.affiliated,
            "website": self.website,
            "fees": self.fees,
            "total_intake": self.total_intake,
            "coordinates": self.coordinates,
            "branches": self.branches,
            "closing_rank": self.closing_rank,
        }

    @eamcet_info.setter
    def eamcet_info(self, other):
        eamcet_d = other[0]
        placement_d = other[1]

        # all eamcet properties.
        self.name = eamcet_d["college"]
        self.coed = True if eamcet_d["coed"] == "COED" else False
        self.minority = None if (e := (eamcet_d["minority"])) == "NA" else e
        self.region = eamcet_d["region"]
        self.aided = False if eamcet_d["aided"] == "UNAIDED" else True
        self.pvt = True if eamcet_d["gov"] == "PVT" else False
        self.phone = eamcet_d["phone"]
        self.address = eamcet_d["address"]
        self.place = eamcet_d["place"]

        # self.hostel
        if "Boys" in (eh := (eamcet_d["hostel"])):
            if "Girls" in eh:
                self.hostel = "Both"
            else:
                self.hostel = "Boys"
        elif "Girls" in eh:
            self.hostel = "Girls"
        else:
            self.hostel = None

        self.district = eamcet_d["district"]
        self.year = int(y) if (y := (eamcet_d["year"])) != None else None
        self.email = eamcet_d["email"]
        self.affiliated = eamcet_d["affiliated"]
        self.website = eamcet_d["website"]
        self.fees = eamcet_d["fees"]
        self.total_intake = eamcet_d["total_intake"]
        self.coordinates = eamcet_d["coordinates"]
        self.branches = other

        t = [branch for branch in self.branches if branch.clsrnk21 != None]
        self.closing_rank = min(
            t, key=lambda x: x.clsrnk21["OC BOYS"]).clsrnk21["OC BOYS"]

    @property
    def branches(self):
        return self._branches

    @branches.setter
    def branches(self, other):
        eamcet_d = other[0]
        placement_d = other[1]

        l_branches = [CollegeBranch(
            branch, self.code, eamcet_d, placement_d) for branch in eamcet_d["branches"]]
        # to sort branches according to order given by the json by me.
        l_branches.sort(key=lambda x: x.position)
        self._branches = tuple(l_branches)

    @property
    def placement_info(self):
        return {
            "highest_salary": self.highest_salary,
            "lowest_salary": self.lowest_salary,
            "salary_mode": self.salary_mode,
            "salary_mean": self.salary_mean,
            "salary_median": self.salary_median,
            "total_offers": self.total_offers,
            "compaies_visited": self.companies_visited,
            "placement_data_year": self.placement_data_year,
            "placement_percent": self.placement_percent
        }

    @placement_info.setter
    def placement_info(self, other):

        self.highest_salary = other.get("highest_salary", None)
        self.lowest_salary = other.get("lowest_salary", None)
        self.salary_mode = other.get("salary_mode", None)
        self.salary_mean =round(g,2) if (g:=(other.get("salary_mean", None))) else None
        self.salary_median = other.get("salary_median", None)
        self.total_offers = other.get("total_offers", None)
        # yes, I know that spelling of companies is wrong.
        self.companies_visited = other.get("compaies_visited", None)
        self.placement_data_year = other.get("placement_data_year", None)
        self.placement_percent = round(
            (tf * 100 / (self.total_intake)), 2) if (tf := (self.total_offers)) else None

        # TODO add closing rank to sorting options.

    # functions..

    @staticmethod
    def sort_colleges(key: str = "all", colleges: tuple | list = None):

        if colleges == None:
            colleges = College.instances.values()
        else:
            assert all(map(lambda x: x.code in College.instances, colleges)
                       ), f"Invalid parameter for colleges:{colleges}"

        def college_sort(college):  # TODO this function is bad, fix it.
            required_placement = (
                college.salary_mean)*(college.total_offers) if college.salary_mean else 0
            intake = college.total_intake

            # can try to remove intake if branch in last rank in same year as placement.
            for branch in college.branches:
                if not branch.clsrnk21:
                    intake -= int(branch.intake)
                elif branch.category in ("ELECTRICAL_2", "MECHANICAL", "MECHANICAL_2", "CHEMICAL", "PHARMACY"):
                    intake -= round(int(branch.intake)*1/2)

            # print(f"--{intake}")
            return required_placement/college.total_intake
            # return college.highest_salary if college.highest_salary else 0

        if key == "all":  # write a better function for this.
            return(sorted(College.instances.values(), key=college_sort, reverse=True))

        else:  # len(key)==0
            def college_sort(college): ...

            if key in College.SORTING_KEYS:
                return(sorted(College.instances.values(), key=lambda x: a if (a := getattr(x, key)) != None else 0, reverse=True if key not in ("year", "closing_rank", "distance") else False))
                # as spelling of companies_visited is compaies_visited in all placement_analysis.

            else:
                raise AttributeError(
                    "argument given to sort_colleges() is invalid.")

    @classmethod
    def sort_branches(cls, college_sort_key: str = "all", colleges: tuple | list = None):

        # TODO make this function sort branches properly, i.e. such that bad branches of good college come after or in between good bracches of next college.
        # no need for checking as, sort_colleges will check.

        colleges = cls.sort_colleges(college_sort_key, colleges)
        sorted_branches = []
        score = []
        # sorted_branches.extend([branch for branch in college.branches])
        for college in colleges:
            for branch in college.branches:
                sorted_branches.append(branch)
                score.append(branch.position*0.5 +
                             (colleges.index(cls.instances[branch.college]))*2)

        sorted_branches = sorted(sorted_branches, key=lambda x: (
            score[sorted_branches.index(x)], x.position))
        return sorted_branches

    # probility of getting into college.

    @property
    def probability(self):
        if hasattr(self, "_probability"):
            return self._probability
        else:
            raise AttributeError("call College.chance_college() first.")

    @classmethod
    def chance_college(cls, rank: int, gender: str, category: str, branch_categories: tuple | list = Branch.all_branches_category.keys(), precision: int = 5):
        '''
        calculates the probability (in percent) of getting into all the colleges.
        '''
        match(gender.lower()):
            case "boy" | "boys" | "male" | "males": gender = "BOYS"
            case "girl" | "girls" | "female" | "females": gender = "GIRLS"
            case _: raise TypeError("Invalid gender... please choose either boy or girl.")

        assert category in cls.CATEGORIES, "Invalid category... Please check College.CATEGORIES"
        assert all(map(lambda s: s in Branch.all_branches_category, branch_categories)
                   ), "Invalid branch category, please check Branch.all_branches_category.keys()"

        check1 = f"OC {gender}"
        check2 = f"{category} {gender}" if gender != "OC" else None

        # for all colleges..
        for college in cls.instances.values():
            num = 0  # numerator
            den = 0  # denominator
            probs = []

            # for each branch category given.
            for ctgry in branch_categories:

                # for branch in college of the above category.
                for branch in college.branches:
                    if branch.category != ctgry:
                        continue
                    # else
                    num = 0  # numerator
                    den = 0  # denominator

                    if (b := (branch.clsrnk21)):
                        num += (1 if b[check1] >= rank-precision else 0)
                        den += 1
                        if check2:
                            num += (1 if b[check2] >= rank-precision else 0)
                            den += 1
                    if (b := (branch.clsrnk20)):
                        num += (1 if b[check1] >= rank-precision else 0)
                        den += 1
                        if check2:
                            num += (1 if b[check2] >= rank-precision else 0)
                            den += 1
                    if (b := (branch.clsrnk19)):
                        num += (1 if b[check1] >= rank-precision else 0)
                        den += 1
                        if check2:
                            num += (1 if b[check2] >= rank-precision else 0)
                            den += 1

                    try:
                        prob = round(num/den*100, 2)
                    except ZeroDivisionError:
                        prob = 0
                    probs.append(prob)

            college._probability = (
                m-1 if (m := max(probs))-1 > 0 else m+1) if len(probs) > 0 else 0

        # return.
        return tuple(filter(lambda c: c._probability >= 90, cls.instances.values()))

    # distance and duration to all colleges

    @property
    def distance(self):
        if hasattr(self, "_distance"):
            return self._distance
        else:
            raise AttributeError("call College.calculate_dist() first.")

    @property
    def duration(self):
        if hasattr(self, "_duration"):
            return self._duration
        else:
            raise AttributeError("call College.calculate_dist() first.")

    @classmethod
    def calculate_dist(cls, cordfrom: tuple | list):
        cordto = [college.coordinates for college in cls.instances.values()]
        cordto = [",".join(list(map(str, l))) for l in cordto]
        cordto = ";".join(cordto)
        link = rf"https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins={cordfrom[0]},{cordfrom[1]}&destinations={cordto}&travelMode=driving&key=AtzlK9HzrY2w0uAX9mww5QfNVFqBuJDIvK9ZWY3tUPx2HrMqVm4cO8E18_bsVV5E"
        d = get(link).json()

        for i, college in enumerate(cls.instances.values()):
            if(d["resourceSets"][0]["resources"][0]["results"][i]["travelDistance"]==-1):
                college._distance = inf
                college._duration = inf
                
                continue

            college._distance = d["resourceSets"][0]["resources"][0]["results"][i]["travelDistance"]
            college._duration = d["resourceSets"][0]["resources"][0]["results"][i]["travelDuration"]

        return tuple(filter(lambda x: x.distance <= 15, cls.instances.values()))

    # filter colleges

    @classmethod
    def filter_colleges(cls, coed=None, aided=None, pvt=None, affiliated=None, year_before=None, hostel=None,
                        total_intake_greater=None, total_intake_lesser=None, fees_greater=None, fees_lesser=None, salary_mean_greater=None,
                        salary_median_greater=None, salary_mode_greater=None, highest_salary_greater=None, total_offers_greater=None,
                        companies_visited_greater=None, district_in=None, distance_college_lesser=None, probability_college_greater=None, **k):
        # assert all(map(lambda s: s in College.FILTER_KEYS, k)),"Invalid filter key, check College.filter_keys"
        filtered_colleges = list()
        conditions = []
        keys = cls.FILTER_KEYS

        for college in College.instances.values():

            flag = True

            if coed != None:
                if coed == True or coed == False:  # to check if the user does not enter invalid values
                    if not(college.coed == coed):
                        flag = False
                else:
                    raise KeyError(f"wrong key value for coed={coed}")

            if aided != None:
                if aided == True or aided == False:
                    if not(college.aided == aided):
                        flag = False
                else:
                    raise KeyError(f"wrong key value for aided={aided}")

            if pvt != None:
                if pvt == True or pvt == False:
                    if not(college.pvt == pvt):
                        flag = False
                else:
                    raise KeyError(f"wrong key value for pvt={pvt}")

            if affiliated != None:
                if affiliated in keys["affiliated"]:
                    if not(college.affiliated == affiliated):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for affiliated={affiliated}")

            if year_before != None:
                if year_before >= keys["year_before"][0] and year_before <= keys["year_before"][1]:
                    if not(int(college.year) <= year_before):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for year_before={year_before}")

            if hostel != None:
                if (hostel[0] == True or hostel[0] == False) and (hostel[1] == "Boys" or hostel[1] == "Girls"):
                    if hostel[0]:
                        if not(college.hostel == hostel[1] or college.hostel == "Both"):
                            flag = False
                    else:
                        if not(college.hostel == None):
                            flag = False
                else:
                    raise KeyError(
                        f"wrong key value for hostel={hostel}.. eg:(False,'Girls')")

            if total_intake_greater != None:
                if total_intake_greater >= keys["total_intake_greater"][0] and total_intake_greater <= keys["total_intake_greater"][1]:
                    if not(college.total_intake >= total_intake_greater):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for total_intake_greater={total_intake_greater}")

            if total_intake_lesser != None:
                if total_intake_lesser >= keys["total_intake_lesser"][0] and total_intake_lesser <= keys["total_intake_lesser"][1]:
                    if not(college.total_intake <= total_intake_lesser):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for total_intake_lesser={total_intake_lesser}")

            if fees_greater != None:
                if fees_greater >= keys["fees_greater"][0] and fees_greater <= keys["fees_greater"][1]:
                    if not(college.fees >= fees_greater):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for fees_greater={fees_greater}")

            if fees_lesser != None:
                if fees_lesser >= keys["fees_lesser"][0] and fees_lesser <= keys["fees_lesser"][1]:
                    if not(college.fees <= fees_lesser):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for fees_lesser={fees_lesser}")

            if salary_mean_greater != None:
                if salary_mean_greater >= keys["salary_mean_greater"][0] and salary_mean_greater <= keys["salary_mean_greater"][1]:
                    if (college.salary_mean == None):
                        flag = False
                    elif not(college.salary_mean >= salary_mean_greater):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for salary_mean_greater={salary_mean_greater}")

            if salary_median_greater != None:
                if salary_median_greater >= keys["salary_median_greater"][0] and salary_median_greater <= keys["salary_median_greater"][1]:
                    if (college.salary_median == None):
                        flag = False
                    elif not(college.salary_median >= salary_median_greater):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for salary_median_greater={salary_median_greater}")

            if salary_mode_greater != None:
                if salary_mode_greater >= keys["salary_mode_greater"][0] and salary_mode_greater <= keys["salary_mode_greater"][1]:
                    if (college.salary_mode == None):
                        flag = False
                    elif not(college.salary_mode >= salary_mode_greater):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for salary_mode_greater={salary_mode_greater}")

            if highest_salary_greater != None:
                if highest_salary_greater >= keys["highest_salary_greater"][0] and highest_salary_greater <= keys["highest_salary_greater"][1]:
                    if (college.highest_salary == None):
                        flag = False
                    elif not(college.highest_salary >= highest_salary_greater):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for highest_salary_greater={highest_salary_greater}")

            if total_offers_greater != None:
                if total_offers_greater >= keys["total_offers_greater"][0] and total_offers_greater <= keys["total_offers_greater"][1]:
                    if (college.total_intake == None):
                        flag = False
                    elif not(college.total_offers >= total_offers_greater):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for total_offers_greater={total_offers_greater}")

            if companies_visited_greater != None:
                if companies_visited_greater >= keys["companies_visited_greater"][0] and companies_visited_greater <= keys["companies_visited_greater"][1]:
                    if (college.companies_visited == None):
                        flag = False
                    elif not(int(college.companies_visited) >= companies_visited_greater):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for companies_visited_greater={companies_visited_greater}")

            if district_in != None:
                if all(map(lambda x: x in keys["district_in"], district_in)):
                    if not(college.district in district_in):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for district_in={district_in}")

            if distance_college_lesser != None:
                if isinstance(distance_college_lesser, (int, float)):
                    if not(college.distance <= distance_college_lesser):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for distance_college_lesser={distance_college_lesser}")

            if probability_college_greater != None:
                if probability_college_greater >= keys["probability_college_greater"][0] and probability_college_greater <= keys["probability_college_greater"][1]:
                    if not(college.probability >= probability_college_greater):
                        flag = False
                else:
                    raise KeyError(
                        f"wrong key value for probability_college_greater={probability_college_greater}")

            if flag:
                filtered_colleges.append(college)
            flag = True

        return filtered_colleges

    @classmethod
    def graph(cls, param: str = "closing_rank", colleges: tuple | list = None):

        # no need of parameter checking, as College.sort_colleges will do.
        colleges = cls.sort_colleges(param, colleges)

        pltx = []
        plty = []

        for college in colleges:
            pltx.append(college.code)
            plty.append(cp if (cp := (getattr(college, param))) != None else 0)

        pyplot.figure(figsize=(9, 7), facecolor="beige", dpi=170)
        pyplot.plot(pltx, plty, "o-", color="orange")
        pyplot.xlabel("Colleges", labelpad=10)
        pyplot.xticks(rotation=90, fontsize=7, color="black")
        pyplot.yticks(color="black", fontsize=6)
        pyplot.ylabel(f"{param}", labelpad=7)

        # increasing and decreasing...so that we can put text in graph points correctly, so they do not overlap.
        increasing = True if param in (
            "year", "closing_rank", "distance") else False

        if not increasing:
            for i, value in enumerate(plty):
                pyplot.text(i, plty[i], round(plty[i]),
                            size=5, ha="right" if i % 2 else "left", va="top" if i % 2 else "bottom")
        else:
            for i, value in enumerate(plty):
                pyplot.text(i, plty[i], round(plty[i]),
                            size=5, ha="left" if i % 2 else "right", va="top" if i % 2 else "bottom")

        pyplot.savefig("graph.png")


#


# main
if __name__ == "__main__":
    print("you were not supposed to run this...just import.")

else:

    file =r"Files/college_info/colleges_data_entered.json"#removed _base_url from here..
    with open(file, "r") as j:
        j = load(j)

    for college in j:
        if j[college]["eamcet_data_entered"]:
            exec(f'{college}=College("{college}")')
