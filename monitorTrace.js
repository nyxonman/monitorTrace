

console.log("jsonData", jsonData)
RTT_CHART_ID = 'rtt'
MODE_CHART_ID = 'mode'
CHAN_CHART_ID = 'chan'
TIMELINE_CHART_ID = 'timeline'

// types of charts
charts = {
	"rtt": {},
	"clTimings": {},
	"timeline": {},
	"buffer": {},
	'modechan': {},
};

// datasets for different charts
datasets = {
	"rtt": [],
	"clTimings": [],
	"timeline": [],
	"buffer": [],
	'modechan': [],
}

// chart options for different charts
chartOptions = {
	'rtt': {
		"chartTitle": "RTT between clData.get and clData.cnf",
		"xAxisType": 'linear',
		"xAxisTitle": "RTT in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,
		// "thTitle"    : "Max Power",
		// "thValue"    : "13"

	},
	'mode': {
		"chartTitle": "Mode Usage",
		"xAxisType": 'category',
		"xAxisTitle": "Modes",
		"yAxisTitle": "Count",
		// "yAxisTitle2": "PDF/CDF",
		// "yAxis2Max": 1,
		// "thTitle"    : "Max Power",
		// "thValue"    : "13"

	},
	'chan': {
		"chartTitle": "Chan Usage",
		"xAxisType": 'category',
		"xAxisTitle": "Channel",
		"yAxisTitle": "Count",
		// "yAxisTitle2": "",
		// "yAxis2Max": 1,
		// "thTitle"    : "Max Power",
		// "thValue"    : "13"

	},
	'timeline': {
		"chartTitle": "Timeline VIsualiser",
		"xAxisType": 'linear',
		"xAxisTitle": "Timestamp in usecs",
		"yAxisMax": 7,
		"yAxisMin": -7,
		// "yAxisTitle": "",
		// "yAxisTitle2": "",
		// "yAxis2Max": ,
		// "thTitle"    : "Max Power",
		// "thValue"    : "13"

	},

};


function drawChart(chartId, renderFlag) {
	var chart;
	document.getElementById('chartContainer').innerHTML = ""
	document.getElementById('container').innerHTML = ""
	switch (chartId) {
		case RTT_CHART_ID:
			create_rtt_chart(renderFlag);
			break;
		case MODE_CHART_ID:
			create_mode_chart(renderFlag);
			break;
		case CHAN_CHART_ID:
			create_chan_chart(renderFlag);
			break
		case TIMELINE_CHART_ID:
			create_timeline_chart(renderFlag);
			break;
		default:
			alert("Improper chart type " + chartId + " for ");
	}

}
// console.log(dataPoints)

function create_chart(id, chartData) {
	console.log(id, chartData)
	var chart = new CanvasJS.Chart("chartContainer",
		{
			animationEnabled: true,
			// colorSet         : "uniqueColorSet",
			// animationDuration: 10000,
			exportEnabled: true,
			animationRender: true,
			zoomEnabled: true,

			//zoomType       : "xy",
			toolTip: {
				shared: true
			},
			title: {
				text: chartOptions[id].chartTitle
			},
			axisX: {
				title: chartOptions[id].xAxisTitle,
				// valueFormatString: "YYYY/MM/DD HH:mm:ss" ,
				// labelAngle: -45,
				crosshair: {
					enabled: true,
					snapToDataPoint: true
				}
			},
			/*axisX2:{
			 title : "Secondary X Axis"
			},*/

			axisY: {
				title: chartOptions[id].yAxisTitle,
				// stripLines:[
				// {
				//     value:chartOptions[RTT_CHART_ID].thValue,
				//     label:chartOptions[RTT_CHART_ID].thTitle+" "+chartOptions[RTT_CHART_ID].thValue
				// }
				// ],
				// maximum:,
				crosshair: {
					enabled: false,
					snapToDataPoint: true,
					/*labelFormatter: function(e) {
						return "$" + CanvasJS.formatNumber(e.value, "##0.00");
					}*/
				}
			},
			/* axisY2:{
				 title : "Secondary Y Axis"
			 },*/
			legend: {
				horizontalAlign: "center", // left, center ,right
				verticalAlign: "top",  // top, center, bottom
				cursor: "pointer",
				itemclick: function (e) {
					//console.log("legend click: " + e.dataPointIndex);
					//console.log(e);
					if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
						e.dataSeries.visible = false;
					} else {
						e.dataSeries.visible = true;
					}

					e.chart.render();
				}
			},
			data: chartData
		});

	return chart
}

