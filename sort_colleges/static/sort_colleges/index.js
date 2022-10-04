function get_location(){
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            var latitude=position.coords.latitude;
            var longitude=position.coords.longitude;
            
            console.log(latitude,longitude);

            //in form..
            document.querySelector("#id_form_latitude").value=latitude;
            document.querySelector("#id_form_longitude").value=longitude;
        })
    }

}

document.addEventListener("DOMContentLoaded",(event) => {
    get_location();

    //putting into form
    if(rank=localStorage.getItem("rank")){

        document.querySelector("#id_form_rank").value=rank;

        gender=localStorage.getItem("gender");
        document.querySelector(`input[value="${gender}"]`).checked=true;

        category=localStorage.getItem("category");
        document.querySelector(`input[value="${category}"]`).checked=true;
    }

    //storing in localstorage.
    var frm= document.querySelector('form[id="details"]')
    frm.onsubmit=() => {
        // localStorage.getItem("rank")
        const form = new FormData(frm);
        const data = Object.fromEntries(form); // data is an js object.

        rank=data["form_rank"]
        gender=data["form_gender"]
        category=data["form_category"]


        localStorage.setItem("rank",rank)
        localStorage.setItem("gender",gender)
        localStorage.setItem("category",category)

        console.log(rank,gender,category)

    }

});

