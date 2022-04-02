import json
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional

main_html_content = """
<!DOCTYPE html>
<html>  
<head>
    <meta charset="UTF-8">
    <title>Find My Route</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
    <!--meta http-equiv="refresh" content="5"-->
</head>
<style>
.main {
    padding: 10px;
    font-size: 20px;
    /* Increased text to enable scrolling */
    padding: 0px 10px;
    min-height: 100%;
}

body {
    height: 97%;
    min-height: 97%;
    font-family: 'Roboto', sans-serif;
    background: #d9eeff;
    overflow: hidden;
}

.controls {
    width: 20%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 25px;
}

.controls:focus {
    border: 4px solid #555;
}

#submit{
    background-color: skyblue;
}

.top_banner {
    text-align: center;
}

#main-data-table{
  margin-left: auto;
  margin-right: auto;
}

.flex-container {
    min-height: 80%;
    display: flex;
    border-radius: 25px;
    text-align: center;
    justify-content: center;
}

.flex-child {
    flex: 1;
    align-self: center;
    border-radius: 25px;
    margin-right: 10px;
}
.flex-container-second {
    min-height: 80%;
    display: flex;
    border-radius: 25px;
    text-align: center;
    justify-content: center;
    flex-direction: column;
}
.flex-first-child-main {
    flex: 1;
    align-self: center;
    border-radius: 25px;
    margin-right: 10px;
    overflow: auto;
    height: 200px;
}
.flex-first-child-main thead th { position: sticky; top: 0; z-index: 1; }

.flex-first-child-second {
    flex: auto;
    align-self: center;
    border-radius: 25px;
    margin-right: 10px;
    overflow: auto;
    height: 200px;
}
.flex-first-child-second thead th { position: sticky; top: 0; z-index: 1; }

table  { border-collapse: collapse; width: 100%; }
th, td { padding: 2px 30px; }
th     { background:#eee; }

.second_child{
    border-radius: 25px;
    width: 200px;
    flex: auto;
    height: 500px;
}
#map {
    align-self: center;
    border-radius: 25px;
    height: 500px;
    width: 100%;
    flex: auto;
  flex-basis: 0;
  flex-grow: 4;

}
.second_col_legend{
    align-self: center;
    border-radius: 25px;
    width: 100%;
    margin-right: 20px;
}
</style>
<body>
            <div class="top_banner">
               <a href="/" style="color: black; text-decoration: none;"><h1>Dashboard</h1></a>
            </div>
            <div>
             
            <input id="dmnd" class="controls" type="number" placeholder="Demand node number" />
            <input id="reli" class="controls" type="number" placeholder="Relief point number" />
            <input id="number" class="controls" type="number" placeholder="Enter number of people" />
            <button id="submit" type="submit" class="controls">Submit</button>

               <script type="text/javascript">
               var myHeaders = new Headers();
               myHeaders.append('pragma', 'no-cache');
               myHeaders.append('cache-control', 'no-cache');

               var myInit = {
               method: 'GET',
               headers: myHeaders,
               };

               fetch("../Data/display_data", myInit)
               .then(function (response) {
                   return response.json();
               }).then(function (apiJsonData) {
                  renderDataInTheTable(apiJsonData);
               })

               function renderDataInTheTable(display_data) {
                    const mytable = document.getElementById("main-data-table");
                    for(var k in display_data) {
                        let newRow = document.createElement("tr");
                        for(var x in display_data[k]){
                            let cell = document.createElement("td");
                            cell.innerText = display_data[k][x];
                            newRow.appendChild(cell);
                            }
                        mytable.appendChild(newRow);
                        }
                    }            
                    document.getElementById("submit").onclick = function () {
                        var requestOptions = {
                            method: 'POST',
                            redirect: 'follow'
                            };
                        fetch(baseUrl+"tableUpdate/?number="+document.getElementById("number").value+"&dmnd="+document.getElementById("dmnd").value+"&reli="+document.getElementById("reli").value, requestOptions)
                        .then(response => response.json())
                        .then(result => {
                            console.log(result),
                            alert("Your request to add "+document.getElementById('number').value+" people in relief point "+document.getElementById('reli').value+" from demand node "+document.getElementById('dmnd').value+" has been sucessfully processed.\\nServer response: "+ result["msg"]);
                            })
                        .catch(error => console.log('error', error));
                    };
                </script>

             </div>
             <div class="flex-container">
                <div class="flex-child">
                    <table id = "main-data-table">
                        <tr>
                          <th>Reliability Value</th>
                          <th>Population Served</th>
                          <th>Population Unserved</th>
                          <th>Demand Nodes</th>
                          <th>Relief Points</th>
                        </tr>
                      </table>
                      <p>
                      Note: Negative values in column 'Population Unserved' shows that there is space to accomodate that much number of people
                      </p>
                </div>
                <div class="second_child">
                    <div id="map">
                    </div>
                    <script
                         src="https://maps.googleapis.com/maps/api/js?key=KEY" type="text/javascript">
                    </script>
                    <div class = "second_col_legend"><table>
<tr>
<td><canvas id="myCanvas">
</canvas></td>
<td><canvas id="myCanvas2">
</canvas></td>
</tr>
<tr>
<td style="text-align:center; vertical-align:top;"><h4>Relief Point</h4></td>
<td style="text-align:center; vertical-align:top;"><h4>Demand Point</h4></td>
</tr>
</table>

<script>
//ctx.arc(x,y,radius,startAngle,endAngle, anticlockwise);  
var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
ctx.canvas.width = "100"
ctx.canvas.height = "50"
ctx.beginPath()
ctx.arc(c.width/2, c.height/2, c.width/4, 0, Math.PI*2, false); // outer (filled)
ctx.arc(c.width/2, c.height/2, c.width/5, 0, Math.PI*2, true); // inner (unfills it)
ctx.fill();
ctx.font = "20px Arial";
ctx.fillText("N", c.width/2.35, c.height/1.55);
var c2 = document.getElementById("myCanvas2");
var ctx2 = c2.getContext("2d");
ctx2.canvas.width = "100"
ctx2.canvas.height = "50"
ctx2.beginPath()
ctx2.arc(c2.width/2, c2.height/2, c2.width/4, 0, Math.PI*2, false); // inner (unfills it)
ctx2.fill();
ctx2.font = "20px Arial";
ctx2.fillStyle = "white";
ctx2.fillText("N", c2.width/2.35, c2.height/1.55);
</script> 

                    </div>
                </div>
                </div>
                         <script>
                    var baseUrl = window.location.protocol+"//"+window.location.hostname+":"+window.location.port+"/"

            const myloc = {
                        lat: 27.302524795918504,
                        lng: 88.59751338243387
                        };
                    var Locations = [
                        ['1', 'Demand', 27.302524795918504, 88.59751338243387, 'setdemand/?dmnd=1'],
                        ['2', 'Demand', 27.309941653731695, 88.59884377512124, 'setdemand/?dmnd=2'],
                        ['3', 'Demand', 27.30582333235349, 88.58828660114838, 'setdemand/?dmnd=3'],
                        ['4', 'Demand', 27.310361103820796, 88.60686894416531, 'setdemand/?dmnd=4'],
                        ['5', 'Demand', 27.293448382503307, 88.5876643286917, 'setdemand/?dmnd=5'],
                        ['6', 'Demand', 27.30007442244496, 88.60322313404959, 'setdemand/?dmnd=6'],
                        ['7', 'Demand', 27.290731480800943, 88.59953239709199, 'setdemand/?dmnd=7'],
                        ['8', 'Demand',27.29443927704333, 88.60976569341749, 'setdemand/?dmnd=8'],
                        ['1', 'Relief', 27.29908312298845, 88.59850259606205, 'setrelief/?reli=1'],
                        ['2', 'Relief', 27.316052526734996, 88.60438310868761, 'setrelief/?reli=2'],
                        ['3', 'Relief', 27.31059938203764, 88.58867470419628, 'setrelief/?reli=3'],
                        ['4', 'Relief', 27.308425729881044, 88.60326660562897, 'setrelief/?reli=4'],
                        ['5', 'Relief', 27.296108563399272, 88.59755852842592, 'setrelief/?reli=5'],
                        ['6', 'Relief', 27.29565087437993, 88.60086281523137, 'setrelief/?reli=6'],
                        ['7', 'Relief', 27.291570492233568, 88.59506962480899, 'setrelief/?reli=7'],
                        ['8', 'Relief', 27.288786566493226, 88.59927488945574, 'setrelief/?reli=8'],
                        ];

                        const map = new google.maps.Map(document.getElementById('map'), {
                            zoom: 14,
                            center: myloc,
                        });

                        var infowindow = new google.maps.InfoWindow();

                        var marker, i;
                        var DemandIcon = {
                            path: google.maps.SymbolPath.CIRCLE,
                            fillOpacity: 1,
                            fillColor: '#ffffff',
                            strokeOpacity: 1,
                            strokeWeight: 1,
                            strokeColor: '#333',
                            scale: 12
                        };
                        var ReliefIcon = {
                            path: google.maps.SymbolPath.CIRCLE,
                            fillOpacity: 1,
                            fillColor: '#000000',
                            strokeOpacity: 1,
                            strokeWeight: 1,
                            strokeColor: '#333',
                            scale: 12
                        };
                        for (i = 0; i < Locations.length; i++) {
                            if (Locations[i][1] == "Demand"){
                                marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(Locations[i][2], Locations[i][3]),
                                    map: map,
                                    icon: ReliefIcon,
                                    url: baseUrl.concat(Locations[i][4]),
                                    label: {color: '#ffffff', fontSize: '12px', fontWeight: '600',
                                    text: Locations[i][0]}
                                });
                            }
                            else if (Locations[i][1] == "Relief"){
                                marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(Locations[i][2], Locations[i][3]),
                                    map: map,
                                    icon: DemandIcon,
                                    url: baseUrl.concat(Locations[i][4]),
                                    label: {color: '#000000', fontSize: '12px', fontWeight: '600',
                                    text: Locations[i][0]}
                                }); 
                            }
                            google.maps.event.addListener(marker, 'click', function() {
                                window.location.href = this.url;
                                window.open(marker.url, '_blank');
                            });
                        }

            </script>
 </body>
</html>
"""

