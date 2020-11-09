

console.log("jsonData", jsonData)
RTT_CHART_ID = 'rtt'
MODE_CHART_ID = 'mode'
CHAN_CHART_ID = 'chan'
TIMELINE_CHART_ID = 'timeline'
BUFFER_CHART_ID = "buffer"
CLTIMING_CHART_ID = "cltiming"
CLTIMINGS_CHART_ID = "cltimings"
TARGET2TXPHR_CHART_ID = "target2txphr"
TXEND2RXSTART_CHART_ID = "txend2rxstart"
RXEND2TARGETTIME_CHART_ID = "rxend2targettime"
RXEND2TXTIME_CHART_ID = "rxend2txtime"
TXCALL2TARGETTIME_CHART_ID = "txcall2targettime"
RXEND2TXCALL_CHART_ID = "rxend2txcall"
RXCALL2AFTERRX_CHART_ID = "rxcall2afterrx"
CL_DUR_CHART_ID = "cl_dur"

// types of charts
charts = {
	"rtt": {},
	"cltiming": {},
	"cltimings": {},
	"timeline": {},
	"buffer": {},
	'chan': {},
	'mode': {}
};

// datasets for different charts
datasets = {
	"rtt": [],
	"cltiming": [],
	"cltimings": [],
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
	'buffer': {
		"chartTitle": "Buffer Stats",
		"xAxisType": 'category',
		"xAxisTitle": "Owner",
		"yAxisTitle": "Count",
		// "yAxisTitle2": "",
		// "yAxis2Max": 1,
		// "thTitle"    : "Max Power",
		// "thValue"    : "13"

	},
	'buffer2': {
		"chartTitle": "Buffer Management",
		"xAxisType": 'linear',
		"xAxisTitle": "Timestamp in usecs",
		"yAxisTitle": "Buffer",
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
	'cltiming': {
		"chartTitle": "CL Timing Summary Report",
		"xAxisType": 'linear',
		"xAxisTitle": "Timestamp in usecs",
		"yAxisMax": 3,
		"yAxisMin": -3,
		// "yAxisTitle": "",
		// "yAxisTitle2": "",
		// "yAxis2Max": ,
		// "thTitle"    : "Max Power",
		// "thValue"    : "13"

	},
	'cltiming': {
		"chartTitle": "CL",
		"xAxisType": 'linear',
		"xAxisTitle": "Timestamp in usecs",
		// "yAxisMax": 3,
		// "yAxisMin": -3,
		// "yAxisTitle": "",
		// "yAxisTitle2": "",
		// "yAxis2Max": ,
		// "thTitle"    : "Max Power",
		// "thValue"    : "13"

	},
	"target2txphr": {
		"chartTitle": "Target 2 tx PHR",
		"xAxisType": 'linear',
		"xAxisTitle": "target2txphr in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"txend2rxstart": {
		"chartTitle": "txend2rxstart",
		"xAxisType": 'linear',
		"xAxisTitle": "txend2rxstart in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"rxend2targettime": {
		"chartTitle": "rxend2targettime",
		"xAxisType": 'linear',
		"xAxisTitle": "rxend2targettime in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"rxend2txtime": {
		"chartTitle": "rxend2txtime",
		"xAxisType": 'linear',
		"xAxisTitle": "rxend2txtime in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"txcall2targettime": {
		"chartTitle": "txcall2targettime",
		"xAxisType": 'linear',
		"xAxisTitle": "txcall2targettime in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"rxend2txcall": {
		"chartTitle": "rxend2txcall",
		"xAxisType": 'linear',
		"xAxisTitle": "rxend2txcall in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"rxcall2afterrx": {
		"chartTitle": "rxcall2afterrx",
		"xAxisType": 'linear',
		"xAxisTitle": "rxcall2afterrx in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"cl_dur": {
		"chartTitle": "cl_dur",
		"xAxisType": 'linear',
		"xAxisTitle": "cl_dur in msecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

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
		case CLTIMING_CHART_ID:
			create_cltiming_chart(renderFlag);
			break;
		case CLTIMINGS_CHART_ID:
			create_cltimings_chart(renderFlag);
			break;
		case BUFFER_CHART_ID:
			create_buffer_chart(renderFlag);
			break;
		default:
			alert("Improper chart type " + chartId + " for ");
	}

}

var markerCnt = 0

function create_marker_line(markerNum, frt, markerColor) {

	var markerListDiv = document.getElementById('markersList')
	var firstMarkerNum = 0
	var secondMarkerNum = 0;
	var firstMarkerElem, secondMarkerElem;
	var firstMarkerVal = 0, secondMarkerVal = 0;

	/* create the marker div */
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
var redrawEnabled = true;

function create_highchart(id, chartData, containerDiv = 'container', annotations_arr = []) {
	console.log(id, chartData)

	chart = Highcharts.chart(containerDiv, {
		credits: {
			enabled: false
		},
		boost: {
			// enabled: false,
			// useGPUTranslations: true,
			// allowForce:true,
			// usePreallocated:true,
			// useAlpha:falses
		},

		chart: {
			// type: 'bar'
			// zoomKey:'alt',
			zoomType: 'x',
			panKey: 'ctrl',

			panning: true,

			events: {
				// load: function () {
				// 	const myChart = this;

				// 	console.log("loaded")

				// },
				// render: function () {
				// 	// console.log("rendered")
				// 	const myChart = this;

				// },
				redraw: function (event) {
					var extremes = this.xAxis[0].getExtremes();
					var border = 35942400000;
					var border = 60000000;
					var boostEnabled;

					var diff = extremes.userMax - extremes.userMin
					if (Number.isNaN(diff))
						diff = extremes.max - extremes.min
					boostEnabled = diff < border ? 0 : 1

					if (redrawEnabled) {
						redrawEnabled = false
						this.update({
							boost: {
								enabled: boostEnabled
							},
							// plotOptions: {
							//   series: {
							// 	boostThreshold: boostEnabled
							//   }
							// }
						});
						redrawEnabled = true
					}
				},
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
						dashStyle: 'ShortDash',
						events: {
							mousedown: function (e) {
								chart.clickX = e.pageX;
								chart.activePlotLine = this;
							}
						}
					});

				}
			}

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
			crosshair: {
				enabled: true,
				snap: chartOptions[id].xAxisType == 'category' ? true : false,
			},
		},

		yAxis: [{ // Primary yAxis
			// visible:id==TIMELINE_CHART_ID? false:trues,
			labels: {
				enabled: id == TIMELINE_CHART_ID || id == CLTIMING_CHART_ID ? false : true,
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


			},
			max: chartOptions[id].yAxis2Max ? chartOptions[id].yAxis2Max : null,
			// const a = { ...(condition && {b: 1}) // if condition is true 'b' will be added. }

			opposite: true
		}],

		series: chartData,
		annotations: annotations_arr

	});

	charts[id] = chart

}


