AmCharts.makeChart("map",{
					"type": "map",
					"pathToImages": "http://www.amcharts.com/lib/3/images/",
					"addClassNames": true,
					"fontSize": 15,
					"color": "#FFFFFF",
					"projection": "mercator",
					"backgroundAlpha": 1,
					"backgroundColor": "rgba(80,80,80,1)",
					"dataProvider": {
						"map": "australiaLow",
						"getAreasFromMap": true,
						"images": [
							{
								"selectable":true,
								"longitude": 118.2167,
								"latitude": -26.8975,
								"label": "Western Australia",
								"labelPosition": "right",
								"labelColor": "rgba(5,5,5,0.99)",
								"labelRollOverColor": "#060606",
								"labelFontSize": 15,
								"width": 150,
							    "height":150,
							    "pie": {
							        "type":"pie",
							        "pullOutRadius":0,
							        "labelRadius": 0,
                                    "dataProvider": [{
                                      "category": "Category #1",
                                      "value": 1200
                                    }, {
                                      "category": "Category #2",
                                      "value": 500
                                    }, {
                                      "category": "Category #3",
                                      "value": 765
                                    }, {
                                      "category": "Category #4",
                                      "value": 260
                                    }],
                                    "labelText": "[[value]]%",
                                    "valueField": "value",
                                    "titleField": "category"
                                    }
							},
							{
								"selectable": true,
								"longitude": 129.1472,
								"latitude": -21.3235,
								"label": "Northern Territory",
								"labelPosition": "right",
								"labelColor": "rgba(3,3,3,0.99)",
								"labelRollOverColor": "#030303",
								"labelFontSize": 15
							},
							{
								"selectable": true,
								"longitude": 142.0188,
								"latitude": -24.2761,
								"label": "Queensland",
								"labelPosition": "right",
								"labelColor": "rgba(0,0,0,0.99)",
								"labelRollOverColor": "#000000",
								"labelFontSize": 15
							},
							{
								"selectable": true,
								"longitude": 131.6829,
								"latitude": -30.0773,
								"label": "South Australia",
								"labelPosition": "right",
								"labelColor": "rgba(0,0,0,0.99)",
								"labelRollOverColor": "#000000",
								"labelFontSize": 15
							},
							{
								"selectable": true,
								"longitude": 143.4953,
								"latitude": -32.8098,
								"label": "New South Wales",
								"labelPosition": "right",
								"labelColor": "rgba(0,0,0,0.99)",
								"labelRollOverColor": "#000000",
								"labelFontSize": 15
							},
							{
								"selectable": true,
								"longitude": 142.7275,
								"latitude": -37.6994,
								"label": "Victoria",
								"labelPosition": "right",
								"labelColor": "rgba(0,0,0,0.99)",
								"labelRollOverColor": "#000000",
								"labelFontSize": 15
							},
							{
								"selectable": true,
								"longitude": 145.3263,
								"latitude": -42.2866,
								"label": "Tasmania",
								"labelPosition": "right",
								"labelColor": "rgba(0,0,0,0.99)",
								"labelRollOverColor": "#000000",
								"labelFontSize": 15
							},
						],
						 "listeners": [ {
                                    "event": "clickMapObject",
                                    "method": function( event ) {
                                      // deselect the area by assigning all of the dataProvider as selected object
                                      map.selectedObject = map.dataProvider;

                                      // toggle showAsSelected
                                      event.mapObject.showAsSelected = !event.mapObject.showAsSelected;

                                      // bring it to an appropriate color
                                      map.returnInitialColor( event.mapObject );

                                      // let's build a list of currently selected states
                                      var states = [];
                                      for ( var i in map.dataProvider.areas ) {
                                        var area = map.dataProvider.areas[ i ];
                                        if ( area.showAsSelected ) {
                                          states.push( area.title );
                                        }
                                      }
                                      console.log(states)
                                    }
                                  } ],
						"areas": [
							{
								"id": "AU-NT",
								"title": "Northern Territory",
								"color": "rgba(21,255,0,0.99)",
								"url":"NT.html"
							},
							{
								"id": "AU-WA",
								"title": "Western Australia",
								"color": "rgba(75,216,181,0.8)",
								"url":"WA.html"
							},
							{
								"id": "AU-NSW",
								"title": "New South Wales",
								"color": "rgba(187,0,255,0.99)",
								"url":"NSW.html"
							},
							{
								"id": "AU-SA",
								"title": "South Australia",
								"color": "rgba(216,75,75,0.99)",
								"url":"SA.html"
							},
							{
								"id": "AU-VIC",
								"title": "Victoria",
								"color": "rgba(255,250,0,0.99)",
								"url":"VT.html"
							},
							{
								"id": "AU-QLD",
								"title": "Queensland",
								"color": "rgba(87,75,216,0.99)",
								"url":"QL.html"

							},
							{
								"id": "AU-TAS",
								"title": "Tasmania",
								"color": "rgba(255,156,0,0.99)",
								"url":"TM.html"
							}
						]
					},
					"balloon": {
						"horizontalPadding": 15,
						"borderAlpha": 0,
						"borderThickness": 1,
						"verticalPadding": 15
					},
					"areasSettings": {
						"color": "rgba(129,129,129,1)",
						"outlineColor": "rgba(80,80,80,1)",
						"rollOverOutlineColor": "rgba(80,80,80,1)",
						"rollOverBrightness": 20,
						"selectedBrightness": 20,
						"selectable": true,
						"unlistedAreasAlpha": 0,
						"unlistedAreasOutlineAlpha": 0
					},
					"imagesSettings": {
						"alpha": 1,
						"color": "rgba(129,129,129,1)",
						"outlineAlpha": 0,
						"rollOverOutlineAlpha": 0,
						"outlineColor": "rgba(80,80,80,1)",
						"rollOverBrightness": 20,
						"selectedBrightness": 20,
						"selectable": true
					},
					"linesSettings": {
						"color": "rgba(129,129,129,1)",
						"selectable": true,
						"rollOverBrightness": 20,
						"selectedBrightness": 20
					},
					"zoomControl": {
						"zoomControlEnabled": true,
						"homeButtonEnabled": false,
						"panControlEnabled": false,
						"right": 38,
						"bottom": 30,
						"minZoomLevel": 0.25,
						"gridHeight": 100,
						"gridAlpha": 0.1,
						"gridBackgroundAlpha": 0,
						"gridColor": "#FFFFFF",
						"draggerAlpha": 1,
						"buttonCornerRadius": 2
					}
				});