var zoomRatio = 1;
var lastX;
var lastY;
var mouseDown;
var chart;
var markerCnt = 0

function create_marker_line(markerNum, frt) {
	var marker = {
		'first' : {
			'elem':null,
			'val':null,
		}
	}
	var markerListDiv = document.getElementById('markersList')
	console.log("markerDiv",markerListDiv.innerHTML)
	var firstMarkerNum=0
	var secondMarkerNum = 0;
	var firstMarkerElem, secondMarkerElem;
	var firstMarkerVal=0, secondMarkerVal=0;
	if (markerNum % 2 != 0) {
		firstMarkerNum = markerNum
		secondMarkerNum = markerNum +1
		lineHtml = `<div class="marker" id="divMarkerVal-${firstMarkerNum}-${secondMarkerNum}">
		<div style="width:33%;">M${firstMarkerNum}: <span name="marker1" class="markerVal" id="marker${firstMarkerNum}Val"> </span></div>
		<div style="width:33%;">M${secondMarkerNum}: <span name="marker2" class="markerVal" id="marker${secondMarkerNum}Val"> </span></div>
		<div style="width:33%;">delta: <span class= "deltaVal" id="deltaVal${firstMarkerNum}${secondMarkerNum}" readonly> </span></div>
		<button class= "removeMkrBtnClass" id="removeMkrBtn${firstMarkerNum}${secondMarkerNum}" >X</button>
		</div>`



		markerListDiv.innerHTML = markerListDiv.innerHTML + lineHtml
	}else{
		firstMarkerNum = markerNum-1
		secondMarkerNum = markerNum
	}

	firstMarkerElem = document.getElementById(`marker${firstMarkerNum}Val`)
	secondMarkerElem = document.getElementById(`marker${secondMarkerNum}Val`)

	console.log("first",firstMarkerNum, "second", secondMarkerNum)

	if (markerNum % 2 != 0) {
		firstMarkerVal = parseInt(frt, 10)
		firstMarkerElem.innerHTML = firstMarkerVal
		secondMarkerVal = document.getElementById(`marker${secondMarkerNum}Val`).innerHTML
	}else{
		firstMarkerVal = document.getElementById(`marker${firstMarkerNum}Val`).innerHTML
		secondMarkerVal = parseInt(frt, 10)
		secondMarkerElem.innerHTML = secondMarkerVal
	}
	console.log("firstVal",firstMarkerVal, "secondVal", secondMarkerVal)

	if(firstMarkerVal!= 0  && secondMarkerVal != 0){
		var delta = parseInt(secondMarkerVal) - parseInt(firstMarkerVal)
		console.log("delta = ", delta)
		deltaElem = document.getElementById(`deltaVal${firstMarkerNum}${secondMarkerNum}`)
		deltaElem.innerHTML = delta
	}


	// m1Val = $("#marker1Val").val()
	// m2Val = $("#marker2Val").val()

	// markerListDiv.appendChild(lineHtml)
}