demand_html_content = """
<!DOCTYPE html>
<html>  
<head>
    <meta charset="UTF-8">
    <title>Find My Route</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
    <!--meta http-equiv="refresh" content="5"-->
</head>
<style>
    html {
height: 100%
}
.main {
    padding: 10px;
    font-size: 20px;
    /* Increased text to enable scrolling */
    padding: 0px 10px;
    min-height: 100%;
}

body {
    height: 97%;
    min-height: 97%;
    font-family: 'Roboto', sans-serif;
    background: #d9eeff;
    overflow: hidden;
}

.controls {
    width: 20%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 25px;
}

.controls:focus {
    border: 4px solid #555;
}

#submit{
    background-color: skyblue;
}

.top_banner {
    text-align: center;
}

#main-data-table{
  margin-left: auto;
  margin-right: auto;
}

.flex-container {
    min-height: 80%;
    display: flex;
    border-radius: 25px;
    text-align: center;
    justify-content: center;
}

.flex-child {
    flex: 1;
    align-self: center;
    border-radius: 25px;
    margin-right: 10px;
}
.flex-container-second {
    min-height: 80%;
    display: flex;
    border-radius: 25px;
    text-align: center;
    justify-content: center;
    flex-direction: column;
}
.flex-first-child-main {
    flex: 1;
    align-self: center;
    border-radius: 25px;
    margin-right: 10px;
    overflow: auto;
    height: 200px;
}
.flex-first-child-main thead th { position: sticky; top: 0; z-index: 1; }

.flex-first-child-second {
    flex: auto;
    align-self: center;
    border-radius: 25px;
    margin-right: 10px;
    overflow: auto;
    height: 200px;
}
.flex-first-child-second thead th { position: sticky; top: 0; z-index: 1; }

table  { border-collapse: collapse; width: 100%; }
th, td { padding: 2px 30px; }
th     { background:#eee; }

.second_child{
    border-radius: 25px;
    width: 200px;
    flex: auto;
    height: 500px;
}
#map {
    align-self: center;
    border-radius: 25px;
    height: 500px;
    width: 100%;
    flex: auto;
    flex-basis: 0;
    flex-grow: 4;
}
.second_col_table{
    align-self: center;
    border-radius: 25px;
    margin-right: 20px;
}
.second_col_legend{
    align-self: center;
    border-radius: 25px;
    width: 100%;
    margin-right: 20px;
}
</style>
<body>
             <div class="top_banner">
               <a href="/" style="color: black; text-decoration: none;"><h1>Dashboard</h1></a>
             </div>
             <div>
                <input id="dmnd" class="controls" type="number" placeholder="Demand node number" />
                <input id="reli" class="controls" type="number" placeholder="Relief point number" />
                <input id="number" class="controls" type="number" placeholder="Enter number of people" />
                <button id="submit" type="submit" class="controls">Submit</button>
             </div>
             <div class="flex-container">
                <div class="flex-child">
                <div class="flex-container-second">
                <div class="flex-first-child-main">
                <h3>Main table</h3>
                    <table id = "main-data-table">
                        <thead>
                        <tr>
                          <th>Reliability<br>Value</th>
                          <th>Population<br>Served</th>
                          <th>Population<br>Unserved</th>
                          <th>Demand<br>Nodes</th>
                          <th>Relief<br>Points</th>
                        </tr>
                        </thead>
                      </table>
                      <br>
                </div>
                <div class="flex-first-child-second">
                <h3>Extra table</h3>
                    <table id = "second-data-table">
                    <thead>
                        <tr>
                          <th>Reliability<br>Value</th>
                          <th>Population<br>Served</th>
                          <th>Population<br>Unserved</th>
                          <th>Demand<br>Nodes</th>
                          <th>Relief<br>Points</th>
                        </tr>
                    </thead>
                      </table>
                </div>
                      <p>
                      Note: Negative values in column 'Population Unserved' shows that there is space to accomodate that much number of people
                      </p>
                </div>                      
                </div>
                <div class="second_child">
                    <div id="map">
                    </div>
                    <script
                         src="https://maps.googleapis.com/maps/api/js?key=KEY" type="text/javascript">
                    </script>
                    <div class = "second_col_legend"><table>
<tr>
<td><canvas id="myCanvas">
</canvas></td>
<td><canvas id="myCanvas2">
</canvas></td>
</tr>
<tr>
<td style="text-align:center; vertical-align:top;"><h4>Relief Point</h4></td>
<td style="text-align:center; vertical-align:top;"><h4>Demand Point</h4></td>
</tr>
</table>

<script>
//ctx.arc(x,y,radius,startAngle,endAngle, anticlockwise);  
var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
ctx.canvas.width = "100"
ctx.canvas.height = "50"
ctx.beginPath()
ctx.arc(c.width/2, c.height/2, c.width/4, 0, Math.PI*2, false); // outer (filled)
ctx.arc(c.width/2, c.height/2, c.width/5, 0, Math.PI*2, true); // inner (unfills it)
ctx.fill();
ctx.font = "20px Arial";
ctx.fillText("N", c.width/2.35, c.height/1.55);
var c2 = document.getElementById("myCanvas2");
var ctx2 = c2.getContext("2d");
ctx2.canvas.width = "100"
ctx2.canvas.height = "50"
ctx2.beginPath()
ctx2.arc(c2.width/2, c2.height/2, c2.width/4, 0, Math.PI*2, false); // inner (unfills it)
ctx2.fill();
ctx2.font = "20px Arial";
ctx2.fillStyle = "white";
ctx2.fillText("N", c2.width/2.35, c2.height/1.55);
</script> 

                    </div>
                </div>
                </div>
                <script type="text/javascript">

                var myHeaders = new Headers();
                myHeaders.append('pragma', 'no-cache');
                myHeaders.append('cache-control', 'no-cache');

                var myInit = {
                method: 'GET',
                headers: myHeaders,
                };

                const params = new URLSearchParams(window.location.search)
                for (const param of params) {
                window[param[0]] = [param[1]]
                }
                document.getElementById('dmnd').value = dmnd;
                reli = [];
                fetch("../Data/display_data", myInit)
                .then(function (response) {
                    return response.json();
                }).then(function (apiJsonData) {
                   renderDataInTheTable(apiJsonData);
                   setMarkers();
                })
                function renderDataInTheTable(display_data) {
                    const mytable = document.getElementById("main-data-table");
                    const mytable2 = document.getElementById("second-data-table");
                    let newBody = document.createElement("tbody");
                    let newBody2 = document.createElement("tbody");
                    mytable.appendChild(newBody)
                    mytable2.appendChild(newBody2)
                    for(var k in display_data) {
                        let newRow = document.createElement("tr");
                        let newRow2 = document.createElement("tr");
                        if (display_data[k][3] == dmnd){
                            for(var x in display_data[k]){
                                let cell2 = document.createElement("td");
                                cell2.innerText = display_data[k][x];
                                newRow2.appendChild(cell2);
                            }
                            reli = [...reli,String(display_data[k][4])]
                            newBody2.appendChild(newRow2);
                        }
                        for(var x in display_data[k]){
                            let cell = document.createElement("td");
                            cell.innerText = display_data[k][x];
                            newRow.appendChild(cell);
                            }
                        newBody.appendChild(newRow);
                        }
                    }
                    var baseUrl = window.location.protocol+"//"+window.location.hostname+":"+window.location.port+"/"
                    document.getElementById("submit").onclick = function () {
                        var requestOptions = {
                            method: 'POST',
                            redirect: 'follow'
                            };
                        fetch(baseUrl+"tableUpdate/?number="+document.getElementById("number").value+"&dmnd="+document.getElementById("dmnd").value+"&reli="+document.getElementById("reli").value, requestOptions)
                        .then(response => response.json())
                        .then(result => {
                            console.log(result),
                            alert("Your request to add "+document.getElementById('number').value+" people in relief point "+document.getElementById('reli').value+" from demand node "+document.getElementById('dmnd').value+" has been sucessfully processed.\\nServer response: "+ result["msg"]);
                            })
                        .catch(error => console.log('error', error));
                    };
                    const myloc = {
                        lat: 27.302524795918504,
                        lng: 88.59751338243387
                        };
                    var Locations = [
                        ['1', 'Demand', 27.302524795918504, 88.59751338243387, '&dmnd=1'],
                        ['2', 'Demand', 27.309941653731695, 88.59884377512124, '&dmnd=2'],
                        ['3', 'Demand', 27.30582333235349, 88.58828660114838, '&dmnd=3'],
                        ['4', 'Demand', 27.310361103820796, 88.60686894416531, '&dmnd=4'],
                        ['5', 'Demand', 27.293448382503307, 88.5876643286917, '&dmnd=5'],
                        ['6', 'Demand', 27.30007442244496, 88.60322313404959, '&dmnd=6'],
                        ['7', 'Demand', 27.290731480800943, 88.59953239709199, '&dmnd=7'],
                        ['8', 'Demand',27.29443927704333, 88.60976569341749, '&dmnd=8'],
                        ['1', 'Relief', 27.29908312298845, 88.59850259606205, '&reli=1'],
                        ['2', 'Relief', 27.316052526734996, 88.60438310868761, '&reli=2'],
                        ['3', 'Relief', 27.31059938203764, 88.58867470419628, '&reli=3'],
                        ['4', 'Relief', 27.308425729881044, 88.60326660562897, '&reli=4'],
                        ['5', 'Relief', 27.296108563399272, 88.59755852842592, '&reli=5'],
                        ['6', 'Relief', 27.29565087437993, 88.60086281523137, '&reli=6'],
                        ['7', 'Relief', 27.291570492233568, 88.59506962480899, '&reli=7'],
                        ['8', 'Relief', 27.288786566493226, 88.59927488945574, '&reli=8'],
                        ];

                        const map = new google.maps.Map(document.getElementById('map'), {
                            zoom: 14,
                            center: myloc,
                        });

                        var infowindow = new google.maps.InfoWindow();

                        var marker, i;
                        var DemandIcon = {
                            path: google.maps.SymbolPath.CIRCLE,
                            fillOpacity: 1,
                            fillColor: '#ffffff',
                            strokeOpacity: 1,
                            strokeWeight: 1,
                            strokeColor: '#333',
                            scale: 12
                        };
                        var ReliefIcon = {
                            path: google.maps.SymbolPath.CIRCLE,
                            fillOpacity: 1,
                            fillColor: '#000000',
                            strokeOpacity: 1,
                            strokeWeight: 1,
                            strokeColor: '#333',
                            scale: 12
                        };

                        function setMarkers(){
                        for (i = 0; i < Locations.length; i++) {
                            if (Locations[i][1] == "Demand" && dmnd.includes(Locations[i][0])){
                                marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(Locations[i][2], Locations[i][3]),
                                    map: map,
                                    icon: ReliefIcon,
                                    label: {color: '#ffffff', fontSize: '12px', fontWeight: '600',
                                    text: Locations[i][0]}
                                });
                            }
                            else if (Locations[i][1] == "Relief" && reli.includes(Locations[i][0])){
                                marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(Locations[i][2], Locations[i][3]),
                                    map: map,
                                    icon: DemandIcon,
                                    url: baseUrl+"handler/?dmnd="+dmnd+Locations[i][4],
                                    label: {color: '#000000', fontSize: '12px', fontWeight: '600',
                                    text: Locations[i][0]}
                                });
                                google.maps.event.addListener(marker, 'click', function() {
                                    window.location.href = this.url;
                                    window.open(marker.url, '_blank');
                            });
                            }
                        }
                        }


            </script>
 </body>
</html>
"""

