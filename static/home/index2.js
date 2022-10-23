// var properties = [
// 	'SlNO',
// 	'Code',
// 	'College',
// 	'ClosingRank',
// 	'TotalIntake',
// ];
// document.addEventListener('DOMContentLoaded',main)

// function main() {
// properties.forEach(function( val,i ) {
	
// 	var orderClass = '';

// 	document.querySelector("#" + val).click(function(e){//removed all from queryselector
// 		e.preventDefault();
// 		document.querySelectorAll('.filter__link.filter__link--active').not(this).removeClass('filter__link--active');
//         this.toggleClass('filter__link--active');
//         document.querySelectorAll('.filter__link').removeClass('asc desc');

//    		if(orderClass == 'desc' || orderClass == '') {
//             this.addClass('asc');
//     			orderClass = 'asc';
//        	} else {
//             this.addClass('desc');
//        		orderClass = 'desc';
//        	}

// 		var parent = this.closest('.header__item');
//     		var index = document.querySelectorAll(".header__item").index(parent);
// 		var $table = document.querySelector('.table-content');
// 		var rows = $table.find('.table-row').get();
// 		var isSelected = (this).hasClass('filter__link--active');
// 		var isNumber = (this).hasClass('filter__link--number');
			
// 		rows.sort(function(a, b){

// 			var x = (a).find('.table-data').eq(index).text();
//     			var y = (b).find('.table-data').eq(index).text();
				
// 			if(isNumber == true) {
    					
// 				if(isSelected) {
// 					return x - y;
// 				} else {
// 					return y - x;
// 				}

// 			} else {
			
// 				if(isSelected) {		
// 					if(x < y) return -1;
// 					if(x > y) return 1;
// 					return 0;
// 				} else {
// 					if(x > y) return -1;
// 					if(x < y) return 1;
// 					return 0;
// 				}
// 			}
//     		});

//             Object.keys(rows).forEach(function(row,index) {
// 			$table.append(row);
// 		});

// 		return false;
// 	});

// });

// }


document.addEventListener('DOMContentLoaded',main)

function main(){
	const headers=document.querySelectorAll(".sort_keys")
	var table_rows= document.querySelectorAll(".table-row")
	table_rows= Array.from(table_rows)
	console.log((table_rows));
	headers.forEach(element => {
		element.addEventListener("click",event =>{

			if ((! element.dataset.sort_type) || (element.dataset.sort_type==="descending")) element.dataset.sort_type="ascending";
			else element.dataset.sort_type="descending";


			table_rows.sort((a,b) => {
				a=parseInt(a.querySelector(`#table${element.id}`).innerHTML)
				b=parseInt(b.querySelector(`#table${element.id}`).innerHTML)
				
				if (element.dataset.sort_type==="ascending")return(a-b)
				else if (element.dataset.sort_type==="descending")return(b-a)
				else return 0
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

	

}