
///////////////////////////////////////////////////////////////////////////////////

/**
 * Constructor for the simulation
 * @param {ID String} elementId 
 */
function Simulation(elementId) {
  this.jqElement = $('#' + elementId);

  this.width = 10;
  this.height = 10;

  //in milliseconds
  this.animationTimeFrame = 250;

  this.canvas = document.getElementById(elementId);

  this.animationFns = [];
  
  this.currentTemp = ((
    Math.random() * (100 - 17)
  )/100.0);
  this.heaterOn = false;

  var that = this;

  app.get('/', function(req, res) {
    res.send({
      "/thermostat": "std_msgs/Int64",
      "/heater": "std_msgs/String"
    });
  });

  app.post('/thermostat', function(req, res) {
    res.send({
      "std_msgs/Int64": that.currentTemp
    });
  });

  app.get('/thermostat', function(req, res) {
    res.send({
      "std_msgs/Int64": that.currentTemp
    });
  });

  app.get('/heater', function(req, res) {
    res.send({
      "std_msgs/String": that.heaterOn
    });
  });

  app.post('/heater', function(req,res) {
    //when posted, use this to set the state and update the view
    if (req.query["std_msgs/String"] === "on") {
      that.heaterOn = true;
    } else if(req.query["std_msgs/String"]  == "off") {
      that.heaterOn = false;
    }

    res.send({
      "std_msgs/String": that.heaterOn
    });
  });

  //set listener here
  app.listen(3000, function() {
    //get all the JSON here and perform the corresponding response.
    console.log('sim server running on port');
  });

  this.run();
}

/**
 * resets the heater to off and the temperature to a random value
 */
Simulation.prototype.restart = function() {
  this.heaterOn = false;
  this.currentTemp = ((
    Math.random() * (90 - 10)
  )/100.0);
}

/**
* returns the canvas frame to render
* given the JSON
*/
Simulation.prototype.defineFrameFn = function(heaterState="off") {
  var that = this;

  console.log(that.currentTemp);
  var colorRange = [
    "#FA7921",
    "#FCBB4B",
    "#FDE74C",
    "#B8EA5B",
    "#5BEAC9",
  ]

  var yMax = colorRange.length;
  var lMax = 50;
  var marginFromTop = 75;
  that.clearCanvas();

  //draw the thermostat
  //placed between the grid range of 50 - 330
  for (y = 0; y < yMax; y+=1){
    for (l = 0; l < lMax; l+= 1) {
      that.draw(colorRange[y], colorRange[y], Math.round(that.canvas.width/4.0), marginFromTop + ((y*lMax)+l));
    }
  }
  
  //record the current temperature bar
  that.draw("lightgray", "lightgray", Math.round(that.canvas.width/4.0) - 10,
            (marginFromTop + (yMax*lMax)) - Math.round( marginFromTop +  (((yMax*lMax)*that.currentTemp - marginFromTop)) ));
  that.draw("lightgray", "lightgray", Math.round(that.canvas.width/4.0),
            (marginFromTop + (yMax*lMax)) - Math.round( marginFromTop +  (((yMax*lMax)*that.currentTemp - marginFromTop)) ));
  that.draw("lightgray", "lightgray", Math.round(that.canvas.width/4.0) + 10,
            (marginFromTop + (yMax*lMax)) - Math.round( marginFromTop +  (((yMax*lMax)*that.currentTemp - marginFromTop)) ));
  that.writeText("Current Temperature: " + Math.round(that.currentTemp*100) + " C", 50, 35 );
  
  var minTemp = "18";
  var maxTemp = "22";
  
  //mark the range 
  that.writeText(minTemp + " C" , Math.round(that.canvas.width/4.0) + 15,
            (marginFromTop + (yMax*lMax)) -  Math.round( marginFromTop +  (((yMax*lMax)* ( parseInt(minTemp) /100.0) - marginFromTop)) - 5));
  that.writeText(maxTemp + " C" , Math.round(that.canvas.width/4.0) + 15,
            (marginFromTop + (yMax*lMax)) -  Math.round( marginFromTop +  (((yMax*lMax)*( parseInt(maxTemp)/100.0) - marginFromTop)) + 5));
  
  //record the current state of the system
  that.writeText("Current Heater State: " + heaterState, 50, 50);
}

Simulation.prototype.updateTemperature = function() {
  //start changing the temperature
  var that = this;

  var heaterState = "off";
  
  if (that.heaterOn) {
    //increase temperature
    that.currentTemp += (Math.random(1, 5)/100.0);
    heaterState = "on";
    if (that.currentTemp > 1) {
      that.currentTemp = 1;
    }
  } else {
    that.currentTemp = that.currentTemp - (Math.random(1, 5)/100.0);
    if (that.currentTemp <= 0) {
      that.currentTemp = 0;
    }
  }

  //redraw the thing
  that.defineFrameFn(heaterState);
  //recall the thing
  setTimeout(function() {
    that.updateTemperature()
  }, that.animationTimeFrame);
}

Simulation.prototype.run = function() {
  var that = this;

  //pull the data and perform the corresponding action
  that.canvas.html = "";
  that.ctx = that.canvas.getContext("2d");
  //load the file with the simulation results
  //and append as functions to the animationFns

  //for this simulation, it will control the parameters
  // of one thing in the system. This file should
  //contain the resulting part
  that.updateTemperature();
}


/**
 * clear anything on the canvas window
 */
Simulation.prototype.clearCanvas = function() {
  this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
}

/**
 * render one frame of the simulation
 */
Simulation.prototype.dframe = function(frameIndex) {
  var that = this;
  that.clearCanvas();
  that.animationFns[frameIndex]();
  var newFrameIndex = frameIndex + 1;
  if (newFrameIndex < that.animationFns.length){
    //continue
    setTimeout(function() {
      that.dframe(newFrameIndex)
    }, that.animationTimeFrame);
  }
}

/**
 * draw a point on the canvas
 */
Simulation.prototype.draw = function(strokeColor, fillColor, xP, yP){
  var that = this;
  this.ctx.strokeStyle = strokeColor;
  this.ctx.fillStyle = fillColor;

  // Draw x, y, width, height
  this.ctx.fillRect(
    xP, 
    yP,
    that.width,
    that.height
  );
}

/**
 * display some text on the window
 */
Simulation.prototype.writeText = function(txt, xP=50, yP=50) {
  this.ctx.fillStyle = "black";
  this.ctx.font = "14px monospace";
  this.ctx.fillText(txt, xP, yP);
}