relief_html_content = """
<!DOCTYPE html>
<html>  
<head>
    <meta charset="UTF-8">
    <title>Find My Route</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
    <!--meta http-equiv="refresh" content="5"-->
</head>
<style>
    html {
height: 100%
}
.main {
    padding: 10px;
    font-size: 20px;
    /* Increased text to enable scrolling */
    padding: 0px 10px;
    min-height: 100%;
}

body {
    height: 97%;
    min-height: 97%;
    font-family: 'Roboto', sans-serif;
    background: #d9eeff;
    overflow: hidden;
}

.controls {
    width: 20%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 25px;
}

.controls:focus {
    border: 4px solid #555;
}

#submit{
    background-color: skyblue;
}

.top_banner {
    text-align: center;
}

#main-data-table{
  margin-left: auto;
  margin-right: auto;
}

.flex-container {
    min-height: 80%;
    display: flex;
    border-radius: 25px;
    text-align: center;
    justify-content: center;
}

.flex-child {
    flex: 1;
    align-self: center;
    border-radius: 25px;
    margin-right: 10px;
}
.flex-container-second {
    min-height: 80%;
    display: flex;
    border-radius: 25px;
    text-align: center;
    justify-content: center;
    flex-direction: column;
}
.flex-first-child-main {
    flex: 1;
    align-self: center;
    border-radius: 25px;
    margin-right: 10px;
    overflow: auto;
    height: 200px;
}
.flex-first-child-main thead th { position: sticky; top: 0; z-index: 1; }

.flex-first-child-second {
    flex: auto;
    align-self: center;
    border-radius: 25px;
    margin-right: 10px;
    overflow: auto;
    height: 200px;
}
.flex-first-child-second thead th { position: sticky; top: 0; z-index: 1; }

table  { border-collapse: collapse; width: 100%; }
th, td { padding: 2px 30px; }
th     { background:#eee; }

.second_child{
    border-radius: 25px;
    width: 200px;
    flex: auto;
    height: 500px;
}
#map {
    align-self: center;
    border-radius: 25px;
    height: 500px;
    width: 100%;
    flex: auto;
  flex-basis: 0;
  flex-grow: 4;

}
.second_col_table{
    align-self: center;
    border-radius: 25px;
    margin-right: 20px;
}
.second_col_legend{
    align-self: center;
    border-radius: 25px;
    width: 100%;
    margin-right: 20px;
}
</style>
<body>
             <div class="top_banner">
               <a href="/" style="color: black; text-decoration: none;"><h1>Dashboard</h1></a>
             </div>
             <div>
                <input id="dmnd" class="controls" type="number" placeholder="Demand node number" />
                <input id="reli" class="controls" type="number" placeholder="Relief point number" />
                <input id="number" class="controls" type="number" placeholder="Enter number of people" />
                <button id="submit" type="submit" class="controls">Submit</button>
             </div>
             <div class="flex-container">
                <div class="flex-child">
                <div class="flex-container-second">
                <div class="flex-first-child-main">
                <h3>Main table</h3>
                    <table id = "main-data-table">
                        <thead>
                        <tr>
                          <th>Reliability<br>Value</th>
                          <th>Population<br>Served</th>
                          <th>Population<br>Unserved</th>
                          <th>Demand<br>Nodes</th>
                          <th>Relief<br>Points</th>
                        </tr>
                        </thead>
                      </table>
                      <br>
                </div>
                <div class="flex-first-child-second">
                <h3>Extra table</h3>
                    <table id = "second-data-table">
                    <thead>
                        <tr>
                          <th>Reliability<br>Value</th>
                          <th>Population<br>Served</th>
                          <th>Population<br>Unserved</th>
                          <th>Demand<br>Nodes</th>
                          <th>Relief<br>Points</th>
                        </tr>
                    </thead>
                      </table>
                </div>
                      <p>
                      Note: Negative values in column 'Population Unserved' shows that there is space to accomodate that much number of people
                      </p>
                </div>                      
                </div>
                <div class="second_child">
                    <div id="map">
                    </div>
                    <script
                         src="https://maps.googleapis.com/maps/api/js?key=KEY" type="text/javascript">
                    </script>
                    <div class = "second_col_legend"><table>
<tr>
<td><canvas id="myCanvas">
</canvas></td>
<td><canvas id="myCanvas2">
</canvas></td>
</tr>
<tr>
<td style="text-align:center; vertical-align:top;"><h4>Relief Point</h4></td>
<td style="text-align:center; vertical-align:top;"><h4>Demand Point</h4></td>
</tr>
</table>

<script>
//ctx.arc(x,y,radius,startAngle,endAngle, anticlockwise);  
var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
ctx.canvas.width = "100"
ctx.canvas.height = "50"
ctx.beginPath()
ctx.arc(c.width/2, c.height/2, c.width/4, 0, Math.PI*2, false); // outer (filled)
ctx.arc(c.width/2, c.height/2, c.width/5, 0, Math.PI*2, true); // inner (unfills it)
ctx.fill();
ctx.font = "20px Arial";
ctx.fillText("N", c.width/2.35, c.height/1.55);
var c2 = document.getElementById("myCanvas2");
var ctx2 = c2.getContext("2d");
ctx2.canvas.width = "100"
ctx2.canvas.height = "50"
ctx2.beginPath()
ctx2.arc(c2.width/2, c2.height/2, c2.width/4, 0, Math.PI*2, false); // inner (unfills it)
ctx2.fill();
ctx2.font = "20px Arial";
ctx2.fillStyle = "white";
ctx2.fillText("N", c2.width/2.35, c2.height/1.55);
</script> 

                    </div>
                </div>
                </div>
                <script type="text/javascript">

                var myHeaders = new Headers();
                myHeaders.append('pragma', 'no-cache');
                myHeaders.append('cache-control', 'no-cache');

                var myInit = {
                method: 'GET',
                headers: myHeaders,
                };

                const params = new URLSearchParams(window.location.search)
                for (const param of params) {
                window[param[0]] = [param[1]]
                }
                document.getElementById('reli').value = reli;
    
                var baseUrl = window.location.protocol+"//"+window.location.hostname+":"+window.location.port+"/"
                dmnd = [];
                fetch("../Data/display_data", myInit)
                .then(function (response) {
                    return response.json();
                }).then(function (apiJsonData) {
                   renderDataInTheTable(apiJsonData);
                   setMarkers();
                })
                function renderDataInTheTable(display_data) {
                    const mytable = document.getElementById("main-data-table");
                    const mytable2 = document.getElementById("second-data-table");
                    let newBody = document.createElement("tbody");
                    let newBody2 = document.createElement("tbody");
                    mytable.appendChild(newBody)
                    mytable2.appendChild(newBody2)
                    for(var k in display_data) {
                        let newRow = document.createElement("tr");
                        let newRow2 = document.createElement("tr");
                        if (display_data[k][4] == reli){
                            for(var x in display_data[k]){
                                let cell2 = document.createElement("td");
                                cell2.innerText = display_data[k][x];
                                newRow2.appendChild(cell2);
                            }
                            dmnd = [...dmnd,String(display_data[k][3])]
                            newBody2.appendChild(newRow2);
                        }
                        for(var x in display_data[k]){
                            let cell = document.createElement("td");
                            cell.innerText = display_data[k][x];
                            newRow.appendChild(cell);
                            }
                        newBody.appendChild(newRow);
                        }
                    }


                    document.getElementById("submit").onclick = function () {
                        var requestOptions = {
                            method: 'POST',
                            redirect: 'follow'
                            };
                        fetch(baseUrl+"tableUpdate/?number="+document.getElementById("number").value+"&dmnd="+document.getElementById("dmnd").value+"&reli="+document.getElementById("reli").value, requestOptions)
                        .then(response => response.json())
                        .then(result => {
                            console.log(result),
                            alert("Your request to add "+document.getElementById('number').value+" people in relief point "+document.getElementById('reli').value+" from demand node "+document.getElementById('dmnd').value+" has been sucessfully processed.\\nServer response: "+ result["msg"]);
                            })
                        .catch(error => console.log('error', error));
                    };
                    const myloc = {
                        lat: 27.302524795918504,
                        lng: 88.59751338243387
                        };
                    var Locations = [
                        ['1', 'Demand', 27.302524795918504, 88.59751338243387, '&dmnd=1'],
                        ['2', 'Demand', 27.309941653731695, 88.59884377512124, '&dmnd=2'],
                        ['3', 'Demand', 27.30582333235349, 88.58828660114838, '&dmnd=3'],
                        ['4', 'Demand', 27.310361103820796, 88.60686894416531, '&dmnd=4'],
                        ['5', 'Demand', 27.293448382503307, 88.5876643286917, '&dmnd=5'],
                        ['6', 'Demand', 27.30007442244496, 88.60322313404959, '&dmnd=6'],
                        ['7', 'Demand', 27.290731480800943, 88.59953239709199, '&dmnd=7'],
                        ['8', 'Demand',27.29443927704333, 88.60976569341749, '&dmnd=8'],
                        ['1', 'Relief', 27.29908312298845, 88.59850259606205, '&reli=1'],
                        ['2', 'Relief', 27.316052526734996, 88.60438310868761, '&reli=2'],
                        ['3', 'Relief', 27.31059938203764, 88.58867470419628, '&reli=3'],
                        ['4', 'Relief', 27.308425729881044, 88.60326660562897, '&reli=4'],
                        ['5', 'Relief', 27.296108563399272, 88.59755852842592, '&reli=5'],
                        ['6', 'Relief', 27.29565087437993, 88.60086281523137, '&reli=6'],
                        ['7', 'Relief', 27.291570492233568, 88.59506962480899, '&reli=7'],
                        ['8', 'Relief', 27.288786566493226, 88.59927488945574, '&reli=8'],
                        ];

                        const map = new google.maps.Map(document.getElementById('map'), {
                            zoom: 14,
                            center: myloc,
                        });

                        var infowindow = new google.maps.InfoWindow();

                        var marker, i;
                        var DemandIcon = {
                            path: google.maps.SymbolPath.CIRCLE,
                            fillOpacity: 1,
                            fillColor: '#ffffff',
                            strokeOpacity: 1,
                            strokeWeight: 1,
                            strokeColor: '#333',
                            scale: 12
                        };
                        var ReliefIcon = {
                            path: google.maps.SymbolPath.CIRCLE,
                            fillOpacity: 1,
                            fillColor: '#000000',
                            strokeOpacity: 1,
                            strokeWeight: 1,
                            strokeColor: '#333',
                            scale: 12
                        };

                        function setMarkers(){
                        for (i = 0; i < Locations.length; i++) {
                            if (Locations[i][1] == "Demand" && dmnd.includes(Locations[i][0])){
                                marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(Locations[i][2], Locations[i][3]),
                                    map: map,
                                    icon: ReliefIcon,
                                    url:baseUrl+"handler/?reli="+reli+Locations[i][4],
                                    label: {color: '#ffffff', fontSize: '12px', fontWeight: '600',
                                    text: Locations[i][0]}
                                });
                                google.maps.event.addListener(marker, 'click', function() {
                                    window.location.href = this.url;
                                    window.open(marker.url, '_blank');
                            });
                            }
                            else if (Locations[i][1] == "Relief" && reli.includes(Locations[i][0])){
                                marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(Locations[i][2], Locations[i][3]),
                                    map: map,
                                    icon: DemandIcon,
                                    label: {color: '#000000', fontSize: '12px', fontWeight: '600',
                                    text: Locations[i][0]}
                            });
                            }
                        }
                        }
            </script>
 </body>
</html>
"""