function create_highchart(id, chartData, containerDiv = 'container') {
	console.log(id, chartData)
	chart = Highcharts.chart(containerDiv, {

		chart: {
			// type: 'bar'
			// zoomKey:'alt',
			zoomType: 'x',
			panKey: 'ctrl',
			panning: true,
			events: {
				click: function (e) {
					let chart = this;
					let xAxis = chart.xAxis[0];
					let xValue = xAxis.toValue(this.mouseDownX);

					let clickX = 0;
					markerCnt++
					console.log("marker ", markerCnt, xValue)
					create_marker_line(markerCnt, xValue)
					// if (markerCnt < 3) {


					xAxis.addPlotLine({
						value: xValue,
						color: '#ff0000',
						width: 1,
						label: {
							rotation: 90,
							text: `M${markerCnt}`,
							className: "markerLabel" + markerCnt
						},
						zIndex: 99,
						className: `marker marker${markerCnt}Line`,
						events: {
							mousedown: function (e) {
								chart.clickX = e.pageX;
								chart.activePlotLine = this;
							}
						}
					});
					// } else {
					// 	markerCnt = 2
					// }



				}
			}
			// panning :{
			// 	type:'x'
			// },
		},

		title: {
			text: chartOptions[id].chartTitle
		},
		plotOptions: {
			area: {
				marker: {
					enabled: false,
					states: {
						hover: { enabled: false }
					}
				},
				// states: {
				// 	inactive: {
				// 		opacity: 0.7
				// 	}
				// },
			},

		},
		legend: {

			verticalAlign: 'top',
		},
		tooltip: {
			// headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
			// pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
			// 	'<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
			// footerFormat: '</table>',
			shared: true,
			// split:true,
			useHTML: true,
			followPointer: false,
			outside: true
		},
		xAxis: {
			title: {
				text: chartOptions[id].xAxisTitle
			},
			type: chartOptions[id].xAxisType,
			crosshair: true,
			// plotLines: [{
			//     id: 'foo',
			//     color: '#00F',
			//     width: 10,
			//     value: 543214567,
			//     onDragStart: function (new_value) {
			//         $("#x_value").text(new_value + ' (Not changed yet)');
			//     },
			//     onDragChange: function (new_value) {
			//         $("#x_value").text(new_value + ' (Dragging)');
			//     },
			//     onDragFinish: function (new_value) {
			//         $("#x_value").text(new_value);
			//     }
			// }]
		},

		yAxis: [{ // Primary yAxis
			// visible:id==TIMELINE_CHART_ID? false:trues,
			labels: {
				enabled: id == TIMELINE_CHART_ID ? false : true,
				// format: '{value}°C',
				// style: {
				// 	color: Highcharts.getOptions().colors[1]
				// }
			},
			plotLines: [{
				value: 0,
				width: 1,
				color: '#999',
				zIndex: 10
			}],
			title: {
				text: chartOptions[id].yAxisTitle,
				// style: {
				// 	color: Highcharts.getOptions().colors[1]
				// }
			},
			// max:  null,
			max: chartOptions[id].yAxisMax ? chartOptions[id].yAxisMax : null,
			min: chartOptions[id].yAxisMin ? chartOptions[id].yAxisMin : null,

		}, { // Secondary yAxis
			title: {
				text: chartOptions[id].yAxisTitle2 ? chartOptions[id].yAxisTitle2 : null,
				// style: {
				// 	color: Highcharts.getOptions().colors[0]
				// }

			},
			max: chartOptions[id].yAxis2Max ? chartOptions[id].yAxis2Max : null,
			// const a = { ...(condition && {b: 1}) // if condition is true 'b' will be added. }

			// labels: {
			// 	format: '{value} mm',
			// 	style: {
			// 		color: Highcharts.getOptions().colors[0]
			// 	}
			// },
			opposite: true
		}],
		// plotOptions: {
		// 	series: {
		// 		color: Highcharts.getOptions().colors[0],
		// 		grouping: false
		// 	}
		// },

		series: chartData

	});




}


