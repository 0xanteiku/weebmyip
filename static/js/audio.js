function play(){
       var audio = document.getElementById("audio");
       audio.play();
}

function random_play(){
	var items = ["baka.mp3", "senpai.mp3", "uwu.mp3"];
	var item = items[Math.floor(Math.random()*items.length)];
    var audio = new Audio('/static/crab/'+item);
    audio.play();
}