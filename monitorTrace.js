console.log("Monitoring on Node IP ", nodeip);
console.log("Monitoring on Node File ", nodefile);
console.log("jsonData", jsonData);
RTT_CHART_ID = 'rtt';
MODE_CHART_ID = 'mode';
CHAN_CHART_ID = 'chan';
TIMELINE_CHART_ID = 'timeline';
BUFFER_CHART_ID = "buffer";
CLTIMING_CHART_ID = "cltiming";
CLTIMINGS_CHART_ID = "cltimings";
TARGET2TX_CHART_ID = "target2tx";
TXEND2RXSTART_CHART_ID = "txend2rxstart";
RXEND2TARGETTIME_CHART_ID = "rxend2targettime";
RXEND2TXTIME_CHART_ID = "rxend2txtime";
TXCALL2TARGETTIME_CHART_ID = "txcall2targettime";
TXCALL2AFTERTX_CHART_ID = "txcall2aftertx";
TXCALL2TX_CHART_ID = "txcall2tx";
RXEND2TXCALL_CHART_ID = "rxend2txcall";
RXCALL2AFTERRX_CHART_ID = "rxcall2afterrx";
AFTERRX2RX_CHART_ID = "afterrx2rx"
TXRXDRIFT_CHART_ID = "txrxdrift"
RXTXDRIFT_CHART_ID = "rxtxdrift"
CL_DUR_CHART_ID = "cl_dur";
THRESHOLD_STEP = 4;
THRESHOLD_GAP = 2;

/*  types of charts */
charts = {
	"rtt": {},
	"cltiming": {},
	"cltimings": {},
	"timeline": {},
	"buffer": {},
	'chan': {},
	'mode': {}
};

/*  datasets for different charts */
datasets = {
	"rtt": [],
	"cltiming": [],
	"cltimings": [],
	"timeline": [],
	"buffer": [],
	'modechan': [],
};

