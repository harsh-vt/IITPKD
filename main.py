import json
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

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
    overflow: auto;
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

.Header_Table {
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
.header_row {
  display: flex;
  align-items: center;
}
.header_col_logo {
  width: 20%;
  text-align:right;
  padding: 5px;
}
.header_col_text {
  flex: 50%;
  padding: 10px;
}
</style>
<body>
            <div class="Header_Table">
                <div class = "header_row">
                    <div class = "header_col_logo">
                        <a href="/" style="color: black; text-decoration: none;">
                        <img src="../Data/Images/logo_transparent.png" alt="logo_transparent" style="width:90px;height:70px;">
                    </div>
                    <div class = "header_col_text">
                        <h1>A scenario analysis tool for population evacuation during disasters</h1>
                        <h2>Supported by : National Mission on Himalayan Studies</h2>
                    </div>
                </a>
            </div>
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
                </script>

             <div class="flex-container">
                <div class="flex-child">
                    <table id = "main-data-table">
                        <tr>
                          <th>Population Centroid</th>
                          <th>Relief Point</th>
                          <th>Reserve Capacity</th>
                          <th>Allocated Evacuation Trips</th>
                          <th>Connectivity Reliability</th>
                        </tr>
                      </table>
                </div>
                <div class="second_child">
                    <div id="map">
                    </div>
                    <script
                         src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAEX5N6BW6mUGgnor0EBcYwf52twggIs8k" type="text/javascript">
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
                        lat: 27.338421745066793,
                        lng: 88.6146979508191
                        };
                    var Locations = [
                        ['1', 'Demand', 27.3297,88.6046,'setdemand/?dmnd=1'],
                        ['2', 'Demand', 27.3211,88.5994,'setdemand/?dmnd=2'],
                        ['3', 'Demand', 27.33,88.6097,'setdemand/?dmnd=3'],
                        ['4', 'Demand', 27.3127,88.5933,'setdemand/?dmnd=4'],
                        ['5', 'Demand', 27.3255,88.6124,'setdemand/?dmnd=5'],
                        ['6', 'Demand', 27.3444,88.6268,'setdemand/?dmnd=6'],
                        ['7', 'Demand', 27.3572,88.6134,'setdemand/?dmnd=7'],
                        ['8', 'Demand', 27.3413,88.6136,'setdemand/?dmnd=8'],
                        ['9', 'Demand', 27.3428,88.6027,'setdemand/?dmnd=9'],
                        ['10', 'Demand', 27.3337,88.6132,'setdemand/?dmnd=10'],
                        ['11', 'Demand', 27.3579,88.6183,'setdemand/?dmnd=11'],
                        ['12', 'Demand', 27.3411,88.6088,'setdemand/?dmnd=12'],
                        ['13', 'Demand', 27.3293,88.6144,'setdemand/?dmnd=13'],
                        ['14', 'Demand', 27.3137,88.6065,'setdemand/?dmnd=14'],
                        ['15', 'Demand', 27.3238,88.6109,'setdemand/?dmnd=15'],
                        ['16', 'Demand', 27.3203,88.6068,'setdemand/?dmnd=16'],
                        ['17', 'Demand', 27.3007,88.5922,'setdemand/?dmnd=17'],
                        ['1', 'Relief', 27.3082,88.5829, 'setrelief/?reli=1'],
                        ['2', 'Relief', 27.3635,88.606, 'setrelief/?reli=2'],
                        ['3', 'Relief', 27.2879,88.5949, 'setrelief/?reli=3'],
                        ['4', 'Relief', 27.2818,88.5918, 'setrelief/?reli=4'],
                        ['5', 'Relief', 27.3692,88.6122, 'setrelief/?reli=5'],
                        ['6', 'Relief', 27.284,88.6028, 'setrelief/?reli=6'],
                        ['7', 'Relief', 27.2677,88.6014, 'setrelief/?reli=7'],
                        ['8', 'Relief', 27.2681,88.6148, 'setrelief/?reli=8'],
                        ['9', 'Relief', 27.261,88.5924, 'setrelief/?reli=9'],
                        ['10', 'Relief', 27.2682,88.6099, 'setrelief/?reli=10'],
                        ['11', 'Relief', 27.2422,88.596, 'setrelief/?reli=11'],
                        ['12', 'Relief', 27.2891,88.5924, 'setrelief/?reli=12'],
                        ['13', 'Relief', 27.3016,88.5822, 'setrelief/?reli=13'],
                        ['14', 'Relief', 27.311,88.5846, 'setrelief/?reli=14'],
                        ['15', 'Relief', 27.299,88.5982, 'setrelief/?reli=15'],
                        ['16', 'Relief', 27.3028,88.6038, 'setrelief/?reli=16'],
                        ['17', 'Relief', 27.3446,88.5947, 'setrelief/?reli=17'],
                        ['18', 'Relief', 27.3263,88.6108, 'setrelief/?reli=18'],
                        ['19', 'Relief', 27.3414,88.6213, 'setrelief/?reli=19'],
                        ['20', 'Relief', 27.3389,88.6065, 'setrelief/?reli=20'],
                        ['21', 'Relief', 27.3389,88.6064, 'setrelief/?reli=21'],
                        ['22', 'Relief', 27.3387,88.6238, 'setrelief/?reli=22'],
                        ['23', 'Relief', 27.3298,88.6141, 'setrelief/?reli=23'],
                        ['24', 'Relief', 27.3387,88.6238, 'setrelief/?reli=24'],
                        ['25', 'Relief', 27.3656,88.6119, 'setrelief/?reli=25'],
                        ['26', 'Relief', 27.3261,88.6146, 'setrelief/?reli=26'],
                        ['27', 'Relief', 27.3129,88.6048, 'setrelief/?reli=27'],
                        ['28', 'Relief', 27.3379,88.6236, 'setrelief/?reli=28'],
                        ['29', 'Relief', 27.3362,88.6119, 'setrelief/?reli=29'],
                        ['30', 'Relief', 27.3303,88.6144, 'setrelief/?reli=30'],
                        ['31', 'Relief', 27.3414,88.6071, 'setrelief/?reli=31'],
                        ['32', 'Relief', 27.3426,88.6093, 'setrelief/?reli=32'],
                        ['33', 'Relief', 27.3383,88.6224, 'setrelief/?reli=33'],
                        ['34', 'Relief', 27.329,88.6123, 'setrelief/?reli=34'],
                        ['35', 'Relief', 27.3426,88.6091, 'setrelief/?reli=35'],
                        ['36', 'Relief', 27.3421,88.6055, 'setrelief/?reli=36'],
                        ['37', 'Relief', 27.3395,88.6096, 'setrelief/?reli=37'],
                        ['38', 'Relief', 27.337,88.6129, 'setrelief/?reli=38'],
                        ['39', 'Relief', 27.3294,88.6113, 'setrelief/?reli=39'],
                        ['40', 'Relief', 27.3294,88.6113, 'setrelief/?reli=40'],
                        ['41', 'Relief', 27.3331,88.6148, 'setrelief/?reli=41'],
                        ['42', 'Relief', 27.3343,88.6139, 'setrelief/?reli=42'],
                        ['43', 'Relief', 27.3268,88.6108, 'setrelief/?reli=43'],
                        ['44', 'Relief', 27.3352,88.6135, 'setrelief/?reli=44'],
                        ];

                        var final = [
                            ['1', '44'],
                            ['3', '40'],
                            ['5', '34'],
                            ['6', '19'],
                            ['6', '24'],
                            ['6', '28'],
                            ['6', '33'],
                            ['8', '37'],
                            ['10', '41'],
                            ['10', '44'],
                            ['10', '38'],
                            ['10', '29'],
                            ['11', '25'],
                            ['12', '31'],
                            ['12', '36'],
                            ['12', '20'],
                            ['12', '21'],
                            ['12', '35'],
                            ['12', '32'],
                            ['13', '26'],
                            ['13', '23'],
                            ['13', '30'],
                            ['14', '27'],
                            ['15', '18'],
                            ['15', '43'],
                        ];

                        const map = new google.maps.Map(document.getElementById('map'), {
                            zoom: 13,
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
    overflow: auto;
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

.Header_Table {
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
.header_row {
  display: flex;
  align-items: center;
}
.header_col_logo {
  width: 20%;
  text-align:right;
  padding: 5px;
}
.header_col_text {
  flex: 50%;
  padding: 10px;
}
</style>
<body>
            <div class="Header_Table">
                <div class = "header_row">
                    <div class = "header_col_logo">
                        <a href="/" style="color: black; text-decoration: none;">
                        <img src="../Data/Images/logo_transparent.png" alt="logo_transparent" style="width:90px;height:70px;">
                    </div>
                    <div class = "header_col_text">
                        <h1>A scenario analysis tool for population evacuation during disasters</h1>
                        <h2>Supported by : National Mission on Himalayan Studies</h2>
                    </div>
                </a>
            </div>
             <div class="flex-container">
                <div class="flex-child">
                <div class="flex-container-second">
                <div class="flex-first-child-main">
                <h3>Main table</h3>
                    <table id = "main-data-table">
                        <thead>
                        <tr>
                          <th>Population Centroid</th>
                          <th>Relief Point</th>
                          <th>Reserved Capacity</th>
                          <th>Allocated Evacuation Trips</th>
                          <th>Connectivity Reliability</th>
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
                          <th>Population Centroid</th>
                          <th>Relief Point</th>
                          <th>Reserved Capacity</th>
                          <th>Allocated Evacuation Trips</th>
                          <th>Connectivity Reliability</th>
                        </tr>
                    </thead>
                      </table>
                </div>
                </div>                      
                </div>
                <div class="second_child">
                    <div id="map">
                    </div>
                    <script
                         src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAEX5N6BW6mUGgnor0EBcYwf52twggIs8k" type="text/javascript">
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
                        if (display_data[k][0] == dmnd){
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
                    const myloc = {
                        lat: 27.338421745066793,
                        lng: 88.6146979508191
                        };
                    var Locations = [
                        ['1', 'Demand', 27.3297,88.6046,'&dmnd=1'],
                        ['2', 'Demand', 27.3211,88.5994,'&dmnd=2'],
                        ['3', 'Demand', 27.33,88.6097,'&dmnd=3'],
                        ['4', 'Demand', 27.3127,88.5933,'&dmnd=4'],
                        ['5', 'Demand', 27.3255,88.6124,'&dmnd=5'],
                        ['6', 'Demand', 27.3444,88.6268,'&dmnd=6'],
                        ['7', 'Demand', 27.3572,88.6134,'&dmnd=7'],
                        ['8', 'Demand', 27.3413,88.6136,'&dmnd=8'],
                        ['9', 'Demand', 27.3428,88.6027,'&dmnd=9'],
                        ['10', 'Demand', 27.3337,88.6132,'&dmnd=10'],
                        ['11', 'Demand', 27.3579,88.6183,'&dmnd=11'],
                        ['12', 'Demand', 27.3411,88.6088,'&dmnd=12'],
                        ['13', 'Demand', 27.3293,88.6144,'&dmnd=13'],
                        ['14', 'Demand', 27.3137,88.6065,'&dmnd=14'],
                        ['15', 'Demand', 27.3238,88.6109,'&dmnd=15'],
                        ['16', 'Demand', 27.3203,88.6068,'&dmnd=16'],
                        ['17', 'Demand', 27.3007,88.5922,'&dmnd=17'],
                        ['1', 'Relief', 27.3082,88.5829, '&reli=1'],
                        ['2', 'Relief', 27.3635,88.606, '&reli=2'],
                        ['3', 'Relief', 27.2879,88.5949, '&reli=3'],
                        ['4', 'Relief', 27.2818,88.5918, '&reli=4'],
                        ['5', 'Relief', 27.3692,88.6122, '&reli=5'],
                        ['6', 'Relief', 27.284,88.6028, '&reli=6'],
                        ['7', 'Relief', 27.2677,88.6014, '&reli=7'],
                        ['8', 'Relief', 27.2681,88.6148, '&reli=8'],
                        ['9', 'Relief', 27.261,88.5924, '&reli=9'],
                        ['10', 'Relief', 27.2682,88.6099, '&reli=10'],
                        ['11', 'Relief', 27.2422,88.596, '&reli=11'],
                        ['12', 'Relief', 27.2891,88.5924, '&reli=12'],
                        ['13', 'Relief', 27.3016,88.5822, '&reli=13'],
                        ['14', 'Relief', 27.311,88.5846, '&reli=14'],
                        ['15', 'Relief', 27.299,88.5982, '&reli=15'],
                        ['16', 'Relief', 27.3028,88.6038, '&reli=16'],
                        ['17', 'Relief', 27.3446,88.5947, '&reli=17'],
                        ['18', 'Relief', 27.3263,88.6108, '&reli=18'],
                        ['19', 'Relief', 27.3414,88.6213, '&reli=19'],
                        ['20', 'Relief', 27.3389,88.6065, '&reli=20'],
                        ['21', 'Relief', 27.3389,88.6064, '&reli=21'],
                        ['22', 'Relief', 27.3387,88.6238, '&reli=22'],
                        ['23', 'Relief', 27.3298,88.6141, '&reli=23'],
                        ['24', 'Relief', 27.3387,88.6238, '&reli=24'],
                        ['25', 'Relief', 27.3656,88.6119, '&reli=25'],
                        ['26', 'Relief', 27.3261,88.6146, '&reli=26'],
                        ['27', 'Relief', 27.3129,88.6048, '&reli=27'],
                        ['28', 'Relief', 27.3379,88.6236, '&reli=28'],
                        ['29', 'Relief', 27.3362,88.6119, '&reli=29'],
                        ['30', 'Relief', 27.3303,88.6144, '&reli=30'],
                        ['31', 'Relief', 27.3414,88.6071, '&reli=31'],
                        ['32', 'Relief', 27.3426,88.6093, '&reli=32'],
                        ['33', 'Relief', 27.3383,88.6224, '&reli=33'],
                        ['34', 'Relief', 27.329,88.6123, '&reli=34'],
                        ['35', 'Relief', 27.3426,88.6091, '&reli=35'],
                        ['36', 'Relief', 27.3421,88.6055, '&reli=36'],
                        ['37', 'Relief', 27.3395,88.6096, '&reli=37'],
                        ['38', 'Relief', 27.337,88.6129, '&reli=38'],
                        ['39', 'Relief', 27.3294,88.6113, '&reli=39'],
                        ['40', 'Relief', 27.3294,88.6113, '&reli=40'],
                        ['41', 'Relief', 27.3331,88.6148, '&reli=41'],
                        ['42', 'Relief', 27.3343,88.6139, '&reli=42'],
                        ['43', 'Relief', 27.3268,88.6108, '&reli=43'],
                        ['44', 'Relief', 27.3352,88.6135, '&reli=44'],
                        ];
                        var final = [
                            ['1', '44'],
                            ['3', '40'],
                            ['5', '34'],
                            ['6', '19'],
                            ['6', '24'],
                            ['6', '28'],
                            ['6', '33'],
                            ['8', '37'],
                            ['10', '41'],
                            ['10', '44'],
                            ['10', '38'],
                            ['10', '29'],
                            ['11', '25'],
                            ['12', '31'],
                            ['12', '36'],
                            ['12', '20'],
                            ['12', '21'],
                            ['12', '35'],
                            ['12', '32'],
                            ['13', '26'],
                            ['13', '23'],
                            ['13', '30'],
                            ['14', '27'],
                            ['15', '18'],
                            ['15', '43'],
                        ];


                        const map = new google.maps.Map(document.getElementById('map'), {
                            zoom: 13,
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
                        var set_reli = [];
                        for (i = 0; i < final.length; i++){
                            if (dmnd.includes(final[i][0])){
                                set_reli.push(final[i][1]);
                            }
                        }
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
                            else if (Locations[i][1] == "Relief" && set_reli.includes(Locations[i][0])){
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
    overflow: auto;
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

.Header_Table {
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
.header_row {
  display: flex;
  align-items: center;
}
.header_col_logo {
  width: 20%;
  text-align:right;
  padding: 5px;
}
.header_col_text {
  flex: 50%;
  padding: 10px;
}
</style>
<body>
            <div class="Header_Table">
                <div class = "header_row">
                    <div class = "header_col_logo">
                        <a href="/" style="color: black; text-decoration: none;">
                        <img src="../Data/Images/logo_transparent.png" alt="logo_transparent" style="width:90px;height:70px;">
                    </div>
                    <div class = "header_col_text">
                        <h1>A scenario analysis tool for population evacuation during disasters</h1>
                        <h2>Supported by : National Mission on Himalayan Studies</h2>
                    </div>
                </a>
            </div>
             <div class="flex-container">
                <div class="flex-child">
                <div class="flex-container-second">
                <div class="flex-first-child-main">
                <h3>Main table</h3>
                    <table id = "main-data-table">
                        <thead>
                        <tr>
                          <th>Population Centroid</th>
                          <th>Relief Point</th>
                          <th>Reserved Capacity</th>
                          <th>Allocated Evacuation Trips</th>
                          <th>Connectivity Reliability</th>
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
                          <th>Population Centroid</th>
                          <th>Relief Point</th>
                          <th>Reserved Capacity</th>
                          <th>Allocated Evacuation Trips</th>
                          <th>Connectivity Reliability</th>
                        </tr>
                    </thead>
                      </table>
                </div>
                </div>                      
                </div>
                <div class="second_child">
                    <div id="map">
                    </div>
                    <script
                         src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAEX5N6BW6mUGgnor0EBcYwf52twggIs8k" type="text/javascript">
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
                        if (display_data[k][1] == reli){
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

                    const myloc = {
                        lat: 27.338421745066793,
                        lng: 88.6146979508191
                        };
                    var Locations = [
                        ['1', 'Demand', 27.3297,88.6046,'&dmnd=1'],
                        ['2', 'Demand', 27.3211,88.5994,'&dmnd=2'],
                        ['3', 'Demand', 27.33,88.6097,'&dmnd=3'],
                        ['4', 'Demand', 27.3127,88.5933,'&dmnd=4'],
                        ['5', 'Demand', 27.3255,88.6124,'&dmnd=5'],
                        ['6', 'Demand', 27.3444,88.6268,'&dmnd=6'],
                        ['7', 'Demand', 27.3572,88.6134,'&dmnd=7'],
                        ['8', 'Demand', 27.3413,88.6136,'&dmnd=8'],
                        ['9', 'Demand', 27.3428,88.6027,'&dmnd=9'],
                        ['10', 'Demand', 27.3337,88.6132,'&dmnd=10'],
                        ['11', 'Demand', 27.3579,88.6183,'&dmnd=11'],
                        ['12', 'Demand', 27.3411,88.6088,'&dmnd=12'],
                        ['13', 'Demand', 27.3293,88.6144,'&dmnd=13'],
                        ['14', 'Demand', 27.3137,88.6065,'&dmnd=14'],
                        ['15', 'Demand', 27.3238,88.6109,'&dmnd=15'],
                        ['16', 'Demand', 27.3203,88.6068,'&dmnd=16'],
                        ['17', 'Demand', 27.3007,88.5922,'&dmnd=17'],
                        ['1', 'Relief', 27.3082,88.5829, '&reli=1'],
                        ['2', 'Relief', 27.3635,88.606, '&reli=2'],
                        ['3', 'Relief', 27.2879,88.5949, '&reli=3'],
                        ['4', 'Relief', 27.2818,88.5918, '&reli=4'],
                        ['5', 'Relief', 27.3692,88.6122, '&reli=5'],
                        ['6', 'Relief', 27.284,88.6028, '&reli=6'],
                        ['7', 'Relief', 27.2677,88.6014, '&reli=7'],
                        ['8', 'Relief', 27.2681,88.6148, '&reli=8'],
                        ['9', 'Relief', 27.261,88.5924, '&reli=9'],
                        ['10', 'Relief', 27.2682,88.6099, '&reli=10'],
                        ['11', 'Relief', 27.2422,88.596, '&reli=11'],
                        ['12', 'Relief', 27.2891,88.5924, '&reli=12'],
                        ['13', 'Relief', 27.3016,88.5822, '&reli=13'],
                        ['14', 'Relief', 27.311,88.5846, '&reli=14'],
                        ['15', 'Relief', 27.299,88.5982, '&reli=15'],
                        ['16', 'Relief', 27.3028,88.6038, '&reli=16'],
                        ['17', 'Relief', 27.3446,88.5947, '&reli=17'],
                        ['18', 'Relief', 27.3263,88.6108, '&reli=18'],
                        ['19', 'Relief', 27.3414,88.6213, '&reli=19'],
                        ['20', 'Relief', 27.3389,88.6065, '&reli=20'],
                        ['21', 'Relief', 27.3389,88.6064, '&reli=21'],
                        ['22', 'Relief', 27.3387,88.6238, '&reli=22'],
                        ['23', 'Relief', 27.3298,88.6141, '&reli=23'],
                        ['24', 'Relief', 27.3387,88.6238, '&reli=24'],
                        ['25', 'Relief', 27.3656,88.6119, '&reli=25'],
                        ['26', 'Relief', 27.3261,88.6146, '&reli=26'],
                        ['27', 'Relief', 27.3129,88.6048, '&reli=27'],
                        ['28', 'Relief', 27.3379,88.6236, '&reli=28'],
                        ['29', 'Relief', 27.3362,88.6119, '&reli=29'],
                        ['30', 'Relief', 27.3303,88.6144, '&reli=30'],
                        ['31', 'Relief', 27.3414,88.6071, '&reli=31'],
                        ['32', 'Relief', 27.3426,88.6093, '&reli=32'],
                        ['33', 'Relief', 27.3383,88.6224, '&reli=33'],
                        ['34', 'Relief', 27.329,88.6123, '&reli=34'],
                        ['35', 'Relief', 27.3426,88.6091, '&reli=35'],
                        ['36', 'Relief', 27.3421,88.6055, '&reli=36'],
                        ['37', 'Relief', 27.3395,88.6096, '&reli=37'],
                        ['38', 'Relief', 27.337,88.6129, '&reli=38'],
                        ['39', 'Relief', 27.3294,88.6113, '&reli=39'],
                        ['40', 'Relief', 27.3294,88.6113, '&reli=40'],
                        ['41', 'Relief', 27.3331,88.6148, '&reli=41'],
                        ['42', 'Relief', 27.3343,88.6139, '&reli=42'],
                        ['43', 'Relief', 27.3268,88.6108, '&reli=43'],
                        ['44', 'Relief', 27.3352,88.6135, '&reli=44'],
                        ];
                        var final = [
                            ['1', '44'],
                            ['3', '40'],
                            ['5', '34'],
                            ['6', '19'],
                            ['6', '24'],
                            ['6', '28'],
                            ['6', '33'],
                            ['8', '37'],
                            ['10', '41'],
                            ['10', '44'],
                            ['10', '38'],
                            ['10', '29'],
                            ['11', '25'],
                            ['12', '31'],
                            ['12', '36'],
                            ['12', '20'],
                            ['12', '21'],
                            ['12', '35'],
                            ['12', '32'],
                            ['13', '26'],
                            ['13', '23'],
                            ['13', '30'],
                            ['14', '27'],
                            ['15', '18'],
                            ['15', '43'],
                        ];

                        const map = new google.maps.Map(document.getElementById('map'), {
                            zoom: 13,
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
                        var set_dmnd = [];
                        for (i = 0; i < final.length; i++){
                            if (reli.includes(final[i][1])){
                                set_dmnd.push(final[i][0]);
                            }
                        }
                        console.log(set_dmnd);
                        for (i = 0; i < Locations.length; i++) {
                            if (Locations[i][1] == "Demand" && set_dmnd.includes(Locations[i][0])){
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
    overflow: auto;
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

.Header_Table {
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
.header_row {
  display: flex;
  align-items: center;
}
.header_col_logo {
  width: 20%;
  text-align:right;
  padding: 5px;
}
.header_col_text {
  flex: 50%;
  padding: 10px;
}
</style>
<body>
            <div class="Header_Table">
                <div class = "header_row">
                    <div class = "header_col_logo">
                        <a href="/" style="color: black; text-decoration: none;">
                        <img src="../Data/Images/logo_transparent.png" alt="logo_transparent" style="width:90px;height:70px;">
                    </div>
                    <div class = "header_col_text">
                        <h1>A scenario analysis tool for population evacuation during disasters</h1>
                        <h2>Supported by : National Mission on Himalayan Studies</h2>
                    </div>
                </a>
            </div>
             <div class="flex-container">
                <div class="flex-child">
                <div class="flex-container-second">
                <div class="flex-first-child-main">
                <h3>Main table</h3>
                    <table id = "main-data-table">
                        <thead>
                        <tr>
                          <th>Population Centroid</th>
                          <th>Relief Point</th>
                          <th>Reserved Capacity</th>
                          <th>Allocated Evacuation Trips</th>
                          <th>Connectivity Reliability</th>
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
                          <th>Population Centroid</th>
                          <th>Relief Point</th>
                          <th>Reserved Capacity</th>
                          <th>Allocated Evacuation Trips</th>
                          <th>Connectivity Reliability</th>
                        </tr>
                    </thead>
                      </table>
                </div>
                </div>            
                </div>
                <div class="second_child">
                <div id="container">
                    <div id="map">
                    </div>
                    <div id="sidebar">
                    </div>
                    <script
                         src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAEX5N6BW6mUGgnor0EBcYwf52twggIs8k&callback=initDirMap&v=weekly" type="text/javascript">
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
                        if (display_data[k][1] == reli && display_data[k][0] == dmnd){
                            reliability = display_data[k][4]
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
                    const myloc = {
                        lat: 27.338421745066793,
                        lng: 88.6146979508191
                        };
                    var Locations = [
                        ['1', 'Demand', 27.3297,88.6046,'&dmnd=1'],
                        ['2', 'Demand', 27.3211,88.5994,'&dmnd=2'],
                        ['3', 'Demand', 27.33,88.6097,'&dmnd=3'],
                        ['4', 'Demand', 27.3127,88.5933,'&dmnd=4'],
                        ['5', 'Demand', 27.3255,88.6124,'&dmnd=5'],
                        ['6', 'Demand', 27.3444,88.6268,'&dmnd=6'],
                        ['7', 'Demand', 27.3572,88.6134,'&dmnd=7'],
                        ['8', 'Demand', 27.3413,88.6136,'&dmnd=8'],
                        ['9', 'Demand', 27.3428,88.6027,'&dmnd=9'],
                        ['10', 'Demand', 27.3337,88.6132,'&dmnd=10'],
                        ['11', 'Demand', 27.3579,88.6183,'&dmnd=11'],
                        ['12', 'Demand', 27.3411,88.6088,'&dmnd=12'],
                        ['13', 'Demand', 27.3293,88.6144,'&dmnd=13'],
                        ['14', 'Demand', 27.3137,88.6065,'&dmnd=14'],
                        ['15', 'Demand', 27.3238,88.6109,'&dmnd=15'],
                        ['16', 'Demand', 27.3203,88.6068,'&dmnd=16'],
                        ['17', 'Demand', 27.3007,88.5922,'&dmnd=17'],
                        ['1', 'Relief', 27.3082,88.5829, '&reli=1'],
                        ['2', 'Relief', 27.3635,88.606, '&reli=2'],
                        ['3', 'Relief', 27.2879,88.5949, '&reli=3'],
                        ['4', 'Relief', 27.2818,88.5918, '&reli=4'],
                        ['5', 'Relief', 27.3692,88.6122, '&reli=5'],
                        ['6', 'Relief', 27.284,88.6028, '&reli=6'],
                        ['7', 'Relief', 27.2677,88.6014, '&reli=7'],
                        ['8', 'Relief', 27.2681,88.6148, '&reli=8'],
                        ['9', 'Relief', 27.261,88.5924, '&reli=9'],
                        ['10', 'Relief', 27.2682,88.6099, '&reli=10'],
                        ['11', 'Relief', 27.2422,88.596, '&reli=11'],
                        ['12', 'Relief', 27.2891,88.5924, '&reli=12'],
                        ['13', 'Relief', 27.3016,88.5822, '&reli=13'],
                        ['14', 'Relief', 27.311,88.5846, '&reli=14'],
                        ['15', 'Relief', 27.299,88.5982, '&reli=15'],
                        ['16', 'Relief', 27.3028,88.6038, '&reli=16'],
                        ['17', 'Relief', 27.3446,88.5947, '&reli=17'],
                        ['18', 'Relief', 27.3263,88.6108, '&reli=18'],
                        ['19', 'Relief', 27.3414,88.6213, '&reli=19'],
                        ['20', 'Relief', 27.3389,88.6065, '&reli=20'],
                        ['21', 'Relief', 27.3389,88.6064, '&reli=21'],
                        ['22', 'Relief', 27.3387,88.6238, '&reli=22'],
                        ['23', 'Relief', 27.3298,88.6141, '&reli=23'],
                        ['24', 'Relief', 27.3387,88.6238, '&reli=24'],
                        ['25', 'Relief', 27.3656,88.6119, '&reli=25'],
                        ['26', 'Relief', 27.3261,88.6146, '&reli=26'],
                        ['27', 'Relief', 27.3129,88.6048, '&reli=27'],
                        ['28', 'Relief', 27.3379,88.6236, '&reli=28'],
                        ['29', 'Relief', 27.3362,88.6119, '&reli=29'],
                        ['30', 'Relief', 27.3303,88.6144, '&reli=30'],
                        ['31', 'Relief', 27.3414,88.6071, '&reli=31'],
                        ['32', 'Relief', 27.3426,88.6093, '&reli=32'],
                        ['33', 'Relief', 27.3383,88.6224, '&reli=33'],
                        ['34', 'Relief', 27.329,88.6123, '&reli=34'],
                        ['35', 'Relief', 27.3426,88.6091, '&reli=35'],
                        ['36', 'Relief', 27.3421,88.6055, '&reli=36'],
                        ['37', 'Relief', 27.3395,88.6096, '&reli=37'],
                        ['38', 'Relief', 27.337,88.6129, '&reli=38'],
                        ['39', 'Relief', 27.3294,88.6113, '&reli=39'],
                        ['40', 'Relief', 27.3294,88.6113, '&reli=40'],
                        ['41', 'Relief', 27.3331,88.6148, '&reli=41'],
                        ['42', 'Relief', 27.3343,88.6139, '&reli=42'],
                        ['43', 'Relief', 27.3268,88.6108, '&reli=43'],
                        ['44', 'Relief', 27.3352,88.6135, '&reli=44'],
                        ];
                        var  d1r44a  = new google.maps.LatLng( 27.3303 ,  88.6064 );
                        var  d1r44b  = new google.maps.LatLng( 27.3306 ,  88.6101 );
                        var  d1r44c  = new google.maps.LatLng( 27.331 ,  88.6112 );
                        var  d1r44d  = new google.maps.LatLng( 27.3318 ,  88.6121 );
                        var  d1r44e  = new google.maps.LatLng( 27.3342 ,  88.6139 );
                        var  d1r44f  = new google.maps.LatLng( 27.3337 ,  88.6142 );
                        var  d1r44g  = new google.maps.LatLng( 27.3351 ,  88.6136 );
                        var  d3r40a  = new google.maps.LatLng( 27.3297 ,  88.61 );
                        var  d3r40b  = new google.maps.LatLng( 27.3295 ,  88.6105 );
                        var  d3r40c  = new google.maps.LatLng( 27.3283 ,  88.6117 );
                        var  d3r40d  = new google.maps.LatLng( 27.3298 ,  88.6119 );
                        var  d5r34a  = new google.maps.LatLng( 27.3267 ,  88.6133 );
                        var  d5r34b  = new google.maps.LatLng( 27.3278 ,  88.613 );
                        var  d5r34c  = new google.maps.LatLng( 27.3287 ,  88.6133 );
                        var  d6r19a  = new google.maps.LatLng( 27.347 ,  88.629 );
                        var  d6r19b  = new google.maps.LatLng( 27.3454 ,  88.6346 );
                        var  d6r19c  = new google.maps.LatLng( 27.3413 ,  88.6252 );
                        var  d6r19d  = new google.maps.LatLng( 27.3417 ,  88.6214 );
                        var  d6r24a  = new google.maps.LatLng( 27.347 ,  88.629 );
                        var  d6r24b  = new google.maps.LatLng( 27.3454 ,  88.6346 );
                        var  d6r24c  = new google.maps.LatLng( 27.3413 ,  88.6252 );
                        var  d6r24d  = new google.maps.LatLng( 27.3367 ,  88.6271 );
                        var  d6r24e  = new google.maps.LatLng( 27.3387 ,  88.6239 );
                        var  d6r28a  = new google.maps.LatLng( 27.347 ,  88.629 );
                        var  d6r28b  = new google.maps.LatLng( 27.3454 ,  88.6346 );
                        var  d6r28c  = new google.maps.LatLng( 27.3413 ,  88.6252 );
                        var  d6r28d  = new google.maps.LatLng( 27.3367 ,  88.6271 );
                        var  d6r28e  = new google.maps.LatLng( 27.3387 ,  88.6239 );
                        var  d6r33a  = new google.maps.LatLng( 27.347 ,  88.629 );
                        var  d6r33b  = new google.maps.LatLng( 27.347 ,  88.6291 );
                        var  d6r33c  = new google.maps.LatLng( 27.3413 ,  88.6252 );
                        var  d6r33d  = new google.maps.LatLng( 27.339 ,  88.6191 );
                        var  d6r33e  = new google.maps.LatLng( 27.3356 ,  88.6203 );
                        var  d6r33f  = new google.maps.LatLng( 27.3381 ,  88.622 );
                        var  d8r37a  = new google.maps.LatLng( 27.3419 ,  88.6126 );
                        var  d8r37b  = new google.maps.LatLng( 27.3409 ,  88.6122 );
                        var  d8r37c  = new google.maps.LatLng( 27.3395 ,  88.6126 );
                        var  d8r37d  = new google.maps.LatLng( 27.3394 ,  88.6127 );
                        var  d8r37e  = new google.maps.LatLng( 27.3385 ,  88.615 );
                        var  d8r37f  = new google.maps.LatLng( 27.3382 ,  88.6151 );
                        var  d8r37g  = new google.maps.LatLng( 27.3351 ,  88.6151 );
                        var  d8r37h  = new google.maps.LatLng( 27.3355 ,  88.6145 );
                        var  d8r37i  = new google.maps.LatLng( 27.3367 ,  88.613 );
                        var  d8r37j  = new google.maps.LatLng( 27.3381 ,  88.6114 );
                        var  d8r37k  = new google.maps.LatLng( 27.3393 ,  88.61 );
                        var  d10r41a  = new google.maps.LatLng( 27.3342 ,  88.6139 );
                        var  d10r41b  = new google.maps.LatLng( 27.3337 ,  88.6142 );
                        var  d10r41c  = new google.maps.LatLng( 27.333 ,  88.6144 );
                        var  d10r44a  = new google.maps.LatLng( 27.3342 ,  88.6139 );
                        var  d10r44b  = new google.maps.LatLng( 27.3337 ,  88.6142 );
                        var  d10r44c  = new google.maps.LatLng( 27.3351 ,  88.6136 );
                        var  d10r38a  = new google.maps.LatLng( 27.3342 ,  88.6139 );
                        var  d10r38b  = new google.maps.LatLng( 27.3337 ,  88.6142 );
                        var  d10r38c  = new google.maps.LatLng( 27.333 ,  88.6144 );
                        var  d10r38d  = new google.maps.LatLng( 27.3313 ,  88.6138 );
                        var  d10r38e  = new google.maps.LatLng( 27.3335 ,  88.6153 );
                        var  d10r38f  = new google.maps.LatLng( 27.3351 ,  88.6151 );
                        var  d10r38g  = new google.maps.LatLng( 27.3355 ,  88.6145 );
                        var  d10r38h  = new google.maps.LatLng( 27.3367 ,  88.613 );
                        var  d10r29a  = new google.maps.LatLng( 27.3342 ,  88.6139 );
                        var  d10r29b  = new google.maps.LatLng( 27.3352 ,  88.6124 );
                        var  d10r29c  = new google.maps.LatLng( 27.3356 ,  88.6115 );
                        var  d10r25a  = new google.maps.LatLng( 27.3562 ,  88.6192 );
                        var  d10r25b  = new google.maps.LatLng( 27.355 ,  88.617 );
                        var  d10r25c  = new google.maps.LatLng( 27.3679 ,  88.6172 );
                        var  d10r25d  = new google.maps.LatLng( 27.3682 ,  88.6106 );
                        var  d10r25e  = new google.maps.LatLng( 27.3674 ,  88.6097 );
                        var  d10r25f  = new google.maps.LatLng( 27.3671 ,  88.6099 );
                        var  d10r25g  = new google.maps.LatLng( 27.3279 ,  88.6117 );
                        var  d10r25h  = new google.maps.LatLng( 27.3276 ,  88.6127 );
                        var  d12r35a  = new google.maps.LatLng( 27.3412 ,  88.6078 );
                        var  d12r35b  = new google.maps.LatLng( 27.3388 ,  88.6087 );
                        var  d12r35c  = new google.maps.LatLng( 27.3393 ,  88.61 );
                        var  d12r35d  = new google.maps.LatLng( 27.3427 ,  88.6092 );
                        var  d12r32a  = new google.maps.LatLng( 27.3412 ,  88.6078 );
                        var  d12r32b  = new google.maps.LatLng( 27.3388 ,  88.6087 );
                        var  d12r32c  = new google.maps.LatLng( 27.3393 ,  88.61 );
                        var  d12r32d  = new google.maps.LatLng( 27.3427 ,  88.6092 );
                        var  d12r36a  = new google.maps.LatLng( 27.3412 ,  88.6078 );
                        var  d12r36b  = new google.maps.LatLng( 27.3388 ,  88.6069 );
                        var  d12r36c  = new google.maps.LatLng( 27.3408 ,  88.6064 );
                        var  d12r36d  = new google.maps.LatLng( 27.3421 ,  88.6047 );
                        var  d12r31a  = new google.maps.LatLng( 27.3412 ,  88.6078 );
                        var  d12r20a  = new google.maps.LatLng( 27.3412 ,  88.6078 );
                        var  d12r20b  = new google.maps.LatLng( 27.3388 ,  88.6069 );
                        var  d12r21a  = new google.maps.LatLng( 27.3412 ,  88.6078 );
                        var  d12r21b  = new google.maps.LatLng( 27.3388 ,  88.6069 );
                        var  d13r23a  = new google.maps.LatLng( 27.3287 ,  88.6133 );
                        var  d13r23b  = new google.maps.LatLng( 27.3303 ,  88.6127 );
                        var  d13r23c  = new google.maps.LatLng( 27.3306 ,  88.6132 );
                        var  d13r30a  = new google.maps.LatLng( 27.3287 ,  88.6133 );
                        var  d13r30b  = new google.maps.LatLng( 27.3303 ,  88.6127 );
                        var  d13r30c  = new google.maps.LatLng( 27.3306 ,  88.6132 );
                        var  d13r26a  = new google.maps.LatLng( 27.3287 ,  88.6133 );
                        var  d13r26b  = new google.maps.LatLng( 27.3278 ,  88.613 );
                        var  d13r26c  = new google.maps.LatLng( 27.3267 ,  88.6133 );
                        var  d13r26d  = new google.maps.LatLng( 27.3277 ,  88.6139 );
                        var  d13r26e  = new google.maps.LatLng( 27.3285 ,  88.6148 );
                        var  d13r26f  = new google.maps.LatLng( 27.3256 ,  88.6142 );
                        var  d14r27a  = new google.maps.LatLng( 27.3142 ,  88.6047 );
                        var  d14r27b  = new google.maps.LatLng( 27.313 ,  88.6049 );
                        var  d15r18a  = new google.maps.LatLng( 27.3233 ,  88.6113 );
                        var  d15r18b  = new google.maps.LatLng( 27.3241 ,  88.6116 );
                        var  d15r18c  = new google.maps.LatLng( 27.3267 ,  88.6114 );
                        var  d15r43a  = new google.maps.LatLng( 27.3233 ,  88.6113 );
                        var  d15r43b  = new google.maps.LatLng( 27.3241 ,  88.6116 );
                        var  d15r43c  = new google.maps.LatLng( 27.3267 ,  88.6114 );

                        var map_obj = {
                            '144': [{location: d1r44a, stopover: false}, {location: d1r44b, stopover: false}, {location: d1r44c, stopover: false}, {location: d1r44d, stopover: false}, {location: d1r44e, stopover: false}, {location: d1r44f, stopover: false}, {location: d1r44g, stopover: false}],
                            '340': [{location: d3r40a, stopover: false}, {location: d3r40b, stopover: false}, {location: d3r40c, stopover: false}, {location: d3r40d, stopover: false}],
                            '534': [{location: d5r34a, stopover: false}, {location: d5r34b, stopover: false}, {location: d5r34c, stopover: false}],
                            '619': [{location: d6r19a, stopover: false}, {location: d6r19b, stopover: false}, {location: d6r19c, stopover: false}, {location: d6r19d, stopover: false}],
                            '624': [{location: d6r24a, stopover: false}, {location: d6r24b, stopover: false}, {location: d6r24c, stopover: false}, {location: d6r24d, stopover: false}, {location: d6r24e, stopover: false}],
                            '628': [{location: d6r28a, stopover: false}, {location: d6r28b, stopover: false}, {location: d6r28c, stopover: false}, {location: d6r28d, stopover: false}, {location: d6r28e, stopover: false}],
                            '633': [{location: d6r33a, stopover: false}, {location: d6r33b, stopover: false}, {location: d6r33c, stopover: false}, {location: d6r33d, stopover: false}, {location: d6r33e, stopover: false}, {location: d6r33f, stopover: false}],
                            '837': [{location: d8r37a, stopover: false}, {location: d8r37b, stopover: false}, {location: d8r37c, stopover: false}, {location: d8r37d, stopover: false}, {location: d8r37e, stopover: false}, {location: d8r37f, stopover: false}, {location: d8r37g, stopover: false}, {location: d8r37h, stopover: false}, {location: d8r37i, stopover: false}, {location: d8r37j, stopover: false}, {location: d8r37k, stopover: false}],
                            '1041': [{location: d10r41a, stopover: false}, {location: d10r41b, stopover: false}, {location: d10r41c, stopover: false}],
                            '1044': [{location: d10r44a, stopover: false}, {location: d10r44b, stopover: false}, {location: d10r44c, stopover: false}],
                            '1038': [{location: d10r38a, stopover: false}, {location: d10r38b, stopover: false}, {location: d10r38c, stopover: false}, {location: d10r38d, stopover: false}, {location: d10r38e, stopover: false}, {location: d10r38f, stopover: false}, {location: d10r38g, stopover: false}, {location: d10r38h, stopover: false}],
                            '1029': [{location: d10r29a, stopover: false}, {location: d10r29b, stopover: false}, {location: d10r29c, stopover: false}],
                            '1025': [{location: d10r25a, stopover: false}, {location: d10r25b, stopover: false}, {location: d10r25c, stopover: false}, {location: d10r25d, stopover: false}, {location: d10r25e, stopover: false}, {location: d10r25f, stopover: false}, {location: d10r25g, stopover: false}, {location: d10r25h, stopover: false}],
                            '1235': [{location: d12r35a, stopover: false}, {location: d12r35b, stopover: false}, {location: d12r35c, stopover: false}, {location: d12r35d, stopover: false}],
                            '1232': [{location: d12r32a, stopover: false}, {location: d12r32b, stopover: false}, {location: d12r32c, stopover: false}, {location: d12r32d, stopover: false}],
                            '1236': [{location: d12r36a, stopover: false}, {location: d12r36b, stopover: false}, {location: d12r36c, stopover: false}, {location: d12r36d, stopover: false}],
                            '1231': [{location: d12r32a, stopover: false}],
                            '1220': [{location: d12r20a, stopover: false}, {location: d12r20b, stopover: false}],
                            '1221': [{location: d12r21a, stopover: false}, {location: d12r21b, stopover: false}],
                            '1323': [{location: d13r23a, stopover: false}, {location: d13r23b, stopover: false}, {location: d13r23c, stopover: false}],
                            '1330': [{location: d13r30a, stopover: false}, {location: d13r30b, stopover: false}, {location: d13r30c, stopover: false}],
                            '1326': [{location: d13r26a, stopover: false}, {location: d13r26b, stopover: false}, {location: d13r26c, stopover: false}, {location: d13r26d, stopover: false}, {location: d13r26e, stopover: false}, {location: d13r26f, stopover: false}],
                            '1427': [{location: d14r27a, stopover: false}, {location: d14r27b, stopover: false}],
                            '1518': [{location: d15r18a, stopover: false}, {location: d15r18b, stopover: false}, {location: d15r18c, stopover: false}],
                            '1543': [{location: d15r43a, stopover: false}, {location: d15r43b, stopover: false}, {location: d15r43c, stopover: false}]
                            }
                        var final = [
                            ['1', '44'],
                            ['3', '40'],
                            ['5', '34'],
                            ['6', '19'],
                            ['6', '24'],
                            ['6', '28'],
                            ['6', '33'],
                            ['8', '37'],
                            ['10', '41'],
                            ['10', '44'],
                            ['10', '38'],
                            ['10', '29'],
                            ['11', '25'],
                            ['12', '31'],
                            ['12', '36'],
                            ['12', '20'],
                            ['12', '21'],
                            ['12', '35'],
                            ['12', '32'],
                            ['13', '26'],
                            ['13', '23'],
                            ['13', '30'],
                            ['14', '27'],
                            ['15', '18'],
                            ['15', '43'],
                        ];

                        const map = new google.maps.Map(document.getElementById('map'), {
                            zoom: 13,
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
                        var set_marker = [];
                        for (i = 0; i < final.length; i++){
                            if (dmnd.includes(final[i][0]) && reli.includes(final[i][1])){
                                set_marker.push(final[i][0]);
                                set_marker.push(final[i][1]);
                            }
                        }
                        for (i = 0; i < Locations.length; i++) {
                            if (Locations[i][1] == "Demand" && set_marker.includes(Locations[i][0])){
                                marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(Locations[i][2], Locations[i][3]),
                                    map: map,
                                    icon: ReliefIcon,
                                    label: {color: '#ffffff', fontSize: '12px', fontWeight: '600',
                                    text: Locations[i][0]}
                                });
                            }
                            else if (Locations[i][1] == "Relief" && set_marker.includes(Locations[i][0])){
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
                            console.log(reliability);
                            if ( reliability < 0.5 )
                            {
                                green = Math.round((reliability * 2 * 255));
                                red = 255;
                                console.log("green");
                                console.log(green);
                            }
                            else
                            {
                                green = 255;
                                red = Math.round(((2 - 2 * reliability) * 255));
                                console.log("red");
                                console.log(red);
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
                                origin: map_obj[dmnd[0]+reli[0]][0]['location'],
                                waypoints: map_obj[dmnd[0]+reli[0]].slice(1,-1),
                                destination:map_obj[dmnd[0]+reli[0]].slice(-1)[0]['location'],
                                optimizeWaypoints: true,
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
    display_df = pd.read_csv("Data/data.csv", encoding= "unicode_escape")

    # Creating JSON for Frontend
    # JSON "index": [Demand node, Relief point, Population Capacity, Allocated Evacuation Trips, 
    #                 Reliability value]
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
    return JSONResponse({'status_code' : 200})

@app.post("/testpost/")
def testPost():
    return JSONResponse({'msg': "test successfull", 'status_code' : 400})
    