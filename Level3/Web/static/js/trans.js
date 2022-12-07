var radio=document.getElementsByName("op");
    if(sessionStorage.op){
        for(var i=0;i<radio.length;i++){
            if(radio[i].value==sessionStorage.op){
                radio[i].checked=true;
            }
        }
    }

var input=document.getElementsByTagName("input");
input[input.length-1].onclick=function(){
    for(var i=0;i<radio.length;i++){
        if(radio[i].checked){
            sessionStorage.op=radio[i].value;
        }
    }
}

