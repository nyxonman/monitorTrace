

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

var markerCnt = 0

function create_marker_line(markerNum, frt, markerColor) {

	var markerListDiv = document.getElementById('markersList')
	var firstMarkerNum = 0
	var secondMarkerNum = 0;
	var firstMarkerElem, secondMarkerElem;
	var firstMarkerVal = 0, secondMarkerVal = 0;
	if (markerNum % 2 != 0) {
		firstMarkerNum = markerNum
		secondMarkerNum = markerNum + 1
		lineHtml = `<div class="marker" style="border:2px solid ${markerColor}"id="divMarkerVal-${firstMarkerNum}-${secondMarkerNum}">
		<div style="width:33%; ">M${firstMarkerNum}: <span name="marker1" class="markerVal" id="marker${firstMarkerNum}Val"> </span></div>
		<div style="width:33%; ">M${secondMarkerNum}: <span name="marker2" class="markerVal" id="marker${secondMarkerNum}Val"> </span></div>
		<div style="width:33%; ">delta: <span class= "deltaVal" id="deltaVal${firstMarkerNum}${secondMarkerNum}" readonly> </span></div>
		<button class= "btn btn-sm btn-outline-secondary removeMkrBtnClass" id="removeMkrBtn${firstMarkerNum}${secondMarkerNum}" >X</button>
		</div>`

		markerListDiv.innerHTML = markerListDiv.innerHTML + lineHtml
	} else {
		firstMarkerNum = markerNum - 1
		secondMarkerNum = markerNum
	}

	firstMarkerElem = document.getElementById(`marker${firstMarkerNum}Val`)
	secondMarkerElem = document.getElementById(`marker${secondMarkerNum}Val`)

	if (markerNum % 2 != 0) {
		firstMarkerVal = parseInt(frt, 10)
		firstMarkerElem.innerHTML = firstMarkerVal
		secondMarkerVal = document.getElementById(`marker${secondMarkerNum}Val`).innerHTML
	} else {
		firstMarkerVal = document.getElementById(`marker${firstMarkerNum}Val`).innerHTML
		secondMarkerVal = parseInt(frt, 10)
		secondMarkerElem.innerHTML = secondMarkerVal
	}

	if (firstMarkerVal != 0 && secondMarkerVal != 0) {
		var delta = parseInt(secondMarkerVal) - parseInt(firstMarkerVal)
		deltaElem = document.getElementById(`deltaVal${firstMarkerNum}${secondMarkerNum}`)
		deltaElem.innerHTML = delta
	}

}


function create_highchart(id, chartData, containerDiv = 'container') {
	console.log(id, chartData)
	// chart = new Highcharts.chart()

	chart = Highcharts.chart(containerDiv, {

		chart: {
			// type: 'bar'
			// zoomKey:'alt',
			zoomType: 'x',
			panKey: 'ctrl',
			panning: true,
			events: {
				click: function (e) {
					if (!e.shiftKey && !e.ctrlKey) return
					let chart = this;
					let xAxis = chart.xAxis[0];
					let xValue = xAxis.toValue(this.mouseDownX);

					let clickX = 0;
					if (markerCnt % 2 == 0)
						colorCnt = markerCnt % 10
					else
						colorCnt = (markerCnt - 1) % 10
					markerColor = Highcharts.getOptions().colors[colorCnt]
					markerCnt++
					create_marker_line(markerCnt, xValue, markerColor)

					xAxis.addPlotLine({
						value: xValue,
						cursor: 'pointer',
						color: markerColor,
						width: 1,
						label: {
							rotation: 90,
							text: `M${markerCnt}`,
							className: "markerLabel markerLabel" + markerCnt
						},
						zIndex: 99,
						className: `marker marker${markerCnt}Line`,
						dashStyle:'ShortDash',
						events: {
							mousedown: function (e) {
								chart.clickX = e.pageX;
								chart.activePlotLine = this;
							}
						}
					});

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

	charts[id]=chart

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
	create_highchart(RTT_CHART_ID, chartData,RTT_CHART_ID)



	return

}

function create_mode_chart(renderFlag) {
	console.log('creating modechanchart')
	let modeRxData = []
	let modeTxData = []

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
	create_highchart(MODE_CHART_ID, chartData,MODE_CHART_ID)


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
	create_highchart(CHAN_CHART_ID, chartData,CHAN_CHART_ID)


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
			findNearestPointBy: 'xy',
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
			findNearestPointBy: 'xy',
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
			findNearestPointBy: 'xy',
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
		findNearestPointBy: 'xy',
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
		findNearestPointBy: 'xy',
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

	create_highchart(TIMELINE_CHART_ID, chartData,TIMELINE_CHART_ID)

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

	$(document).on("click", ".removeMkrBtnClass", function (event) {
		// console.log("clicked",event)
		// console.log($(this))
		parentRow = $(this).parent()
		id = parentRow.attr('id').split('-')
		$(`.marker${id[1]}Line`).remove()
		$(`.marker${id[2]}Line`).remove()
		$(`.markerLabel${id[1]}`).remove()
		$(`.markerLabel${id[2]}`).remove()
		// console.log("parent", parentRow.attr('id'))
		parentRow.remove()

	});
	$(document).on("click", "#removeAllMarkers", function (event) {
		// console.log("clicked",event)
		// console.log($(this))
		$('.marker').remove()
		$('.markerLabel').remove()
	});

	document.getElementById('container')
		.addEventListener(
			'mousemove',
			function (e) {
				if (chart.activePlotLine) {
					chart.activePlotLine.svgElem.translate(e.pageX - chart.clickX, 0);
				}
			}
		);

	document.addEventListener(
		'mouseup',
		function (e) {
			if (chart.activePlotLine) {
				chart.activePlotLine = false;
			}
		}
	);



	// var mytabs = document.getElementsByClassName()



}


