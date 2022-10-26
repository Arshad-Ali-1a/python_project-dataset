document.addEventListener('DOMContentLoaded',main)

function main(){
	const headers=document.querySelectorAll(".sort_keys")
	var table_rows= document.querySelectorAll(".table-row")
	table_rows= Array.from(table_rows)
	// console.log((table_rows[4].querySelector("#tableDataYear").innerHTML));


	//for sorting
	headers.forEach(element => {
		element.addEventListener("click",event =>{

			if ((! element.dataset.sort_type) || (element.dataset.sort_type==="descending")) element.dataset.sort_type="ascending";
			else element.dataset.sort_type="descending";


			table_rows.sort((a,b) => {

				a=a.querySelector(`#table${element.id}`).innerHTML
				b=b.querySelector(`#table${element.id}`).innerHTML

				if (element.dataset.sort_type==="ascending"){
					if(a=="None" && b=="None") return 0
					else if (a=="None") return 1
					else if (b=="None") return -1

					return(parseInt(a)-parseInt(b))
				}

				else if (element.dataset.sort_type==="descending"){
					if(a=="None" && b=="None") return 0
					else if (b=="None") return -1
					else if (a=="None") return 1

					return(parseInt(b)-parseInt(a))
				}

				else{
					console.log("problem in sorting")
					return 0 
				}
					
				//then some problem
			})

			//making table empty.
			document.querySelector(".table-content").innerHTML = "";
			
			//adding in table
			var count=1;
			for (let row of table_rows) {
				row.querySelector(`#tableSlno`).innerHTML=count;
				count++;
				document.querySelector(".table-content").appendChild(row)

			}		
		})
	});

	// for sticky header
	var header=document.querySelector(".table-header")
	header_position= header.offsetTop ;
	header_width= header.offsetWidth ;

	// window.onresize=()=>{
	// 	if(window.pageYOffset<header_position){
	// 		header_width= header.offsetWidth ;
	// 		console.log(header_width)
	// 	}
	// }

	window.onscroll=()=>{

		if(window.pageYOffset>= header_position){
			header.classList.add("sticky_header")
			header.style.width=`${header_width}px`
		}
		else{
			header.classList.remove("sticky_header")
			header.style.width="100%"
		}

	}	

}