function create_rtt_chart(renderFlag) {

	if (!jsonData.hasOwnProperty('rttJson')) return;

	console.log('creating RTT')
	let freqData = []
	let pdfData = []
	let cdfData = []
	let x_data = []
	jsonData.rttJson.forEach(item => {
		freqData.push({ x: item.diff, y: item.freq })
		pdfData.push({ x: item.diff, y: item.pdf })
		cdfData.push({ x: item.diff, y: item.cdf })
	});

	chartData = [
		/* count */
		{
			type: "column",
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
	create_highchart(RTT_CHART_ID, chartData, RTT_CHART_ID)



	return

}

function create_mode_chart(renderFlag) {
	if (!jsonData.hasOwnProperty('modeTxJson')) return;

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
		/* Mode Rx */
		{
			type: "column",
			name: "ModeRx",
			data: modeRxData,
			color: Highcharts.getOptions().colors[7]
		},
		/* Mode Tx */
		{
			type: "column",
			name: "ModeTx",
			data: modeTxData,
			color: Highcharts.getOptions().colors[3]
		},

	]
	create_highchart(MODE_CHART_ID, chartData, MODE_CHART_ID)

}
function create_chan_chart(renderFlag) {
	if (!jsonData.hasOwnProperty('chanTxJson')) return;

	console.log('creating chanchanchart')
	let chanRxData = []
	let chanTxData = []

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
		/* Chan Rx */
		{
			type: "column",
			name: "Chan Rx",
			data: chanRxData,
			color: Highcharts.getOptions().colors[7]
		},
		/* Chan Tx */
		{
			type: "column",
			name: "Chan Tx",
			data: chanTxData,
			color: Highcharts.getOptions().colors[3]
		},

	]
	create_highchart(CHAN_CHART_ID, chartData, CHAN_CHART_ID)

}