function create_rtt_chart(renderFlag) {
	console.log('creating RTT')
	let freqData = []
	let pdfData = []
	let cdfData = []
	let x_data = []
	let freq_y_data = []
	let pdf_y_data = []
	let cdf_y_data = []
	jsonData.rttJson.forEach(item => {
		freqData.push({ x: item.diff, y: item.freq })
		pdfData.push({ x: item.diff, y: item.pdf })
		cdfData.push({ x: item.diff, y: item.cdf })
		x_data.push(item.diff)
		freq_y_data.push(item.freq)
		pdf_y_data.push(item.pdf)
		cdf_y_data.push(item.cdf)
	});

	let chartData = [
		/* count */
		{
			type: "column",
			axisYType: 'primary',
			name: "Freq",
			showInLegend: true,
			legendText: "Freq",
			// visible: false, //***hidden
			dataPoints: freqData,

		},
		/* pdf */
		{
			type: "line",
			name: "PDF",
			axisYType: 'secondary',
			showInLegend: true,
			legendText: "PDF",
			dataPoints: pdfData,

		},
		/* cdf */
		{
			type: "line",
			name: "CDF",
			axisYType: 'secondary',
			showInLegend: true,
			legendText: "CDF",
			dataPoints: cdfData,

		},

	]

	var chart = create_chart(RTT_CHART_ID, chartData)

	if (renderFlag)
		chart.render();

	chartData = [
		/* count */
		{
			type: "column",
			// axisYType: 'primary',
			name: "Freq",
			// showInLegend: true,
			// legendText: "Freq",
			// visible: false, //***hidden
			data: freqData,
			color: Highcharts.getOptions().colors[0]
		},
		/* pdf */
		{
			type: "line",
			name: "PDF",
			yAxis: 1,
			// showInLegend: true,
			// legendText: "PDF",
			data: pdfData,
			color: Highcharts.getOptions().colors[3]
		},
		/* cdf */
		{
			type: "line",
			name: "CDF",
			yAxis: 1,
			// showInLegend: true,
			// legendText: "CDF",
			data: cdfData,
			color: Highcharts.getOptions().colors[2]
		},

	]
	create_highchart(RTT_CHART_ID, chartData)



	return

}

function create_mode_chart(renderFlag) {
	console.log('creating modechanchart')
	let modeRxData = []
	let modeTxData = []

	// let pdfData = []
	// let cdfData = []
	jsonData.modeRxJson.forEach(item => {
		modeRxData.push({ label: item.mode, y: item.count })
	});
	jsonData.modeTxJson.forEach(item => {
		modeTxData.push({ label: item.mode, y: item.count })
	});
	chartData = [
		/* count */
		{
			type: "column",
			axisYType: 'primary',
			name: "Mode Rx",
			showInLegend: true,
			legendText: "Mode Rx",
			// visible: false, //***hidden
			dataPoints: modeRxData,

		},
		/* pdf */
		{
			type: "column",
			name: "Mode Tx",
			axisYType: 'primary',
			showInLegend: true,
			legendText: "Mode Tx",
			dataPoints: modeTxData,

		},


	]
	var chart = create_chart(MODE_CHART_ID, chartData)

	if (renderFlag)
		chart.render();

	jsonData.modeRxJson.forEach(item => {
		modeRxData.push({ name: item.mode, y: item.count })
	});
	jsonData.modeTxJson.forEach(item => {
		modeTxData.push({ name: item.mode, y: item.count })
	});

	chartData = [
		/* count */
		{
			type: "column",
			// axisYType: 'primary',
			name: "ModeRx",
			// showInLegend: true,
			// legendText: "Freq",
			// visible: false, //***hidden
			data: modeRxData,
			color: Highcharts.getOptions().colors[7]
		},
		/* pdf */
		{
			type: "column",
			name: "ModeTx",
			// showInLegend: true,
			// legendText: "PDF",
			data: modeTxData,
			color: Highcharts.getOptions().colors[3]
		},


	]
	create_highchart(MODE_CHART_ID, chartData)


}
function create_chan_chart(renderFlag) {
	console.log('creating chanchanchart')
	let chanRxData = []
	let chanTxData = []

	// let pdfData = []
	// let cdfData = []
	jsonData.chanRxJson.forEach(item => {
		chanRxData.push({ label: item.chan, y: item.count })
	});
	jsonData.chanTxJson.forEach(item => {
		chanTxData.push({ label: item.chan, y: item.count })
	});
	let chartData = [
		/* count */
		{
			type: "column",
			axisYType: 'primary',
			name: "chan Rx",
			showInLegend: true,
			legendText: "chan Rx",
			// visible: false, //***hidden
			dataPoints: chanRxData
		},
		/* pdf */
		{
			type: "column",
			name: "chan Tx",
			axisYType: 'primary',
			showInLegend: true,
			legendText: "chan Tx",
			dataPoints: chanTxData
		},


	]
	var chart = create_chart(CHAN_CHART_ID, chartData)

	if (renderFlag)
		chart.render();
	chanRxData = []
	chanTxData = []

	jsonData.chanRxJson.forEach(item => {
		chanRxData.push({ name: item.chan, y: item.count })
	});
	jsonData.chanTxJson.forEach(item => {
		chanTxData.push({ name: item.chan, y: item.count })
	});

	chartData = [
		/* count */
		{
			type: "column",
			// axisYType: 'primary',
			name: "Chan Rx",
			// showInLegend: true,
			// legendText: "Freq",
			// visible: false, //***hidden
			data: chanRxData,
			color: Highcharts.getOptions().colors[7]
		},
		/* pdf */
		{
			type: "column",
			name: "Chan Tx",
			// showInLegend: true,
			// legendText: "PDF",
			data: chanTxData,
			color: Highcharts.getOptions().colors[3]
		},


	]
	create_highchart(CHAN_CHART_ID, chartData)


}
let rawData = [
	{ name: 'D', x: 2, y: 2, dur: 2 },
	// { name: 'B', x: , y:2 ,dur:5},
	{ name: 'A', x: 5, y: 2, dur: 10 },
	// { name: 'E', x: 8, y:2 ,dur:10},
	{ name: 'C', x: 21, y: 2, dur: 20 },
];
function makeSeries(listOfData) {
	var sumX = 0.0;
	for (var i = 0; i < listOfData.length; i++) {
		sumX += listOfData[i].x;
	}
	var gap = sumX / rawData.length * 0.2;
	var allSeries = []
	var x = 0.0;
	for (var i = 0; i < listOfData.length; i++) {
		var data = listOfData[i];
		allSeries[i] = {
			name: data.name,
			data: [
				[data.x, 0], [data.x, data.y],
				{
					x: x + data.x / 2.0,
					y: data.y,
					dataLabels: { enabled: true, format: data.x + ' x {y}' }
				},
				[data.dur + data.x, data.y], [data.dur + data.x, 0]
			],
			w: data.x,
			h: data.y
		};
		x += data.x + gap;
	}
	console.log("allseries", allSeries)
	return allSeries;
}

