$(function() {
    $(".toggle").on("click", function() {
        if ($(".item").hasClass("active")) {
            $(".item").removeClass("active");
            $(this).find("a").html("<i class='fas fa-bars'></i>");
        } else {
            $(".item").addClass("active");
            $(this).find("a").html("<i class='fas fa-times'></i>");
        }
    });
});

var myVar;

function myFunction() {
  myVar = setTimeout(showPage, 2000);
}

function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("myDiv").style.display = "block";
}



function secondsToString(seconds) {
    var minute = Math.floor((seconds / 60) % 60);
    minute = (minute < 10)? '0' + minute : minute;
    var second = seconds % 60;
    second = (second < 10)? '0' + second : second;
    return minute + ':' + second;
}
    


function updateClock() {
    document.getElementById('contador').innerHTML = (totalTime);
    document.getElementById('contador2').innerHTML = (totalTime-15);
    
    if (totalTime == 15){
        var extra1 = document.getElementById('juego');
        var extra = document.getElementById('pre-juego');
        var extra2 = document.getElementById('pregunta-visible');
        extra.style.display = 'none';
        extra1.style.display = 'block'
        extra2.style.display = 'block'
    }
    
    if(totalTime == 0){
        location.reload();
        // document.getElementById("selesion").innerHTML = "Paragraph changed!";
        // var intro = document.getElementById('selesion');
        // intro.style.display = 'block';
            
        // function programarAviso(){
        //     setTimeout(function(){mostrarAviso()},9000); 
        // }
        
        // function mostrarAviso(){
        //     document.getElementById('listo').click();
        // }
            
        // mostrarAviso();
            
        
    }   
    else{
    totalTime-=1;
    setTimeout("updateClock()",1000);
    }
}
    