/*  chart options for different charts */
chartOptions = {
	'rtt': {
		"chartTitle": "RTT between clData.get and clData.cnf",
		"xAxisType": 'linear',
		"xAxisTitle": "RTT in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,
		/*  "thTitle"    : "Max Power", */
		/*  "thValue"    : "13" */

	},
	'mode': {
		"chartTitle": "Mode Usage",
		"xAxisType": 'category',
		"xAxisTitle": "Modes",
		"yAxisTitle": "Count",
		/*  "yAxisTitle2": "PDF/CDF", */
		/*  "yAxis2Max": 1, */
		/*  "thTitle"    : "Max Power", */
		/*  "thValue"    : "13" */

	},
	'chan': {
		"chartTitle": "Channel Usage",
		"xAxisType": 'category',
		"xAxisTitle": "Channel",
		"yAxisTitle": "Count",
		/*  "yAxisTitle2": "", */
		/*  "yAxis2Max": 1, */
		/*  "thTitle"    : "Max Power", */
		/*  "thValue"    : "13" */

	},
	'buffer': {
		"chartTitle": "Buffer Stats",
		"xAxisType": 'category',
		"xAxisTitle": "Owner",
		"yAxisTitle": "Count",
		/*  "yAxisTitle2": "", */
		/*  "yAxis2Max": 1, */
		/*  "thTitle"    : "Max Power", */
		/*  "thValue"    : "13" */

	},
	'buffer2': {
		"chartTitle": "Buffer Management",
		"xAxisType": 'linear',
		"xAxisTitle": "Timestamp in usecs",
		"yAxisTitle": "Buffer",
		/*  "yAxisTitle2": "", */
		/*  "yAxis2Max": 1, */
		/*  "thTitle"    : "Max Power", */
		/*  "thValue"    : "13" */

	},
	'timeline': {
		"chartTitle": "Timeline Visualiser (TimeOffset=" + jsonData['timing_offset'] + ")",
		"xAxisType": 'linear',
		"xAxisTitle": "Timestamp in usecs",
		"yAxisMax": (THRESHOLD_GAP + THRESHOLD_STEP) * TOTAL_NODES,
		"yAxisMin": 0,
		/*  "yAxisTitle": "", */
		/*  "yAxisTitle2": "", */
		/*  "yAxis2Max": , */
		/*  "thTitle"    : "Max Power", */
		/*  "thValue"    : "13" */

	},
	'cltiming': {
		"chartTitle": "CL Timing Summary Report",
		"xAxisType": 'linear',
		"xAxisTitle": "Timestamp in usecs",
		"yAxisMax": 3,
		"yAxisMin": -3,
		/*  "yAxisTitle": "", */
		/*  "yAxisTitle2": "", */
		/*  "yAxis2Max": , */
		/*  "thTitle"    : "Max Power", */
		/*  "thValue"    : "13" */

	},

	"target2tx": {
		"chartTitle": "Target Time to TX preamble",
		"xAxisType": 'linear',
		"xAxisTitle": "target2tx in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"txend2rxstart": {
		"chartTitle": "txend to RX start Call",
		"xAxisType": 'linear',
		"xAxisTitle": "txend2rxstart in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"rxend2targettime": {
		"chartTitle": "RX end to Target Tx Time",
		"xAxisType": 'linear',
		"xAxisTitle": "rxend2targettime in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"rxend2txtime": {
		"chartTitle": "RX end to TX PHR time",
		"xAxisType": 'linear',
		"xAxisTitle": "rxend2txtime in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"txcall2targettime": {
		"chartTitle": "TX Wrapper call to Target Time",
		"xAxisType": 'linear',
		"xAxisTitle": "txcall2targettime in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"txcall2aftertx": {
		"chartTitle": "TX Wrapper call to Wrapper Return",
		"xAxisType": 'linear',
		"xAxisTitle": "txcall2afterTx in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,
	},
	"txcall2tx": {
		"chartTitle": "TX Wrapper call to Tx Preamble",
		"xAxisType": 'linear',
		"xAxisTitle": "txcall2tx in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,
	},

	"rxend2txcall": {
		"chartTitle": "RX End to TX Call",
		"xAxisType": 'linear',
		"xAxisTitle": "rxend2txcall in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"rxcall2afterrx": {
		"chartTitle": "RX CAL duration",
		"xAxisType": 'linear',
		"xAxisTitle": "rxcall2afterrx in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},
	"afterrx2rx": {
		"chartTitle": "After Rx to Rx Preamble",
		"xAxisType": 'linear',
		"xAxisTitle": "afterrx2rx in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,
	},
	"txrxdrift": {
		"chartTitle": "Tx to Rx Drift",
		"xAxisType": 'linear',
		"xAxisTitle": "txrxdrift in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,
	},
	"rxtxdrift": {
		"chartTitle": "Rx to Tx Drift",
		"xAxisType": 'linear',
		"xAxisTitle": "rxtxdrift in usecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,
	},
	"cl_dur": {
		"chartTitle": "CL Duration",
		"xAxisType": 'linear',
		"xAxisTitle": "cl_dur in msecs",
		"yAxisTitle": "Count",
		"yAxisTitle2": "PDF/CDF",
		"yAxis2Max": 1,

	},

};

THRESHOLDS = [];
for (i = 0; i < (TOTAL_NODES); i++) {
	THRESHOLDS.push(THRESHOLD_GAP + i * THRESHOLD_STEP + THRESHOLD_GAP * i);
}


function drawChart(chartId, tabName, renderFlag) {

	switch (chartId) {
		case RTT_CHART_ID:
			create_rtt_chart(tabName, renderFlag);
			break;
		case MODE_CHART_ID:
			create_mode_chart(tabName, renderFlag);
			break;
		case CHAN_CHART_ID:
			create_chan_chart(tabName, renderFlag);
			break;
		case TIMELINE_CHART_ID:
			create_timeline_chart(tabName, renderFlag);
			break;
		case CLTIMING_CHART_ID:
			create_cltiming_chart(tabName, renderFlag);
			break;
		case CLTIMINGS_CHART_ID:
			create_cltimings_chart(tabName, renderFlag);
			break;
		case BUFFER_CHART_ID:
			create_buffer_chart(tabName, renderFlag);
			break;
		default:
			alert("Improper chart type " + chartId + " for ");
	}

}

function display_alert(type = 'warning', msg = "") {
	var alertDivStr = '<div class="alert alert-' + type + ' alert-dismissible fade show" role="alert">' + msg + '<button type = "button" class="close" data-dismiss="alert" aria- label="Close" ><span aria-hidden="true">&times;</span></button ></div>';
	$('#alertDiv').html(alertDivStr);
}

var markerCnt = 0;

function create_marker_line(tabName, markerNum, frt, markerColor, id) {

	var markerListDiv = document.getElementById('markersList' + '-' + tabName);
	var firstMarkerNum = 0;
	var secondMarkerNum = 0;
	var firstMarkerElem, secondMarkerElem;
	var firstMarkerVal = 0, secondMarkerVal = 0;

	/* create the marker div */
	if (markerNum % 2 != 0) {
		firstMarkerNum = markerNum;
		secondMarkerNum = markerNum + 1;
		lineHtml = `<div class="marker col-sm-6 " style="border:2px solid ${markerColor}"id="divMarkerVal-${firstMarkerNum}-${secondMarkerNum}">
			<div class="row">
				<div class="col-sm-3"> M${firstMarkerNum}: <span name="marker1" class="markerVal" id="marker${firstMarkerNum}Val"> </span></div>
				<div class="col-sm-3"> M${secondMarkerNum}: <span name="marker2" class="markerVal" id="marker${secondMarkerNum}Val"> </span></div>
				<div class="col-sm-6"> Delta: <span class= "deltaVal" id="deltaVal${firstMarkerNum}${secondMarkerNum}"> </span>
				<i style="color:${markerColor};" class="fas fa-backspace fs-lg removeMkrBtnClass float-right" id="removeMkrBtn${firstMarkerNum}${secondMarkerNum}"></i></div>
			</div>
		</div>`;

		markerListDiv.innerHTML = markerListDiv.innerHTML + lineHtml;
	} else {
		firstMarkerNum = markerNum - 1;
		secondMarkerNum = markerNum;
	}

	firstMarkerElem = document.getElementById(`marker${firstMarkerNum}Val`);
	secondMarkerElem = document.getElementById(`marker${secondMarkerNum}Val`);

	if (markerNum % 2 != 0) {
		firstMarkerVal = parseInt(frt, 10);
		firstMarkerElem.innerHTML = firstMarkerVal;
		secondMarkerVal = document.getElementById(`marker${secondMarkerNum}Val`).innerHTML;
	} else {
		firstMarkerVal = document.getElementById(`marker${firstMarkerNum}Val`).innerHTML;
		secondMarkerVal = parseInt(frt, 10);
		secondMarkerElem.innerHTML = secondMarkerVal;
	}

	if (firstMarkerVal != 0 && secondMarkerVal != 0) {
		var delta = parseInt(secondMarkerVal) - parseInt(firstMarkerVal);
		var signStr = Math.sign(delta) == -1 ? "-" : "";
		var deltaElem = document.getElementById(`deltaVal${firstMarkerNum}${secondMarkerNum}`);
		var deltaSec = 0;
		var deltaMs = 0;
		var deltaUs = 0;
		var deltaStr = delta + ' usec (';
		var deltaMsStr = '';
		var deltaSecStr = '';
		var deltaUsStr = delta + 'usec ';
		var extra = 0;

		delta = Math.abs(delta);
		if (delta > 1000) {
			deltaMs = parseInt(delta / 1000, 10);
			deltaUs = delta % 1000;
			deltaMsStr = deltaMs + "ms ";
			extra = 1;
		}

		if (deltaMs > 1000) {
			deltaSec = parseInt(deltaMs / 1000, 10);
			deltaMs = deltaMs % 1000;
			deltaSecStr = deltaSec + " sec ";
			deltaMsStr = deltaMs + "ms ";
		}
		if (deltaUs <= 0) {
			deltaUs = '';
			deltaUsStr = '';
		} else {
			deltaUsStr = deltaUs + "us";
		}

		deltaStr = extra ? delta + " ( " + deltaSecStr + deltaMsStr + deltaUsStr + " )" : delta;
		deltaElem.innerHTML = signStr + deltaStr;
	}

}
var redrawEnabled = true;

function create_pie_highchart(id, chartData, dd_data = [], containerDiv = 'container', annotations_arr = []) {
	console.log(id, chartData, dd_data);
	var pie_colors = ["#44A9A8", "#F7A35C", "#90ed7d", "#f7a35c", "#e4d354", "#f45b5b", "#91e8e1"];

	chart = Highcharts.chart(containerDiv, {
		credits: {
			enabled: false
		},


		plotOptions: {
			pie: {
				/*    showInLegend: true, */
				dataLabels: {
					enabled: true,
					distance: -10,
					inside: true,
					format: '{point.name} {point.y}',
					crop: true,
					overflow: 'allow'
				},
				colors: pie_colors
			}
		},
		exporting: false,

		chart: {
			height: 150,
			backgroundColor: "transparent"
		},
		dataLabels: {
			/*  enabled: false */
		},

		title: false,

		legend: {
			verticalAlign: 'top',
		},
		tooltip: {
			headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
			pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b>'
		},



		series: chartData,
		drilldown: {
			series: dd_data,
		},
		/*  annotations: annotations_arr */

	});

}


function create_highchart(id, tabName, chartData, containerDiv = 'container', annotations_arr = []) {
	console.log(id, tabName, chartData);
	var zoomRatio = 1;

	zero_x_arr = [];

	/* define multiple offsets for timeline graph and 0s for others */
	for (i = 0; i < TOTAL_NODES; i++) {
		zero_x_arr.push(
			{

				value: id == "timeline" ? THRESHOLDS[i] : 0,
				width: 1,
				color: '#999',
				zIndex: 10
			});
	}

	chart = Highcharts.chart(containerDiv, {
		credits: {
			enabled: false
		},
		boost: {
			/*  enabled: false, */
			useGPUTranslations: true,
			/*  allowForce:true, */
			/*  usePreallocated:true, */
			seriesThreshold: 252,
			useAlpha: false
		},
		exporting: {
			sourceWidth: 1920,
			sourceHeight: 920,
		},

		chart: {
			/*  type: 'bar' */
			/*  zoomKey:'alt', */
			zoomType: 'x',
			panKey: 'ctrl',

			panning: true,

			events: {
				load: function (event) {
					const myChart = this;

					myChart.renderer.button('+', 30, 10)
						.attr({
							zIndex: 99,
						})
						.on('click', function () {
							var xMin = chart.xAxis[0].getExtremes().min;
							var xMax = chart.xAxis[0].getExtremes().max;
							delta = xMax - xMin;
							chart.xAxis[0].setExtremes(xMin + delta / 4, xMax - delta / 4);
						})
						.add();
					myChart.renderer.button('-', 60, 10)
						.attr({
							zIndex: 99,
						})
						.on('click', function () {
							var xMin = chart.xAxis[0].getExtremes().min;
							var xMax = chart.xAxis[0].getExtremes().max;
							delta = xMax - xMin;
							chart.xAxis[0].setExtremes(xMin - delta / 2, xMax + delta / 2);
						})
						.add();
					myChart.renderer.button('O', 90, 10)
						.attr({
							zIndex: 99
						})
						.on('click', function () {
							chart.zoomOut();
						})
						.add();

				},
				/*  render: function () { */
				/*  	 console.log("rendered") */
				/*  	const myChart = this; */

				/*  }, */
				redraw: function (event) {
					var extremes = this.xAxis[0].getExtremes();
					var border = 35942400000;
					var border = 60000000;
					var boostEnabled;

					var diff = extremes.userMax - extremes.userMin;
					if (Number.isNaN(diff))
						diff = extremes.max - extremes.min;
					boostEnabled = diff < border ? 0 : 1;

					if (redrawEnabled) {
						redrawEnabled = false;
						this.update({
							boost: {
								enabled: boostEnabled
							},
							/*  plotOptions: { */
							/*    series: { */
							/*  	boostThreshold: boostEnabled */
							/*    } */
							/*  } */
						});
						redrawEnabled = true;
					}
				},
				click: function (e) {
					if (!e.shiftKey && !e.ctrlKey) return;
					let chart = this;
					let xAxis = chart.xAxis[0];
					let xValue = xAxis.toValue(this.mouseDownX);

					let clickX = 0;
					if (markerCnt % 2 == 0)
						colorCnt = markerCnt % 10;
					else
						colorCnt = (markerCnt - 1) % 10;
					markerColor = Highcharts.getOptions().colors[colorCnt];
					markerCnt++;
					create_marker_line(tabName, markerCnt, xValue, markerColor, id);

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
						zIndex: 999,
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
			/*  headerFormat: '<span style="font-size:10px">{point.key}</span><table>', */
			/*  pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' + */
			/*  	'<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>', */
			/*  footerFormat: '</table>', */
			shared: true,
			/*  split:true, */
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
				zIndex: 999,
				enabled: true,
				snap: chartOptions[id].xAxisType == 'category' ? true : false,
			},
		},

		yAxis: [{ /*  Primary yAxis */
			/*  visible:id==TIMELINE_CHART_ID? false:trues, */
			labels: {
				enabled: id == TIMELINE_CHART_ID || id == CLTIMING_CHART_ID ? false : true,
				/*  format: '{value}°C', */
				/*  style: { */
				/*  	color: Highcharts.getOptions().colors[1] */
				/*  } */
			},
			/* zero cross */
			plotLines: zero_x_arr,
			title: {
				text: chartOptions[id].yAxisTitle,
				/*  style: { */
				/*  	color: Highcharts.getOptions().colors[1] */
				/*  } */
			},
			/*  max:  null, */
			max: chartOptions[id].yAxisMax ? chartOptions[id].yAxisMax : null,
			min: chartOptions[id].yAxisMin ? chartOptions[id].yAxisMin : null,

		}, { /*  Secondary yAxis */
			title: {
				text: chartOptions[id].yAxisTitle2 ? chartOptions[id].yAxisTitle2 : null,


			},
			max: chartOptions[id].yAxis2Max ? chartOptions[id].yAxis2Max : null,
			/*  const a = { ...(condition && {b: 1})  if condition is true 'b' will be added. } */

			opposite: true
		}],

		series: chartData,
		annotations: annotations_arr

	});

	charts[id] = chart;

}

function drawPieChart_cl_newend() {


	if (!jsonData.clstatsJson.hasOwnProperty('CL_NEW_END')) return;

	jsonData_clnewend = jsonData.clstatsJson.CL_NEW_END;
	if (Object.keys(jsonData_clnewend).length == 0) return;

	dd_clouts_data = [];
	for (const [key, value] of Object.entries(jsonData_clnewend.CL_NEW.drilldown.CL_OUT.drilldown)) {
		dd_clouts_data.push({
			name: key,
			y: value
		});
	}
	dd_clends_data = [];
	for (const [key, value] of Object.entries(jsonData_clnewend.CL_END.drilldown)) {
		dd_clends_data.push({
			name: key,
			y: value
		});
	}

	/*  create CL PIE CHART */
	chartData = [
		/* count */
		{
			type: "pie",
			name: "CL",
			/*  colorByPoint: true, */

			data: [
				{
					name: "CL NEW",
					y: jsonData_clnewend.CL_NEW.val,
					drilldown: "dd_cl_new",
					/*  color:'red', */
				},
				{
					name: "CL END",
					y: jsonData_clnewend.CL_END.val,
					drilldown: "dd_cl_end"
				},
			],
		},

	];
	dd_data = [
		{
			name: "CL NEW",
			type: 'pie',
			id: "dd_cl_new",
			data: [
				{
					name: "CL_OUT",
					y: jsonData_clnewend.CL_NEW.drilldown.CL_OUT.val,
					drilldown: 'dd_cl_out'
				},
				{
					name: "CL_IN",
					y: jsonData_clnewend.CL_NEW.drilldown.CL_IN
				},

			]
		}, {
			name: "CL_OUT",
			type: 'pie',
			id: 'dd_cl_out',
			data: dd_clouts_data

		},
		{
			name: "CL_END",
			type: 'pie',
			id: 'dd_cl_end',
			data: dd_clends_data

		}
	];
	create_pie_highchart("clpietotal", chartData, dd_data, 'clpietotal');

}

function drawPieChart_cl_data_reqresp() {

	if (!jsonData.clstatsJson.hasOwnProperty('CL_DATA_REQ_RESP')) return;

	cl_data_reqresp_stats = jsonData.clstatsJson.CL_DATA_REQ_RESP;
	if (Object.keys(cl_data_reqresp_stats).length == 0) return;

	dd_cldata_reqresp_data = [];
	for (const [key, value] of Object.entries(cl_data_reqresp_stats.CL_DATA_RESP.drilldown)) {
		dd_cldata_reqresp_data.push({
			name: key,
			y: value
		});
	}

	/*  create CL PIE CHART */
	chartData = [
		/* count */
		{
			type: "pie",
			name: "CL DATA",
			colorByPoint: true,
			data: [
				{
					name: "DATAREQ",
					y: cl_data_reqresp_stats.CL_DATA_REQ.val,

				},
				{
					name: "DATARESP",
					y: cl_data_reqresp_stats.CL_DATA_RESP.val,
					drilldown: "dd_cl_data_resp"
				},
			],
		},

	];
	dd_data = [
		{
			name: "DATARESP",
			type: 'pie',
			id: "dd_cl_data_resp",
			data: dd_cldata_reqresp_data
		}
	];
	create_pie_highchart("clpiedatareqresp", chartData, dd_data, 'clpiedatareqresp');

}
function drawPieChart_cl_tx_rx() {

	if (!jsonData.clstatsJson.hasOwnProperty('CL_TX_RX')) return;

	jsonData_cltxrx = jsonData.clstatsJson.CL_TX_RX;
	if (Object.keys(jsonData_cltxrx).length == 0) return;

	dd_cltx_data = [];
	for (const [key, value] of Object.entries(jsonData_cltxrx.CL_TX.drilldown)) {
		dd_cltx_data.push({
			name: key,
			y: value
		});
	}
	dd_clrx_data = [];
	for (const [key, value] of Object.entries(jsonData_cltxrx.CL_RX.drilldown)) {
		dd_clrx_data.push({
			name: key,
			y: value
		});
	}

	/*  create CL PIE CHART */
	chartData = [
		/* count */
		{
			type: "pie",
			name: "CL TX RX",
			colorByPoint: true,
			data: [
				{
					name: "TX",
					y: jsonData_cltxrx.CL_TX.val,
					drilldown: "dd_cl_tx"

				},
				{
					name: "RX",
					y: jsonData_cltxrx.CL_RX.val,
					drilldown: "dd_cl_rx"
				},
			],
		},

	];
	dd_data = [
		{
			name: "TX",
			type: 'pie',
			id: "dd_cl_tx",
			data: dd_cltx_data
		}, {
			name: "RX",
			type: 'pie',
			id: "dd_cl_rx",
			data: dd_clrx_data
		}
	];
	create_pie_highchart("clpietxrx", chartData, dd_data, 'clpietxrx');
}
function drawPieChart_cl_txdone() {

	if (!jsonData.clstatsJson.hasOwnProperty('CL_TXDONE')) return;

	jsonData_cltxdone = jsonData.clstatsJson.CL_TXDONE;
	if (Object.keys(jsonData_cltxdone).length == 0) return;


	dd_cltx_done = [];
	for (const [key, value] of Object.entries(jsonData_cltxdone.drilldown)) {
		dd_cltx_done.push({
			name: key,
			y: value
		});
	}


	/*  create CL PIE CHART */
	chartData = [
		/* count */
		{
			type: "pie",
			name: "CL TXDONE",
			colorByPoint: true,
			data: [
				{
					name: "TXDONE",
					y: jsonData_cltxdone.val,
					drilldown: "dd_cl_txdone"

				},

			],
		},

	];
	dd_data = [
		{
			name: "TX",
			type: 'pie',
			id: "dd_cl_txdone",
			data: dd_cltx_done
		}
	];
	create_pie_highchart("clpietxdone", chartData, dd_data, 'clpietxdone');

}

function drawPieChart() {
	if (!jsonData.hasOwnProperty('clstatsJson')) return;

	clstats = jsonData.clstatsJson;
	console.log('clstats ', clstats);

	/*  CL NEW END */
	drawPieChart_cl_newend();

	/*  CL DATA REQ RESP */
	drawPieChart_cl_data_reqresp();

	/* CL TX RX */
	drawPieChart_cl_tx_rx();

	/* CL TXDONE */
	drawPieChart_cl_txdone();

}



function create_rtt_chart(tabName, renderFlag) {

	if (!jsonData.hasOwnProperty('rttJson')) return;

	console.log('creating RTT');
	let freqData = [];
	let pdfData = [];
	let cdfData = [];
	let x_data = [];
	jsonData.rttJson.forEach(item => {
		freqData.push({ x: item.diff, y: item.freq });
		pdfData.push({ x: item.diff, y: item.pdf });
		cdfData.push({ x: item.diff, y: item.cdf });
	});

	chartData = [
		/* count */
		{
			type: "column",
			name: "Freq",
			/*  showInLegend: true, */
			/*  legendText: "Freq", */
			/*  visible: false, ***hidden */
			data: freqData,
			color: Highcharts.getOptions().colors[0]
		},
		/* pdf */
		{
			type: "line",
			name: "PDF",
			yAxis: 1,
			/*  showInLegend: true, */
			/*  legendText: "PDF", */
			data: pdfData,
			color: Highcharts.getOptions().colors[3]
		},
		/* cdf */
		{
			type: "line",
			name: "CDF",
			yAxis: 1,
			/*  showInLegend: true, */
			/*  legendText: "CDF", */
			data: cdfData,
			color: Highcharts.getOptions().colors[2]
		},

	];
	create_highchart(RTT_CHART_ID, tabName, chartData, RTT_CHART_ID);



	return;

}

function create_mode_chart(tabName, renderFlag) {
	if (!jsonData.hasOwnProperty('modeTxJson')) return;

	console.log('creating modechanchart');
	let modeRxData = [];
	let modeTxData = [];

	jsonData.modeRxJson.forEach(item => {
		;
		modeRxData.push({ name: item.mode, y: item.count })
	});
	jsonData.modeTxJson.forEach(item => {
		modeTxData.push({ name: item.mode, y: item.count });
	});

	chartData = [
		/* Mode Rx */
		{
			type: "column",
			name: "ModeRx",
			data: modeRxData,
			dataLabels: {
				enabled: true,
			},
			color: Highcharts.getOptions().colors[7]
		},
		/* Mode Tx */
		{
			type: "column",
			name: "ModeTx",
			data: modeTxData,
			dataLabels: {
				enabled: true,
			},
			color: Highcharts.getOptions().colors[3]
		},

	];
	create_highchart(MODE_CHART_ID, tabName, chartData, MODE_CHART_ID);

}
function create_chan_chart(tabName, renderFlag) {
	if (!jsonData.hasOwnProperty('chanTxJson')) return;

	console.log('creating chanchanchart');
	let chanRxData = [];
	let chanTxData = [];

	jsonData.chanRxJson.forEach(item => {
		chanRxData.push({ name: item.chan, y: item.count });
	});
	chanRxData.sort(function (a, b) {
		return a.name - b.name;
	});
	jsonData.chanTxJson.forEach(item => {
		chanTxData.push({ name: item.chan, y: item.count });
	});
	chanTxData.sort(function (a, b) {
		return a.name - b.name;
	});
	chartData = [
		/* Chan Rx */
		{
			type: "column",
			name: "Chan Rx",
			data: chanRxData,
			dataLabels: {
				enabled: true,
			},
			color: Highcharts.getOptions().colors[7],
		},
		/* Chan Tx */
		{
			type: "column",
			name: "Chan Tx",
			data: chanTxData,
			dataLabels: {
				enabled: true,
			},
			color: Highcharts.getOptions().colors[3],
		},

	];
	create_highchart(CHAN_CHART_ID, tabName, chartData, CHAN_CHART_ID);

}

function create_buffer_chart(tabName, renderFlag) {
	if (!jsonData.hasOwnProperty('buffer_Json')) return;

	console.log('creating buffer summary chart');
	let bufClaimData = [];
	let bufRelData = [];
	let bufLeakData = [];
	let chartData = [];

	jsonData.buffer_summaryJson.forEach(item => {
		bufClaimData.push({ name: item.owner, y: item.buf_claim });
		bufRelData.push({ name: item.owner, y: item.buf_release });
		bufLeakData.push({ name: item.owner, y: item.buf_leak });
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

	];
	create_highchart(BUFFER_CHART_ID, tabName, chartData, BUFFER_CHART_ID);

	console.log('creating buffer alloc');
	chartData = [];
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
	};

	if (!jsonData.hasOwnProperty('buffer_Json')) {
		return;
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
					/*  dataLabels: { enabled: true, format: '{x} x {y}' } */
				},
				[item.rel_frt, item.buffer_dec],
				[item.rel_frt, 0],

				/*  [item.ts_txend, 1], */

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
				/*  split: true, */
				/*  followPointer: true, */
				useHTML: true,
				headerFormat: '<span style="color: {series.color}">{series.name} </span>: 0x' + item.buffer_dec.toString(16),
				pointFormat: '<br><span>claimedFRT: ' + item.frt_dec + '</span><br> releasedFRT:' + item.rel_frt + '<br>Dur: ' + item.frt_diff + " usec"
			},
		})
	});

	create_highchart(BUFFER_CHART_ID + "2", tabName, chartData, BUFFER_CHART_ID + "2");

}

