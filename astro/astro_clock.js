


//Append the month names within the arcs
svg.selectAll(".monthText")
    .data(monthData)
    .enter().append("text")
    .attr("class", "monthText")
    .attr("x", 5)   //Move the text from the start angle of the arc
    .attr("dy", 18) //Move the text down
    .append("textPath")
    .attr("xlink:href",function(d,i){return "#monthArc_"+i;})
    .text(function(d){return d.month;});




<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
	<title>Months on an Arc</title>

	<!-- D3.js -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js" charset="utf-8"></script>
	
	<!-- Month names -->
	<link href='http://fonts.googleapis.com/css?family=Courgette' rel='stylesheet' type='text/css'>
	
	<style>
		#chart{
			text-align: center;
		}
		
		.monthArc {
			fill: white;
			stroke: #AAAAAA;
		}

		.monthText {
			fill: #6B6B6B;
			font-size: 13px;
			font-family: 'Courgette', sans-serif;
		}
	</style>
  </head>
  <body>

	<div id="chart"></div>
	
    <script>
		////////////////////////////////////////////////////////////
		//////////////////////// Set-up ////////////////////////////
		////////////////////////////////////////////////////////////

		var screenWidth = window.innerWidth;

		var margin = {left: 20, top: 20, right: 20, bottom: 20},
			width = Math.min(screenWidth, 500) - margin.left - margin.right,
			height = Math.min(screenWidth, 500) - margin.top - margin.bottom;
					
		var svg = d3.select("#chart").append("svg")
					.attr("width", (width + margin.left + margin.right))
					.attr("height", (height + margin.top + margin.bottom))
				  .append("g").attr("class", "wrapper")
					.attr("transform", "translate(" + (width / 2 + margin.left) + "," + (height / 2 + margin.top) + ")");

		////////////////////////////////////////////////////////////
		//////////////////// Scales & Data /////////////////////////
		////////////////////////////////////////////////////////////

		//The start date number and end date number of the months in a year
		var monthData = [
			{month: "January", 	startDateID: 0, 	endDateID: 30},
			{month: "February", startDateID: 31, 	endDateID: 58},
			{month: "March", 	startDateID: 59, 	endDateID: 89},
			{month: "April", 	startDateID: 90, 	endDateID: 119},
			{month: "May", 		startDateID: 120, 	endDateID: 150},
			{month: "June", 	startDateID: 151, 	endDateID: 180},
			{month: "July", 	startDateID: 181, 	endDateID: 211},
			{month: "August", 	startDateID: 212, 	endDateID: 242},
			{month: "September",startDateID: 243, 	endDateID: 272},
			{month: "October", 	startDateID: 273, 	endDateID: 303},
			{month: "November", startDateID: 306, 	endDateID: 333},
			{month: "December",	startDateID: 334, 	endDateID: 364}
		];

		//Creates a function that makes SVG paths in the shape of arcs with the specified inner and outer radius 
		var arc = d3.svg.arc()
			.innerRadius(width*0.9/2) 
			.outerRadius(width*0.9/2 + 30);
		  
		//Creates function that will turn the month data into start and end angles
		var pie = d3.layout.pie()
			.value(function(d) { return d.endDateID - d.startDateID; })
			.padAngle(.01)
			.sort(null);

		////////////////////////////////////////////////////////////
		//////////////////// Create the Slices /////////////////////
		////////////////////////////////////////////////////////////

		//Draw the arcs themselves
		svg.selectAll(".monthArc")
			.data(pie(monthData))
		   .enter().append("path")
			.attr("class", "monthArc")
			.attr("id", function(d,i) { return "monthArc_"+i; })
			.attr("d", arc);
			
		//Append the month names within the arcs
		svg.selectAll(".monthText")
			.data(monthData)
		    .enter().append("text")
			.attr("class", "monthText")
			.attr("x", 5) //Move the text from the start angle of the arc
			.attr("dy", 18) //Move the text down
		    .append("textPath")
			.attr("xlink:href",function(d,i){return "#monthArc_"+i;})
			.text(function(d){return d.month;});	
	</script>
	
  </body>
</html>


