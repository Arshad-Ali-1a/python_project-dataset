
document.addEventListener("DOMContentLoaded",()=>{
    
    const url= document.URL;
    const college_code=document.getElementById("college_code").innerHTML;




    //setting height of iframe.
    window_height=window.innerHeight
    heading_height=document.getElementById("heading").offsetHeight
    console.log(window_height)
    document.getElementById("sections").style.height=`${window_height-100-heading_height}px`;
    // console.log(document.getElementById("sections").style.height)
    

    //changing iframe src

    document.querySelectorAll(".nav-a").forEach((element) => {
        element.addEventListener("click",(event) => {
            url_fetch = url.replace(college_code,`sections/${element.dataset.link}/${college_code}`);
            console.log(url_fetch)
            document.getElementById("sections").setAttribute("src",url_fetch)
        })
    })
})