handler_html_content = """
<!DOCTYPE html>
<html>  
<head>
    <meta charset="UTF-8">
    <title>Find My Route</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
    <!--meta http-equiv="refresh" content="5"-->
</head>
<style>
    html {
height: 100%
}
.main {
    padding: 10px;
    font-size: 20px;
    /* Increased text to enable scrolling */
    padding: 0px 10px;
    min-height: 100%;
}

body {
    height: 97%;
    min-height: 97%;
    font-family: 'Roboto', sans-serif;
    background: #d9eeff;
    overflow: hidden;
}

.controls {
    width: 20%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 25px;
}

.controls:focus {
    border: 4px solid #555;
}

#submit{
    background-color: skyblue;
}

.top_banner {
    text-align: center;
}

#main-data-table{
  margin-left: auto;
  margin-right: auto;
}

.flex-container {
    min-height: 80%;
    display: flex;
    border-radius: 25px;
    text-align: center;
    justify-content: center;
}

.flex-child {
    flex: 1;
    align-self: center;
    border-radius: 25px;
    margin-right: 10px;
}
.flex-container-second {
    min-height: 80%;
    display: flex;
    border-radius: 25px;
    text-align: center;
    justify-content: center;
    flex-direction: column;
}
.flex-first-child-main {
    flex: 1;
    align-self: center;
    border-radius: 25px;
    margin-right: 10px;
    overflow: auto;
    height: 200px;
}
.flex-first-child-main thead th { position: sticky; top: 0; z-index: 1; }

.flex-first-child-second {
    flex: auto;
    align-self: center;
    border-radius: 25px;
    margin-right: 10px;
    overflow: auto;
    height: 200px;
}
.flex-first-child-second thead th { position: sticky; top: 0; z-index: 1; }

table  { border-collapse: collapse; width: 100%; }
th, td { padding: 2px 30px; }
th     { background:#eee; }

.second_child{
    border-radius: 25px;
    width: 200px;
    flex: auto;
    height: 500px;
}
#map {
    align-self: centre;
    border-radius: 25px;
    height: 500px;
    width: 100%;
    flex: auto;
  flex-basis: 0;
  flex-grow: 4;

}
#container {
  height: 100%;
  display: flex;
}

#sidebar {
  flex-basis: 15rem;
  flex-grow: 1;
  padding: 1rem;
  max-width: 30rem;
  height: 100%;
  box-sizing: border-box;
  overflow: auto;
}

.second_col_table{
    align-self: center;
    border-radius: 25px;
    margin-right: 20px;
}
.second_col_legend{
    align-self: center;
    border-radius: 25px;
    width: 100%;
    margin-right: 20px;
}
</style>
<body>
             <div class="top_banner">
               <a href="/" style="color: black; text-decoration: none;"><h1>Dashboard</h1></a>
             </div>
             <div>
                <input id="dmnd" class="controls" type="number" placeholder="Demand node number" />
                <input id="reli" class="controls" type="number" placeholder="Relief point number" />
                <input id="number" class="controls" type="number" placeholder="Enter number of people" />
                <button id="submit" type="submit" class="controls" onclick="submitFunction()">Submit</button>
             </div>
             <div class="flex-container">
                <div class="flex-child">
                <div class="flex-container-second">
                <div class="flex-first-child-main">
                <h3>Main table</h3>
                    <table id = "main-data-table">
                        <thead>
                        <tr>
                          <th>Reliability<br>Value</th>
                          <th>Population<br>Served</th>
                          <th>Population<br>Unserved</th>
                          <th>Demand<br>Nodes</th>
                          <th>Relief<br>Points</th>
                        </tr>
                        </thead>
                      </table>
                      <br>
                </div>
                <div class="flex-first-child-second">
                <h3>Extra table</h3>
                    <table id = "second-data-table">
                    <thead>
                        <tr>
                          <th>Reliability<br>Value</th>
                          <th>Population<br>Served</th>
                          <th>Population<br>Unserved</th>
                          <th>Demand<br>Nodes</th>
                          <th>Relief<br>Points</th>
                        </tr>
                    </thead>
                      </table>
                </div>
                      <p>
                      Note: Negative values in column 'Population Unserved' shows that there is space to accomodate that much number of people
                      </p>
                </div>            
                </div>
                <div class="second_child">
                <div id="container">
                    <div id="map">
                    </div>
                    <div id="sidebar">
                    </div>
                    <script
                         src="https://maps.googleapis.com/maps/api/js?key=KEY&callback=initDirMap&v=weekly" type="text/javascript">
                    </script>
                    </div>
                    <div class = "second_col_legend"><table>
<tr>
<td><canvas id="myCanvas">
</canvas></td>
<td><canvas id="myCanvas2">
</canvas></td>
<td><canvas id="myCanvas3">
</canvas></td>
</tr>
<tr>
<td style="text-align:center; vertical-align:top;"><h4>Relief Point</h4></td>
<td style="text-align:center; vertical-align:top;"><h4>Demand Point</h4></td>
<td style="text-align:center; vertical-align:top;"><h4>Reliability Gradient<br>Red:low            Green:high</h4></td>
</tr>
</table>

<script>
//ctx.arc(x,y,radius,startAngle,endAngle, anticlockwise);  
var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
ctx.canvas.width = "100"
ctx.canvas.height = "50"
ctx.beginPath()
ctx.arc(c.width/2, c.height/2, c.width/4, 0, Math.PI*2, false); // outer (filled)
ctx.arc(c.width/2, c.height/2, c.width/5, 0, Math.PI*2, true); // inner (unfills it)
ctx.fill();
ctx.font = "20px Arial";
ctx.fillText("N", c.width/2.35, c.height/1.55);
var c2 = document.getElementById("myCanvas2");
var ctx2 = c2.getContext("2d");
ctx2.canvas.width = "100"
ctx2.canvas.height = "50"
ctx2.beginPath()
ctx2.arc(c2.width/2, c2.height/2, c2.width/4, 0, Math.PI*2, false); // inner (unfills it)
ctx2.fill();
ctx2.font = "20px Arial";
ctx2.fillStyle = "white";
ctx2.fillText("N", c2.width/2.35, c2.height/1.55);
var c3 = document.getElementById("myCanvas3");
var ctx3 = c3.getContext("2d");
ctx3.canvas.width = "100"
ctx3.canvas.height = "50"
var grd = ctx3.createLinearGradient(0,0,c.width,0);
grd.addColorStop(0,"red");
grd.addColorStop(0.5,"yellow");
grd.addColorStop(1,"green");
// Fill with gradient
ctx3.fillStyle = grd;
ctx3.fillRect(c.width/10,c.width/10,c.width/1.2,c.width/3);</script> 

</script> 

                    </div>
                </div>
                </div>
                <script type="text/javascript">
                var myHeaders = new Headers();
                myHeaders.append('pragma', 'no-cache');
                myHeaders.append('cache-control', 'no-cache');

                var myInit = {
                method: 'GET',
                headers: myHeaders,
                };

                const params = new URLSearchParams(window.location.search)
                for (const param of params) {
                window[param[0]] = [param[1]]
                }

                document.getElementById('dmnd').value = dmnd;
                document.getElementById('reli').value = reli;
    
                var baseUrl = window.location.protocol+"//"+window.location.hostname+":"+window.location.port+"/"
                fetch("../Data/display_data", myInit)
                .then(function (response) {
                    return response.json();
                }).then(function (apiJsonData) {
                   renderDataInTheTable(apiJsonData);
                   setMarkers();
                   initDirMap();
                })
                var reliability;
                function renderDataInTheTable(display_data) {
                    const mytable = document.getElementById("main-data-table");
                    const mytable2 = document.getElementById("second-data-table");
                    let newBody = document.createElement("tbody");
                    let newBody2 = document.createElement("tbody");
                    mytable.appendChild(newBody)
                    mytable2.appendChild(newBody2)
                    for(var k in display_data) {
                        let newRow = document.createElement("tr");
                        let newRow2 = document.createElement("tr");
                        if (display_data[k][4] == reli && display_data[k][3] == dmnd){
                            reliability = display_data[k][0]
                            for(var x in display_data[k]){
                                let cell2 = document.createElement("td");
                                cell2.innerText = display_data[k][x];
                                newRow2.appendChild(cell2);
                            }
                            newBody2.appendChild(newRow2);
                        }
                        for(var x in display_data[k]){
                            let cell = document.createElement("td");
                            cell.innerText = display_data[k][x];
                            newRow.appendChild(cell);
                            }
                        newBody.appendChild(newRow);
                        }
                    }
                    
                    document.getElementById("submit").onclick = function () {
                        var requestOptions = {
                            method: 'POST',
                            redirect: 'follow'
                            };
                        fetch(baseUrl+"tableUpdate/?number="+document.getElementById("number").value+"&dmnd="+document.getElementById("dmnd").value+"&reli="+document.getElementById("reli").value, requestOptions)
                        .then(response => response.json())
                        .then(result => {
                            console.log(result),
                            alert("Your request to add "+document.getElementById('number').value+" people in relief point "+document.getElementById('reli').value+" from demand node "+document.getElementById('dmnd').value+" has been sucessfully processed.\\nServer response: "+ result["msg"]);
                            })
                        .catch(error => console.log('error', error));
                    };

                    const myloc = {
                        lat: 27.302524795918504,
                        lng: 88.59751338243387
                        };
                    var Locations = [
                        ['1', 'Demand', 27.302524795918504, 88.59751338243387, '&dmnd=1'],
                        ['2', 'Demand', 27.309941653731695, 88.59884377512124, '&dmnd=2'],
                        ['3', 'Demand', 27.30582333235349, 88.58828660114838, '&dmnd=3'],
                        ['4', 'Demand', 27.310361103820796, 88.60686894416531, '&dmnd=4'],
                        ['5', 'Demand', 27.293448382503307, 88.5876643286917, '&dmnd=5'],
                        ['6', 'Demand', 27.30007442244496, 88.60322313404959, '&dmnd=6'],
                        ['7', 'Demand', 27.290731480800943, 88.59953239709199, '&dmnd=7'],
                        ['8', 'Demand', 27.29443927704333, 88.60976569341749, '&dmnd=8'],
                        ['1', 'Relief', 27.29908312298845, 88.59850259606205, '&reli=1'],
                        ['2', 'Relief', 27.316052526734996, 88.60438310868761, '&reli=2'],
                        ['3', 'Relief', 27.31059938203764, 88.58867470419628, '&reli=3'],
                        ['4', 'Relief', 27.308425729881044, 88.60326660562897, '&reli=4'],
                        ['5', 'Relief', 27.296108563399272, 88.59755852842592, '&reli=5'],
                        ['6', 'Relief', 27.29565087437993, 88.60086281523137, '&reli=6'],
                        ['7', 'Relief', 27.291570492233568, 88.59506962480899, '&reli=7'],
                        ['8', 'Relief', 27.288786566493226, 88.59927488945574, '&reli=8'],
                        ];

                        const map = new google.maps.Map(document.getElementById('map'), {
                            zoom: 14,
                            center: myloc,
                        });

                        var infowindow = new google.maps.InfoWindow();

                        var marker, i;
                        var DemandIcon = {
                            path: google.maps.SymbolPath.CIRCLE,
                            fillOpacity: 1,
                            fillColor: '#ffffff',
                            strokeOpacity: 1,
                            strokeWeight: 1,
                            strokeColor: '#333',
                            scale: 12
                        };
                        var ReliefIcon = {
                            path: google.maps.SymbolPath.CIRCLE,
                            fillOpacity: 1,
                            fillColor: '#000000',
                            strokeOpacity: 1,
                            strokeWeight: 1,
                            strokeColor: '#333',
                            scale: 12
                        };

                        function setMarkers(){
                        for (i = 0; i < Locations.length; i++) {
                            if (Locations[i][1] == "Demand" && dmnd.includes(Locations[i][0])){
                                marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(Locations[i][2], Locations[i][3]),
                                    map: map,
                                    icon: ReliefIcon,
                                    label: {color: '#ffffff', fontSize: '12px', fontWeight: '600',
                                    text: Locations[i][0]}
                                });
                            }
                            else if (Locations[i][1] == "Relief" && reli.includes(Locations[i][0])){
                                marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(Locations[i][2], Locations[i][3]),
                                    map: map,
                                    icon: DemandIcon,
                                    label: {color: '#000000', fontSize: '12px', fontWeight: '600',
                                    text: Locations[i][0]}
                            });
                            }
                        }
                        }
                        function initDirMap() {
                            var red, green, blue;
                            if ( reliability < 0.25 )
                            {
                                green = Math.round((reliability * 4 * 255));
                                red = 255;
                            }
                            else
                            {
                                green = 255;
                                red = Math.round(((2 - 4 * reliability) * 255));
                            }
                            const rgbToHex = (r, g, b) => '#' + [r, g, b].map(x => {
                            const hex = x.toString(16)
                            return hex.length === 1 ? '0' + hex : hex
                            }).join('')

                            for (i = 0; i < Locations.length; i++) {
                                if (Locations[i][1] == "Demand" && dmnd.includes(Locations[i][0])){
                                    origin_lat = Locations[i][2];
                                    origin_lng = Locations[i][3];
                                }
                                else if (Locations[i][1] == "Relief" && reli.includes(Locations[i][0])){
                                    dest_lat = Locations[i][2];
                                    dest_lng = Locations[i][3];
                                }
                                }
                            const directionsRenderer = new google.maps.DirectionsRenderer({suppressMarkers: true, polylineOptions: { strokeColor: rgbToHex(red,green,0) }});
                            const directionsService = new google.maps.DirectionsService();
                            directionsRenderer.setMap(map);
                            directionsRenderer.setPanel(document.getElementById("sidebar"));
                            directionsService
                                .route({
                                origin: {
                                    lat : origin_lat,
                                    lng : origin_lng,
                                },
                                destination:{
                                    lat: dest_lat,
                                    lng: dest_lng,
                                },
                                travelMode: google.maps.TravelMode.DRIVING,
                                })
                                .then((response) => {
                                directionsRenderer.setDirections(response);
                                })
                                .catch((e) => window.alert("Directions request failed due to " + status));
                            }
            </script>
 </body>
</html>
"""


