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
});
