
document.addEventListener('DOMContentLoaded',()=>{
	console.log("hoihihihihi")
	var table_rows= document.querySelectorAll(".table-row")
	table_rows= Array.from(table_rows)


	document.getElementById("OriginalSort").addEventListener("click",(event)=>{

		const element= event.target;
		if ((! element.dataset.sort_type) || (element.dataset.sort_type==="descending")) element.dataset.sort_type="ascending";
		else element.dataset.sort_type="descending";

	
		//making table empty.
		document.querySelector(".table-content").innerHTML = "";

		//adding in table
		if (element.dataset.sort_type="descending") var table_rows_new=table_rows.reverse()
		else var table_rows_new=table_rows

		var count=1;
		for (let row of table_rows_new) {
			row.querySelector(`#tableSlno`).innerHTML=count;
			count++;
			document.querySelector(".table-content").appendChild(row)
		}
	})

})