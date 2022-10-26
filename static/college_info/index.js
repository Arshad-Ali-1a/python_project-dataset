
document.addEventListener("DOMContentLoaded",()=>{
    
    const url= document.URL;
    const college_code=document.getElementById("college_code").innerHTML;
    url_fetch = url.replace(college_code,`sections/eamcet/${college_code}`); //!logic for eamcet, placement,etc
    console.log(url_fetch)


    //setting height of iframe.
    window_height=window.innerHeight
    heading_height=document.getElementById("heading").offsetHeight
    console.log(window_height)
    document.getElementById("sections").style.height=`${window_height-100-heading_height}px`;
    // console.log(document.getElementById("sections").style.height)
    
    //changing iframe src
    document.getElementById("sections").setAttribute("src",url_fetch)
})