function create_buffer_chart(renderFlag) {
	if (!jsonData.hasOwnProperty('buffer_Json')) return;

	console.log('creating buffer summary chart')
	let bufClaimData = []
	let bufRelData = []
	let bufLeakData = []
	let chartData = []

	jsonData.buffer_summaryJson.forEach(item => {
		bufClaimData.push({ name: item.owner, y: item.buf_claim })
		bufRelData.push({ name: item.owner, y: item.buf_release })
		bufLeakData.push({ name: item.owner, y: item.buf_leak })
	});

	chartData = [
		/* claims */
		{
			type: "column",
			name: "Buff Claim",
			dataLabels: {
				enabled: true,
				color: Highcharts.getOptions().colors[7]
			},
			data: bufClaimData,
			color: Highcharts.getOptions().colors[7]
		},
		/* release */
		{
			type: "column",
			name: "Buff release",
			dataLabels: {
				enabled: true,
				color: Highcharts.getOptions().colors[3]
			},
			data: bufRelData,
			color: Highcharts.getOptions().colors[3]
		},
		/* leaks */
		{
			type: "column",
			name: "Buff Leaks",
			dataLabels: {
				enabled: true,
				color: Highcharts.getOptions().colors[5]
			},
			data: bufLeakData,
			color: Highcharts.getOptions().colors[5]
		},

	]
	create_highchart(BUFFER_CHART_ID, chartData, BUFFER_CHART_ID)

	console.log('creating buffer alloc')
	chartData = []
	buf_colors = {
		'CL': '#ff0000',
		'FH': '#00ff00',
		'RXBCON': '#0000ff',
		'ALINK': '#009999',
		'MACMGR': '#003f5c',
		"LMMGR": "#444e86",
		"TXBCON": "#955196",
		"SA": "#dd5182",
		"ELG": "#ff6e54",
		"TXBCAST": "#ffa600",
	}

	if (!jsonData.hasOwnProperty('buffer_Json')) {
		return
	}

	/* Buffer allocated area*/
	jsonData.buffer_Json.forEach(item => {
		chartData.push({
			type: 'area',
			findNearestPointBy: 'xy',

			data: [
				[item.frt_dec, 0],
				[item.frt_dec, item.buffer_dec],
				{
					x: item.frt_dec + item.frt_diff / 2.0,
					y: item.buffer_dec,
					// dataLabels: { enabled: true, format: '{x} x {y}' }
				},
				[item.rel_frt, item.buffer_dec],
				[item.rel_frt, 0],

				// [item.ts_txend, 1],

			],
			states: {
				inactive: {
					opacity: 0.6
				}
			},

			zIndex: 5,
			name: item.owner,

			showInLegend: false,
			color: buf_colors[item.owner],
			lineWidth: 0.25,
			fillOpacity: 0.1,
			tooltip: {
				// split: true,
				// followPointer: true,
				useHTML: true,
				headerFormat: '<span style="color: {series.color}">{series.name} </span>: 0x' + item.buffer_dec.toString(16),
				pointFormat: '<br><span>claimedFRT: ' + item.frt_dec + '</span><br> releasedFRT:' + item.rel_frt + '<br>Dur: ' + item.frt_diff + " usec"
			},
		})
	});

	create_highchart(BUFFER_CHART_ID + "2", chartData, BUFFER_CHART_ID + "2")

}

function create_cltimings_chart(renderFlag) {
	let freqData = []
	let pdfData = []
	let cdfData = []
	let chartData = []
	console.log('creating cltimings')

	for (const [key, value] of Object.entries(jsonData)) {
		freqData = []
		pdfData = []
		cdfData = []
		chartData = []
		let id = ''

		if (!key.startsWith('cltimings_'))
			continue;

		id = key.slice(10, -4)

		jsonData[key].forEach(item => {
			freqData.push({ x: item[id], y: item.freq })
			pdfData.push({ x: item[id], y: item.pdf })
			cdfData.push({ x: item[id], y: item.cdf })
		})

		chartData = [
			/* count */
			{
				type: "column",
				name: "Freq",
				data: freqData,
				color: Highcharts.getOptions().colors[0]
			},
			/* pdf */
			{
				type: "line",
				name: "PDF",
				yAxis: 1,
				data: pdfData,
				color: Highcharts.getOptions().colors[3]
			},
			/* cdf */
			{
				type: "line",
				name: "CDF",
				yAxis: 1,
				data: cdfData,
				color: Highcharts.getOptions().colors[2]
			},
		]

		create_highchart(id, chartData, id)

	}
}