function create_cltimings_chart(tabName, renderFlag) {
	let freqData = [];
	let pdfData = [];
	let cdfData = [];
	let chartData = [];
	console.log('creating cltimings');

	for (const [key, value] of Object.entries(jsonData)) {
		freqData = [];
		pdfData = [];
		cdfData = [];
		chartData = [];
		let id = '';

		if (!key.startsWith('cltimings_'))
			continue;

		id = key.slice(10, -4);

		jsonData[key].forEach(item => {
			freqData.push({ x: item[id], y: item.freq });
			pdfData.push({ x: item[id], y: item.pdf });
			cdfData.push({ x: item[id], y: item.cdf });
		});

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
		];

		create_highchart(id, tabName, chartData, id);

	}
}

function create_cltiming_chart(tabName, renderFlag) {
	if (!jsonData.hasOwnProperty('cltimingJson')) return;

	console.log("cltiming", jsonData.cltimingJson);
	let chartData = [];
	tx_dur = 2000;

	points_dic = jsonData.cltimingJson.points_dic;
	rx_dur = points_dic['rxEnd'] - (points_dic['rx']);
	txdiff = points_dic['Tx1'] - points_dic['TargetTx1'];
	/* POLL ACK DATA */
	chartData.push({
		type: 'area',
		findNearestPointBy: 'xy',
		data: [
			[points_dic.Tx1, 0],
			[points_dic.Tx1, 0.5],
			{
				x: points_dic.Tx1 + tx_dur / 2,
				y: 0.5,
				dataLabels: {
					enabled: true,
					format: "Transmission e.g. POLL",

				}
			},
			[points_dic.Tx1 + tx_dur, 0.5],
			[points_dic.Tx1 + tx_dur, 0],
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
			[points_dic.rx, 0],
			[points_dic.rx, -0.5],
			{
				x: points_dic.rx + rx_dur / 2,
				y: -0.5,
				dataLabels: {
					enabled: true,
					format: "Reception e.g. ACK",
					verticalAlign: 'top'
				}
			},
			[points_dic.rx + rx_dur, -0.5],

			[points_dic.rx + rx_dur, 0],
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
			[points_dic.Tx2, 0],
			[points_dic.Tx2, 0.5],
			{
				x: points_dic.Tx2 + (tx_dur + 500) / 2,
				y: 0.5,
				dataLabels: {
					enabled: true,
					format: "Transmission e.g. DATA",

				}
			},
			[points_dic.Tx2 + tx_dur + 500, 0.5],
			[points_dic.Tx2 + tx_dur + 500, 0],
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
	});

	/* lollipop */
	let lollipopData = [];
	let annotations = [];

	value_levels = {
		"WrapperCall1": -2,
		"WrapperReturn": 2,
		"TargetTx1": -2,
		"Tx1": -2,
		"EndTxTime": -2,
		"rxStart_beforeCall": 2,
		"rxStart_afterCall": 2,
		"rx": 2,
		"rxEnd": -2,
		"WrapperCall2": 2,
		"TargetTx2": -2,
		"Tx2": -2,
	};

	cnt = 0;
	for (const [key, value] of Object.entries(jsonData.cltimingJson.points_dic)) {
		/*  push lollipops data */
		lollipopData.push({
			x: value,
			y: jsonData.cltimingJson.levels_dic[key],
			color: jsonData.cltimingJson.colors_dic[key],
			id: key,
			name: jsonData.cltimingJson.names_label_dic[key],
		});

		/*  push annotations for lollipop labels */
		annotations.push({
			labelOptions: {
				backgroundColor: 'rgba(255,255,0,0.3)',
				verticalAlign: jsonData.cltimingJson.levels_dic[key] < 0 ? 'top' : 'bottom',
				/*  y: 15 */
				distance: 10,
			},
			labels: [{
				point: key,
				text: jsonData.cltimingJson.names_label_dic[key]
			}]
		});
		/*  push annotations for arrows and its labels */
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
				/*  markerEnd: 'arrow', */
				/*  markerStart:'diamond', */

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
		});

		cnt++;
	}
	/* for min/max/avg */
	annotations.push({
		/* undefined - delayed value is inherited from plotOptions */
		labelOptions: {
			backgroundColor: 'rgba(0,0,0,0.8)',
		},
		labels: [{
			point: {
				x: 150, y: 0,
			},
			text: "min/max/avg"
		}]
	});


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
		/*  color: '#8FBC8F', */
		connectorWidth: 2,
		fillOpacity: 0.6,
		toolTip: {
			enabled: false
		},
		enableMouseTracking: false,

	});

	create_highchart(CLTIMING_CHART_ID, tabName, chartData, CLTIMING_CHART_ID, annotations_arr = annotations);

}