app = FastAPI()

app.mount("/Data", StaticFiles(directory="Data"), name="Data")

class entry(BaseModel):
    number: int
    key: str

@app.get("/")
def create_table():
    return HTMLResponse(content = main_html_content, status_code = 200)

@app.get("/init/")
async def init_table():
    df = pd.read_csv("Data/data.csv", encoding= "unicode_escape")

    # Selecting by decision
    decision =  df['Decision variable'].values[0:64].astype('float')
    selected = list()
    for idx, item in enumerate(decision):
        if (item >= 0.1):
            selected.append(idx)

    # Output DataFrame with selected coulumns
    display_df = df.loc[selected, ['Paths' , 'Connectivity Reliability of paths (P)', \
        'Number of trips (Population)', 'Reserve capacity (PCU)']]
    display_df['Unserved population'] = display_df['Number of trips (Population)'] - \
        display_df['Reserve capacity (PCU)']
    display_df['Demand Nodes'] = display_df['Paths'].astype(str).str[1].astype(int)
    display_df['Relief Points'] = display_df['Paths'].astype(str).str[3].astype(int)
    display_df.drop(['Paths', 'Reserve capacity (PCU)'], axis=1, inplace=True)
    display_df.reset_index(inplace = True, drop = True)
    # Creating JSON for Frontend
    # JSON "index": [Reliability value, Population served, Population unserved, 
    #                 Demand node, Relief point]
    display_df.index += 1
    with open('Data/display_data', 'w') as fp:
        json.dump(display_df.T.to_dict('list'), fp, sort_keys=True, indent=4)

    return HTMLResponse(content = main_html_content, status_code = 200)

