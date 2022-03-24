import json
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional

html_content = """
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

.s-controls{
    width: 20%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 25px;
    
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

.flex-container {
    min-height: 88%;
    display: flex;
    border-radius: 25px;
    text-align: center;
    justify-content: center;
}

.flex-child {
    flex: 1;
    align-self: center;
    border-radius: 25px;
    margin-right: 20px;
    border: 2px solid white;
}
/*
.flex-child:first-child {
    margin-right: 20px;
    height: 100%;
}
*/
#map {
    align-self: center;
    border-radius: 25px;
    height: 500px;
    width: 200px;
    /* The width is the width of the web page */

    flex: auto;
        border: 2px solid black;
}
  
#container {
    height: 100%;
    display: flex;
  }
  
</style>
<body>
             <div class="top_banner">
                <h1>Dashboard</h1>
             </div>
             <div>
             
             <input id="key" class="controls" type="number" placeholder="Relief point number" />
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
                    const mytable = document.getElementById("html-data-table");
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
                        var
                         key = document.getElementById("key").value-1
                        location.href = "/handler/?number="+document.getElementById("number").value+"&key="+key;
                    };
                </script>

             </div>
             <div class="flex-container">
                <div class="flex-child text">
                    <table id = html-data-table>
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
                    <div id="map"></div>
                    <script
                         src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBHLMLeLRKTCHcBBQtpJRSnq_yMiNrDzbY" type="text/javascript">
                        </script>
            </div>
            </div>
                         <script>
            const myloc = {
                        lat: 27.302524795918504,
                        lng: 88.59751338243387
                        };
                    var LocationsForMap = [
                        ['1', 27.302524795918504, 88.59751338243387],
                        ['2', 27.309941653731695, 88.59884377512124],
                        ['3', 27.30582333235349, 88.58828660114838],
                        ['4', 27.310361103820796, 88.60686894416531],
                        ['5', 27.293448382503307, 88.5876643286917],
                        ['6', 27.3022574472417, 88.61036710954333],
                        ['7', 27.29443927704333, 88.60976569341749],
                        ['8', 27.299968941716006, 88.61238427207702],
                        ];

                        const map = new google.maps.Map(document.getElementById('map'), {
                            zoom: 15,
                            center: myloc,
                        });

                        var infowindow = new google.maps.InfoWindow();

                        var marker, i;
                        var mIcon = {
                            path: google.maps.SymbolPath.CIRCLE,
                            fillOpacity: 1,
                            fillColor: '#fff',
                            strokeOpacity: 1,
                            strokeWeight: 1,
                            strokeColor: '#333',
                            scale: 12
                        };
                        for (i = 0; i < LocationsForMap.length; i++) {  
                        marker = new google.maps.Marker({
                            position: new google.maps.LatLng(LocationsForMap[i][1], LocationsForMap[i][2]),
                            map: map,
                            icon: mIcon,
                            label: {color: '#000', fontSize: '12px', fontWeight: '600',
                              text: String(i+1)}
                        });
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
async def create_table():
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
    with open('Data/display_data', 'w') as fp:
        json.dump(display_df.T.to_dict('list'), fp, sort_keys=True, indent=4)

    return HTMLResponse(content=html_content, status_code=200)

@app.get("/handler/")
def update_table(number: int, key: str, msg: Optional[str] = ""):
    # JSON "index": [Reliability value, Population served, Population unserved, 
    #                 Demand node, Relief point]
    with open('Data/display_data', 'r') as fp:
        display_data = json.load(fp)
    # Get Key and Number of People from request
    # Check if Population unserved is negative, ie there is room for more population to serve
    if (display_data[key][2] + number) <=0:
        display_data[key][2] += number
        msg += "Update Successful. "
    # Alert added to warn population limit after changes
        if display_data[key][2] > -1:
            msg += "Cannot add anymore people. "
    # Saving JSON at end of task
        with open('Data/display_data', 'w') as fp:
            json.dump(display_data, fp, sort_keys=True, indent=4)
    else:
        msg += "Entered value exceeds the population limit. "
        return HTMLResponse(content=html_content, status_code=400)
    display_data.update({'msg': msg})
    return HTMLResponse(content=html_content, status_code=200)