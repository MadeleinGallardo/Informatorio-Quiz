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
    
    if(totalTime == 0){
        location.reload();
  
    }   
    else{
    totalTime-=1;
    setTimeout("updateClock()",1000);
    }
}

function updateClock2() {
    document.getElementById('contador2').innerHTML = (totalTime);
    
    if(totalTime == 0){
        location.href="/jugar";
  
    }   
    else{
    totalTime-=1;
    setTimeout("updateClock2()",1000);
    }
}