@app.get("/setdemand/")
async def create_demand_node(dmnd: int):
    return HTMLResponse(content = demand_html_content, status_code = 200)

@app.get("/setrelief/")
async def create_relief_node(reli: int):    
    return HTMLResponse(content = relief_html_content, status_code = 200)

@app.get("/handler/")
async def show_map(dmnd:int, reli: int):    
    return HTMLResponse(content = handler_html_content, status_code = 200)

@app.post("/tableUpdate/")
def update_table(number: int, dmnd: int, reli: int):
    # JSON "index": [Reliability value, Population served, Population unserved, 
    #                 Demand node, Relief point]
    with open('Data/display_data', 'r') as fp:
        display_data = json.load(fp)
        print("load sucessful")
        print(display_data)
    # Get Key and Number of People from request
    # Check if Population unserved is negative, ie there is room for more population to serve
    msg = ''
    for row in display_data:
        if (display_data[row][3] == dmnd and display_data[row][4] == reli):
            if (display_data[row][2] > 0):
                msg += "Relief point full. "
                return JSONResponse({'msg': msg, 'status_code' : 400})
            if (display_data[row][2] + number) <= 0:
                display_data[row][2] += number
                msg += "Update successful for %d people. "%(number)
                with open('Data/display_data', 'w') as fp:
                    json.dump(display_data, fp, sort_keys=True, indent=4)
        # Alert added to warn population limit after changes
                if (display_data[row][2] > -1):
                    msg += "Cannot add anymore people. "
        # Saving JSON at end of task
            else:
                msg += "Entered population value %d exceeds the population limit of the relief point. "%(number)
                return JSONResponse({'msg': msg, 'status_code' : 400})
    return JSONResponse({'msg': msg, 'status_code' : 200})

@app.post("/testpost/")
def testPost():
    return JSONResponse({'msg': "test successfull", 'status_code' : 400})