function create_timeline_chart(tabName, renderFlag) {
	if (!jsonData.hasOwnProperty('timeline_clStartEndJson')) return;

	console.log('creating timeline chart');
	let chartData = [];
	let dataPoints = [];

	new_timeline_txJson = jsonData.timeline_txJson.filter((item) => {
		return ((parseInt(item.cl_id) >= new_start_cl_id) && ((parseInt(item.cl_id) <= new_end_cl_id)));
	});
	new_timeline_rxJson = jsonData.timeline_rxJson.filter((item) => {
		return ((parseInt(item.cl_id) >= new_start_cl_id) && (parseInt(item.cl_id) <= new_end_cl_id));
	});
	new_timeline_clStartEndJson = jsonData.timeline_clStartEndJson.filter((item) => {
		return ((parseInt(item.cl_id) >= new_start_cl_id) && (parseInt(item.cl_id) <= new_end_cl_id));
	});
	new_timeline_phyIndJson = jsonData.timeline_phyIndJson.filter((item) => {
		return ((parseInt(item.cl_id) >= new_start_cl_id) && (parseInt(item.cl_id) <= new_end_cl_id));
	});
	new_timeline_clTracesJson = jsonData.timeline_clTracesJson.filter((item) => {
		return ((parseInt(item.cl_id) >= new_start_cl_id) && (parseInt(item.cl_id) <= new_end_cl_id));
	});


	/* TX area*/
	new_timeline_txJson.forEach(item => {
		th = THRESHOLDS[item.NODE];
		chartData.push({
			type: 'area',
			findNearestPointBy: 'xy',
			data: [
				[item.ts_txstart, 0 + th],
				[item.ts_txstart, 1 + th],
				{
					x: item.ts_txstart + item.tx_dur / 2.0,
					y: 1 + th,
					/*  dataLabels: { enabled: true, format: '{x} x {y}' } */
				},
				[item.ts_txend, 1 + th],
				[item.ts_txend, 0 + th],

				/*  [item.ts_txend, 1], */

			],
			states: {
				inactive: {
					opacity: 0.8
				}
			},
			threshold: th,

			zIndex: 5,
			name: "Node " + item.NODE + "-TX",
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
	new_timeline_rxJson.forEach(item => {
		th = THRESHOLDS[item.NODE];

		chartData.push({
			type: 'area',
			findNearestPointBy: 'xy',
			data: [
				[item.ts_rxstart, 0 + th], [item.ts_rxstart, -1 + th],
				{
					x: item.ts_rxstart + item.rx_dur / 2.0,
					y: -1 + th,
					/*  dataLabels: { enabled: true, format: '{x} x {y}',}, */
					toolTip: false
				},
				[item.ts_rxend, -1 + th],
				[item.ts_rxend, 0 + th]
				/*  [item.ts_rxend, -1], */

			],
			threshold: th,

			turboThreshold: 0,

			states: {
				inactive: {
					opacity: 0.8
				}
			},
			showInLegend: false,
			zIndex: 5,
			name: "Node " + item.NODE + "-RX",
			color: item.color,
			tooltip: {
				/*  followPointer: true, */
				split: true,
				useHTML: true,
				headerFormat: '<span style="color: {series.color}">{series.name}</span>: ',
				pointFormat: '<span>FRT: {point.x}</span><br>' + item.hoverinfo
			},
		})
	});
	/* CL area */
	new_timeline_clStartEndJson.forEach(item => {
		th = THRESHOLDS[item.NODE];

		chartData.push({
			type: 'area',
			/*  findNearestPointBy: 'xy', */
			data: [
				[item.clstart, 0 + th], [item.clstart, 1.5 + th],
				{
					x: item.clstart + item.cldiff / 2.0,
					y: 1.5 + th,
					dataLabels: { enabled: true, format: item.hoverinfo }
				},
				[item.clend, 1.5 + th],
				[item.clend, -1.5 + th], [item.clstart, -1.5 + th],
				[item.clstart, 0 + th],
			],
			states: {
				inactive: {
					opacity: 0.8
				}
			},
			threshold: item.NODE,

			/*  dataLabels: { enabled: true, format: item.hoverinfo, inside: true }, */
			zIndex: 1,
			showInLegend: false,
			grouping: true,
			name: "Node " + item.NODE + "-CL " + item.cl_id,
			fillColor: 'rgba(247, 228, 194,0.35)',
			color: "rgba(247, 228, 194,1)",

			turboThreshold: 0,

			/*  tooltip:null */
			tooltip: {
				/*  followPointer: true, */
				split: true,
				useHTML: true,
				headerFormat: '<span style="color: rgba(170, 135, 54,1)">{series.name}</span>: ',
				pointFormat: '<span>FRT: {point.x}</span> ' + item.hoverinfo
			},
		})
	});

	/* Phy Data Indications */
	dataPoints = [];
	dataPoints = new_timeline_phyIndJson.map((item) => {
		if (!Number(item.frt_dec)) {
			console.log("Error..", item);
		}
		return {
			x: item.frt_dec,
			y: -2 + THRESHOLDS[item.NODE],
			color: item.color,
			info: item.trace_info,
			node: item.NODE
		};
	});

	chartData.push({
		type: "scatter",
		findNearestPointBy: 'xy',
		/*  axisYType: 'primary', */
		name: "phyInd",
		showInLegend: true,
		states: {
			inactive: {
				opacity: 0.8
			}
		},
		visible: false, /* ***hidden */
		data: dataPoints,
		tooltip: {
			headerFormat: '<span style="font-size:10px">{series.name} FRT: {point.key}</span><table>',
			pointFormat: '<tr><td style="color:{series.color};padding:0">Node {point.node}-CL {point.clid} </td></tr>' +
				'<tr><td style="color:{series.color};padding:0">{point.info} </td></tr>',
			footerFormat: '</table>',
			/*  shared: true, */
			useHTML: true,
			followPointer: false,
			/*  outside: true */
		},
		marker: {
			symbol: "triangle"
		},
		turboThreshold: 0,


	});

	/* CL Traces */
	dataPoints = [];
	dataPoints = new_timeline_clTracesJson.map((item) => {
		return {
			x: item.frt_dec,
			y: 2 + THRESHOLDS[item.NODE],
			color: item.color,
			info: item.trace_info,
			clid: item.cl_id,
			node: item.NODE
		};
	});

	chartData.push({
		type: "scatter",
		findNearestPointBy: 'xy',
		/*  axisYType: 'primary', */
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
		visible: false, /* ***hidden */
		data: dataPoints,
		tooltip: {
			headerFormat: '<span style="font-size:10px">FRT: {point.key}</span><table>',
			pointFormat: '<tr> <td style="color:{series.color};padding:0">Node {point.node}-CL {point.clid} </td>\</tr>' +
				'<tr> <td style="color:{series.color};padding:0">{point.info} </td>\</tr>',
			footerFormat: '</table>',
			/*  shared: true, */
			useHTML: true,
			followPointer: false,
			/*  outside: true */
		},
		turboThreshold: 0,

	});

	create_highchart(TIMELINE_CHART_ID, tabName, chartData, TIMELINE_CHART_ID);


}

/* function trigerred when clicked on the tab */
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
	graphId = evt.currentTarget.attributes.graphId.value;

	if (Object.keys(charts[graphId]).length == 0)
		drawChart(graphId, tabName, true);

}

function init_timeline_cl_filter() {
	if (!jsonData.hasOwnProperty('timeline_clStartEndJson')) return;
	orig_start_cl_id = Math.min(parseInt(jsonData.timeline_txJson[0].cl_id), parseInt(jsonData.timeline_rxJson[0].cl_id));
	orig_end_cl_id = Math.max(jsonData.timeline_txJson[jsonData.timeline_txJson.length - 1].cl_id, jsonData.timeline_rxJson[jsonData.timeline_rxJson.length - 1].cl_id);
	$('#timelineStartClId').val(orig_start_cl_id);
	$('#timelineEndClId').val(orig_end_cl_id);
	old_start_cl_id = orig_start_cl_id;
	old_end_cl_id = orig_end_cl_id;
	new_start_cl_id = orig_start_cl_id;
	new_end_cl_id = orig_end_cl_id;
	$('.clFilter .totalCls').html((new_end_cl_id - new_start_cl_id + 1) + " CL(s)");
	console.log("total CLs", new_end_cl_id - new_start_cl_id);
	console.log("Filter init ", { new_start_cl_id, new_end_cl_id });

}
var new_start_cl_id = 0;
var new_end_cl_id = 0;
var old_start_cl_id = 0;
var old_end_cl_id = 0;
var orig_start_cl_id = 0;
var orig_end_cl_id = 0;
var diff = 0;
function prepare_timeline_cl_filter(evt = false) {

	if (evt.target.id == "timelineResetBtn") {
		new_start_cl_id = Math.min(parseInt(jsonData.timeline_txJson[0].cl_id), parseInt(jsonData.timeline_rxJson[0].cl_id));
		new_end_cl_id = Math.max(jsonData.timeline_txJson[jsonData.timeline_txJson.length - 1].cl_id, jsonData.timeline_rxJson[jsonData.timeline_rxJson.length - 1].cl_id);
		$('#timelineStartClId').val(new_start_cl_id);
		$('#timelineEndClId').val(new_end_cl_id);
		$(".alert").alert('close');

	} else {
		new_start_cl_id = parseInt($('#timelineStartClId').val());
		new_end_cl_id = parseInt($('#timelineEndClId').val());
	}


	if (new_start_cl_id < orig_start_cl_id || new_start_cl_id > orig_end_cl_id) {
		display_alert('warning', `<b>Start CL Id ${new_start_cl_id}&nbsp;is out of range [${orig_start_cl_id},${orig_end_cl_id}].</b> Resetting to the min possible value.`);
		new_start_cl_id = orig_start_cl_id;
		$('#timelineStartClId').val(new_start_cl_id);
	}
	if (new_end_cl_id > orig_end_cl_id || new_end_cl_id < orig_start_cl_id) {
		display_alert('warning', `<b>End CL Id ${new_end_cl_id}&nbsp;is out of range [${orig_start_cl_id},${orig_end_cl_id}].</b> Resetting to the max possible value.`);
		new_end_cl_id = orig_end_cl_id;
		$('#timelineEndClId').val(new_end_cl_id);
	}

	/* do nothing if filters has not changed */
	if (new_start_cl_id == old_start_cl_id && new_end_cl_id == old_end_cl_id) return;

	diff = new_end_cl_id - new_start_cl_id;
	if (diff < 0) {
		display_alert('warning', `<b> End CL id ${new_end_cl_id}&nbsp;> Start CL id ${new_start_cl_id}</b>. Resetting to the range [${orig_start_cl_id}, ${orig_end_cl_id}] `);
		new_start_cl_id = orig_start_cl_id;
		new_end_cl_id = orig_end_cl_id;
		$('#timelineStartClId').val(new_start_cl_id);
		$('#timelineEndClId').val(new_end_cl_id);
	}
	/* console.log("Filtered ", { new_start_cl_id, new_end_cl_id }); */
	$('.clFilter .totalCls').html((new_end_cl_id - new_start_cl_id + 1) + " CL(s)");
	drawChart(TIMELINE_CHART_ID, "timelineTab", true);
	old_start_cl_id = new_start_cl_id;
	old_end_cl_id = new_end_cl_id;
}

/* when everything is loaded */
window.onload = function () {

	if (nodeip != 'None' || nodeip.length != 4) {
		$('#nodeip').html(nodeip);
	} else if (nodefile != 'None') {
		$('#nodeip').html(nodefile);
	}

	/* pie charts */
	drawPieChart();

	/* prepare timeline cl_id filters */
	init_timeline_cl_filter();

	$(document).on("click", ".filterBtn", prepare_timeline_cl_filter);
	$('.filterInput').keypress(function (event) {
		var keycode = (event.keyCode ? event.keyCode : event.which);
		if (keycode == '13') {
			prepare_timeline_cl_filter(event);
		}
	});

	/* trigger a click on the first tab to show*/
	document.getElementById("firstTab").click();

	/* remove marker handler */
	$(document).on("click", ".removeMkrBtnClass", function (event) {
		parentRow = $(this).parent().parent().parent();
		id = parentRow.attr('id').split('-');
		$(`.marker${id[1]}Line`).remove();
		$(`.marker${id[2]}Line`).remove();
		$(`.markerLabel${id[1]}`).remove();
		$(`.markerLabel${id[2]}`).remove();
		parentRow.remove();

	});

	/* remove all markers handler */
	$(document).on("click", "#removeAllMarkers", function (event) {
		$('.marker').remove();
		$('.markerLabel').remove();
		markerCnt = 0;
	});

	/* refreshing the page */
	refreshIntv = $('#refreshIntvDur').val() * $('#refreshIntUnit').val() * 1000;
	var seconds = refreshIntv / 1000;
	var secondTimer;
	console.log("refreshIntv", refreshIntv);
	if (refreshIntv > 0) {
		refreshTimer = setTimeout(function () {
			location.reload();
		}, refreshIntv);
		secondTimer = setInterval(function () {
			$('.countdownString').html(`<i class="fas fa-sync"></i>&nbsp;in ${seconds--}...`);
		}, 1000);
	}

	/* handle change in the refresh interval */
	$(document).on("change", "#refreshIntvDur,#refreshIntUnit", function (event) {
		refreshIntv = $('#refreshIntvDur').val() * $('#refreshIntUnit').val() * 1000;
		seconds = refreshIntv / 1000;
		if (typeof refreshTimer !== 'undefined') clearTimeout(refreshTimer);
		if (secondTimer) clearInterval(secondTimer);
		if (refreshIntv > 0) {
			refreshTimer = setTimeout(function () {
				location.reload();
			}, refreshIntv);
			secondTimer = setInterval(function () {
				$('.countdownString').html(`<i class="fas fa-sync"></i>&nbsp;in ${seconds--}...`);
			}, 1000);
		} else {
			$('.countdownString').html('');

		}
	});


}
