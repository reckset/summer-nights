function TallyTds(){
    const url = "https://mvr35kmrh0.execute-api.us-east-2.amazonaws.com/api/touchdowns"
    var obj;
    var endStr;

    fetch(url, {
        headers: {
            'Content-Type': 'application/json',
        }
        })
        .then(response => response.json())
        .then(data => {
            obj = data;
        })
        .then(() => {
            //console.log(obj.TdsByWeek[1]);
            for (var i = 1; i <= obj.TdsByWeek.length; i++) {
                if (i != 6) {
                    document.getElementById("week-" + i.toString()).innerHTML = obj.TdsByWeek[i-1];
                }
            }

            document.getElementById("dave").innerHTML = obj.Dave;
            document.getElementById("rex").innerHTML = obj.Rex;
            document.getElementById("tim").innerHTML = obj.Tim;
    
            // highlight current lagger orange
            if ((obj.Dave <= obj.Rex) && (obj.Dave <= obj.Tim)) {
            document.getElementById("scoreboard-dave").style.backgroundColor = "orange";
            document.getElementById("scoreboard-dave").style.color = "white";
            }
            if ((obj.Rex <= obj.Dave) && (obj.Rex <= obj.Tim)) {
            document.getElementById("scoreboard-rex").style.backgroundColor = "orange";
            document.getElementById("scoreboard-rex").style.color = "white";
            }
            if ((obj.Tim <= obj.Dave) && (obj.Tim <= obj.Rex)) {
            document.getElementById("scoreboard-tim").style.backgroundColor = "orange";
            document.getElementById("scoreboard-tim").style.color = "white";
            }

            // highlight current leader green
            if ((obj.Dave > obj.Rex) && (obj.Dave > obj.Tim)) {
                document.getElementById("scoreboard-dave").style.backgroundColor = "green";
                document.getElementById("scoreboard-dave").style.color = "white";
                }
                if ((obj.Rex > obj.Dave) && (obj.Rex > obj.Tim)) {
                document.getElementById("scoreboard-rex").style.backgroundColor = "green";
                document.getElementById("scoreboard-rex").style.color = "white";
                }
                if ((obj.Tim > obj.Dave) && (obj.Tim > obj.Rex)) {
                document.getElementById("scoreboard-tim").style.backgroundColor = "green";
                document.getElementById("scoreboard-tim").style.color = "white";
                }
        });
}