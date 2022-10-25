const url= document.URL;
const college_code="cbit";
url_fetch = url.replace("demo/g",`eamcet/${college_code}`);
console.log(url_fetch)



function put_data(htm) {
    document.getElementById("sections").innerHTML=htm
}


document.addEventListener("DOMContentLoaded",()=>{
    

    // fetch(url_fetch)
    // .then(response => {
    //     return (response.text());
    // })
    // .then(htm => {
    //     console.log(htm)
    //     put_data(htm)
    // })

    //setting height of iframe.
    window_height=window.innerHeight
    console.log(window_height)
    document.getElementById("sections").style.height=`${window_height-20}px`;
    // console.log(document.getElementById("sections").style.height)
    
    //changing iframe src
    document.getElementById("sections").setAttribute("src",url_fetch)
})