function create_cltiming_chart(renderFlag) {
	if (!jsonData.hasOwnProperty('cltimingJson')) return;

	console.log("cltiming", jsonData.cltimingJson)
	let chartData = []
	tx_dur = 2000

	points_dic = jsonData.cltimingJson.points_dic
	rx_dur = points_dic['rxEnd'] - (points_dic['rxPHR'])
	txdiff = points_dic['TxPHR1'] - points_dic['TargetTx1']
	/* POLL ACK DATA */
	chartData.push({
		type: 'area',
		findNearestPointBy: 'xy',
		data: [
			[points_dic.TxPHR1, 0],
			[points_dic.TxPHR1, 0.5],
			[points_dic.TxPHR1 + tx_dur, 0.5],
			[points_dic.TxPHR1 + tx_dur, 0],
		],
		enableMouseTracking: false,
		zIndex: 5,
		states: {
			inactive: {
				opacity: 1
			}
		},
		name: "POLL",
		showInLegend: false,
		color: '#E9967A',
		lineWidth: 2,
		fillOpacity: 0.6,
		tooltip: {
			enabled: false
		},
	}, {
		type: 'area',
		findNearestPointBy: 'xy',
		data: [
			[points_dic.rxPHR - 0, 0],
			[points_dic.rxPHR - 0, -0.5],
			[points_dic.rxPHR - 0 + rx_dur, -0.5],
			[points_dic.rxPHR - 0 + rx_dur, 0],
		],
		name: "ACK",
		enableMouseTracking: false,

		zIndex: 5,
		states: {
			inactive: {
				opacity: 1
			}
		},
		showInLegend: false,
		color: '#8FBC8F',
		lineWidth: 2,
		fillOpacity: 0.6,
		tooltip: {
			enabled: false
		},

	}, {
		type: 'area',
		findNearestPointBy: 'xy',
		data: [
			[points_dic.TxPHR2, 0],
			[points_dic.TxPHR2, 0.5],
			[points_dic.TxPHR2 + tx_dur + 500, 0.5],
			[points_dic.TxPHR2 + tx_dur + 500, 0],
		],
		enableMouseTracking: false,

		zIndex: 5,
		states: {
			inactive: {
				opacity: 1
			}
		},
		name: "Data",
		showInLegend: false,
		color: '#E9967A',
		lineWidth: 2,
		fillOpacity: 0.6,
		tooltip: {
			enabled: false
		},
	})

	/* lollipop */
	let lollipopData = []
	let annotations = []

	value_levels = {
		"WrapperCall1": -2,
		"WrapperReturn": 2,
		"TargetTx1": -2,
		"TxPHR1": -2,
		"EndTxTime": -2,
		"rxStart_beforeCall": 2,
		"rxStart_afterCall": 2,
		"rxPHR": 2,
		"rxEnd": -2,
		"WrapperCall2": 2,
		"TargetTx2": -2,
		"TxPHR2": -2,
	}

	cnt = 0
	for (const [key, value] of Object.entries(jsonData.cltimingJson.points_dic)) {
		// push lollipops data
		lollipopData.push({
			x: value,
			y: jsonData.cltimingJson.levels_dic[key],
			color: jsonData.cltimingJson.colors_dic[key],
			id: key,
			name: jsonData.cltimingJson.names_label_dic[key],
		})

		// push annotations for lollipop labels
		annotations.push({
			labelOptions: {
				backgroundColor: 'rgba(255,255,0,0.3)',
				verticalAlign: jsonData.cltimingJson.levels_dic[key] < 0 ? 'top' : 'bottom',
				// y: 15
				distance: 10,
			},
			labels: [{
				point: key,
				text: jsonData.cltimingJson.names_label_dic[key]
			}]
		})
		// push annotations for arrows and its labels
		annotations.push({
			draggable: '',

			shapes: [{
				fill: 'none',
				stroke: 'red',
				strokeWidth: 1,
				dashStyle: 'LongDash',
				type: 'path',
				points: [
					{
						x: jsonData.cltimingJson.arrows_x[cnt].x1,
						y: jsonData.cltimingJson.arrows_x[cnt].y,
						xAxis: 0,
						yAxis: 0
					}, {
						x: jsonData.cltimingJson.arrows_x[cnt].x2,
						y: jsonData.cltimingJson.arrows_x[cnt].y,
						xAxis: 0,
						yAxis: 0
					}],
				// markerEnd: 'arrow',
				// markerStart:'diamond',

			}],
			labelOptions: {
				backgroundColor: 'rgba(255,255,255,0.4)',
				borderColor: 'rgba(0,0,0,0)',
				style: {
					color: "black",
				},
				verticalAlign: value_levels[key] < 0 ? 'bottom' : 'top',
				y: value_levels[key],
			},
			labels: [{
				point: {
					x: (jsonData.cltimingJson.arrows_x[cnt].x1 + jsonData.cltimingJson.arrows_x[cnt].x2) / 2,
					y: jsonData.cltimingJson.arrows_x[cnt].y,
					xAxis: 0,
					yAxis: 0
				},
				text: jsonData.cltimingJson.val_texts[cnt],
				allowOverlap: true,
				padding: 2
			}]
		})

		cnt++
	}
	/* for min/max/avg */
	annotations.push({
		//undefined - delayed value is inherited from plotOptions
		labelOptions: {
			backgroundColor: 'rgba(0,0,0,0.8)',
		},
		labels: [{
			point: {
				x: 100, y: 0,
			},
			text: "min/max/avg"
		}]
	})


	chartData.push({
		type: 'lollipop',
		findNearestPointBy: 'xy',
		data: lollipopData,

		zIndex: 7,
		states: {
			inactive: {
				opacity: 1
			}
		},

		showInLegend: false,
		// color: '#8FBC8F',
		connectorWidth: 2,
		fillOpacity: 0.6,
		toolTip: {
			enabled: false
		},
		enableMouseTracking: false,

	})

	create_highchart(CLTIMING_CHART_ID, chartData, CLTIMING_CHART_ID, annotations_arr = annotations)

}