function create_timeline_chart(renderFlag) {
	console.log('creating timeline chart')
	let chanRxData = []
	let ts_txData = []
	let ts_rxData = []
	let first = true
	let chartData = []
	let dataPoints = []

	/* TX area*/
	jsonData.timeline_txJson.forEach(item => {
		chartData.push({
			type: 'area',
			data: [
				[item.ts_txstart, 0],
				[item.ts_txstart, 1],
				{
					x: item.ts_txstart + item.tx_dur / 2.0,
					y: 1,
					// dataLabels: { enabled: true, format: '{x} x {y}' }
				},
				[item.ts_txend, 1],
				// [item.ts_txend, 1],

			],
			states: {
				inactive: {
					opacity: 0.8
				}
			},

			zIndex: 5,
			// name: "CL " + item.cl_id,
			name: "TX",
			showInLegend: false,
			color: item.color,
			tooltip: {
				split: true,
				// followPointer: true,
				useHTML: true,
				headerFormat: '<span style="color: {series.color}">{series.name}</span>: ',
				pointFormat: '<span>FRT: {point.x}</span><br>' + item.hoverinfo
			},
		})
	});

	/* RX area */
	jsonData.timeline_rxJson.forEach(item => {
		chartData.push({
			type: 'area',

			data: [
				[item.ts_rxstart, 0], [item.ts_rxstart, -1],
				{
					x: item.ts_rxstart + item.rx_dur / 2.0,
					y: -1,
					// dataLabels: { enabled: true, format: '{x} x {y}',},
					toolTip: false
				},
				[item.ts_rxend, -1],
				// [item.ts_rxend, -1],

			],
			states: {
				inactive: {
					opacity: 0.8
				}
			},
			showInLegend: false,
			zIndex: 5,
			name: "RX",
			color: item.color,
			tooltip: {
				// followPointer: true,
				useHTML: true,
				headerFormat: '<span style="color: {series.color}">{series.name}</span>: ',
				pointFormat: '<span>FRT: {point.x}</span><br>' + item.hoverinfo
			},
		})
	});
	/* CL area */
	jsonData.timeline_clStartEndJson.forEach(item => {
		chartData.push({
			type: 'area',
			data: [
				[item.clstart, 0], [item.clstart, 3],
				{
					x: item.clstart + item.cldiff / 2.0,
					y: 3,
					dataLabels: { enabled: true, format: item.hoverinfo }
				},
				[item.clend, 3], [item.clend, 0],
				[item.clend, -3], [item.clstart, -3],
				[item.clstart, 0],
			],
			states: {
				inactive: {
					opacity: 0.8
				}
			},
			// dataLabels: { enabled: true, format: item.hoverinfo, inside: true },
			zIndex: 1,
			showInLegend: false,
			grouping: true,
			name: "CL " + item.cl_id,
			fillColor: 'rgba(247, 228, 194,0.35)',
			color: "rgba(247, 228, 194,1)",

			// tooltip:null
			tooltip: {
				// followPointer: true,
				useHTML: true,
				headerFormat: '<span style="color: {series.color}">{series.name}</span>: ',
				pointFormat: '<span>FRT: {point.x}</span> ' + item.hoverinfo
			},
		})
	})

	/* Phy Data Indications */
	dataPoints = [];
	dataPoints = jsonData.timeline_phyIndJson.map((item) => {
		if (!Number(item.frt_dec)) {
			console.log("Error..", item)
		}
		return {
			x: item.frt_dec,
			y: -6,
			color: item.color,
			info: item.trace_info
		}
	});

	chartData.push({
		type: "scatter",
		// axisYType: 'primary',
		name: "phyData Indications",
		showInLegend: true,
		states: {
			inactive: {
				opacity: 0.8
			}
		},
		visible: false, //***hidden
		data: dataPoints,
		tooltip: {
			headerFormat: '<span style="font-size:10px">FRT: {point.key}</span><table>',
			pointFormat: '<tr><td style="color:{series.color};padding:0">{point.info} </td></tr>',
			footerFormat: '</table>',
			// shared: true,
			useHTML: true,
			followPointer: false,
			// outside: true
		},
		marker: {
			symbol: "triangle"
		},
		turboThreshold: 0,


	})

	/* CL Traces */
	dataPoints = [];
	dataPoints = jsonData.timeline_clTracesJson.map((item) => {
		return {
			x: item.frt_dec,
			y: 6,
			color: item.color,
			info: item.trace_info,
			clid: item.cl_id
		}
	});
	chartData.push({
		type: "scatter",
		// axisYType: 'primary',
		name: "CL Traces",
		showInLegend: true,
		states: {
			inactive: {
				opacity: 0.8
			}
		},
		marker: {
			symbol: "triangle-down"
		},
		color: "red",
		visible: false, //***hidden
		data: dataPoints,
		tooltip: {
			headerFormat: '<span style="font-size:10px">FRT: {point.key}, CL id {point.clid}</span><table>',
			pointFormat: '<tr><td style="color:{series.color};padding:0">{point.info} </td></tr>',
			footerFormat: '</table>',
			// shared: true,
			useHTML: true,
			followPointer: false,
			// outside: true
		},
		turboThreshold: 0,

	})


	create_highchart(TIMELINE_CHART_ID, chartData)

}
function openGraph(evt, tabName) {
	var i, tabcontent, tablinks;
	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i < tabcontent.length; i++) {
		tabcontent[i].style.display = "none";
	}
	tablinks = document.getElementsByClassName("tablinks");
	for (i = 0; i < tablinks.length; i++) {
		tablinks[i].className = tablinks[i].className.replace(" active", "");
	}
	document.getElementById(tabName).style.display = "block";
	evt.currentTarget.className += " active";
	graphId = evt.currentTarget.attributes.graphId.value
	drawChart(graphId, true)
}
window.onload = function () {
	console.log("document ready")

	// drawChart(RTT_CHART_ID, true)
	document.getElementById("firstTab").click();

	$(document).on("click", ".removeMkrBtnClass", function(event){
		// console.log("clicked",event)
		// console.log($(this))
		parentRow=$(this).parent()
		id = parentRow.attr('id').split('-')
		$(`.marker${id[1]}Line`).remove()
		$(`.marker${id[2]}Line`).remove()
		$(`.markerLabel${id[1]}`).remove()
		$(`.markerLabel${id[2]}`).remove()
		// console.log("parent", parentRow.attr('id'))
		parentRow.remove()

	});



	// var mytabs = document.getElementsByClassName()



}


