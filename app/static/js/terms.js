
function getterms(){
    $.ajax({
        url: "/api/terms", 
        dataType: "json",
        jsonp: "jsonp",
        cache: false,
        cors: true,
        success: function(data) {
        console.log("Yes");
        console.log(data);
        cards = 3;
        let row = document.createElement('div');
        row.className = 'row';
        for(var i=0;i<data.length;i++){
            
            if ( cards >= 3 ){
                let row = document.createElement('div');
                row.className = 'row'; 
                cards = 0
                console.log("Row at " + data[i]['company_name'])
            }else{ cards++ ; let row = document.createElement('div'); } 
            
            let card = document.createElement('div');
            if ( data[i]['count'] == 0 ){
                card.className = 'card col-xl-3 text-white bg-dark o-hidden h-120';
            }else if ( data[i]['count'] < 5 ){
            card.className = 'card col-xl-3 text-black bg-light o-hidden h-120';
            }else if ( data[i]['count'] < 15 ){
                card.className = 'card col-xl-3 text-black bg-primary o-hidden h-120';
            }else if ( data[i]['count'] < 25 ){
                card.className = 'card col-xl-3 text-black bg-warning o-hidden h-120';
            }else if ( data[i]['count'] >= 25 ){
                card.className = 'card col-xl-3 text-black bg-danger o-hidden h-120';
            }else{
            card.className = 'card col-xl-3 text-black bg-light o-hidden h-120';
            }

            let cardBody = document.createElement('div');
            cardBody.className = 'card-body';
    
            let title = document.createElement('h6');
            title.innerText = data[i]['company_name'] + " " + data[i]['count'] ;
            title.className = 'float-left';

    
            cardBody.appendChild(title);
            card.appendChild(cardBody);
            row.appendChild(card);
            comapny.appendChild(row);
        }
    }});
}