function create_timeline_chart(renderFlag) {
	if (!jsonData.hasOwnProperty('timeline_clStartEndJson')) return;

	console.log('creating timeline chart')
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
				[item.ts_txend, 0],

				// [item.ts_txend, 1],

			],
			states: {
				inactive: {
					opacity: 0.8
				}
			},

			zIndex: 5,
			name: "TX",
			showInLegend: false,
			color: item.color,
			tooltip: {
				split: true,
				useHTML: true,
				headerFormat: '<span style="color: {series.color}">{series.name}</span>: ',
				pointFormat: '<span>FRT: {point.x}</span><br>' + item.hoverinfo
			},
			turboThreshold: 0,

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
				[item.ts_rxend, 0]
				// [item.ts_rxend, -1],

			],
			turboThreshold: 0,

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
			// findNearestPointBy: 'xy',
			data: [
				[item.clstart, 0], [item.clstart, 3],
				{
					x: item.clstart + item.cldiff / 2.0,
					y: 3,
					dataLabels: { enabled: true, format: item.hoverinfo }
				},
				[item.clend, 3],
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
			turboThreshold: 0,

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

	create_highchart(TIMELINE_CHART_ID, chartData, TIMELINE_CHART_ID)
	console.log('creating timeline chart END')


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

	if (Object.keys(charts[graphId]).length == 0)
		drawChart(graphId, true)

}

window.onload = function () {
	console.log("document ready")

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

	refreshIntv = $('#refreshIntvDur').val() * $('#refreshIntUnit').val() * 1000
	console.log("refreshIntv", refreshIntv)
	if (refreshIntv > 0) {
		refreshTimer = setTimeout(function () {
			location.reload();
		}, refreshIntv);
	}

	$(document).on("click", "#removeAllMarkers", function (event) {
		$('.marker').remove()
		$('.markerLabel').remove()
	});

	$(document).on("change", "#refreshIntvDur", function (event) {
		refreshIntv = $('#refreshIntvDur').val() * $('#refreshIntUnit').val() * 1000
		if (typeof refreshTimer !== 'undefined') clearTimeout(refreshTimer);
		if (refreshIntv > 0) {
			refreshTimer = setTimeout(function () {
				location.reload();
			}, refreshIntv);
		}
	});

}


