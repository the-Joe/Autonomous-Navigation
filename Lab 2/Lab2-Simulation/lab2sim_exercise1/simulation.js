///////////////////////////////////////////////////////////////////////////////////
var Engine = Matter.Engine;
var Render = Matter.Render;
var World = Matter.World;
var Bodies = Matter.Bodies;
var Mouse = Matter.Mouse;
var MouseConstraint = Matter.MouseConstraint;
var Body = Matter.Body;
var Events = Matter.Events;


var colors = {
  green: "#7C9D30",
  red: "#E54012",
  yellow: "#FDE74C",
  greenOff: "#717D56",
  redOff: "#A78379",
  yellowOff: "#B8B178",
  gray: "#FFFFFF",
  blue: "#5BC0EB",
}

function getRandomArbitrary(min, max) {
  return Math.random() * (max - min) + min;
}

function euclideanDistance(x1, y1, x2, y2) {
  return Math.sqrt(Math.pow((x2 - x1), 2) + Math.pow((y2 - y1), 2));
}

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
  this.matterCanvas = document.getElementById("matter");

  //min distance to allow pickup and delivery
  this.currentTime = 0;

  var that = this;
  
  this.mouseOpt = false;

  this.leaderBot = {};
  this.followBot = {};

  this.X_POS = (that.canvas.width/4 - 50);
  this.Y_POS = (that.canvas.height / 2);
  this.BOT_SIZE = 50;
  this.MAX_ROBOT_SPEED = 5;
  this.MAX_ROBOT_ANGVEL = Math.pi/6;
  this.DISTANCE_TO_CHANGE_DIRECTION = this.BOT_SIZE + 10;

  this.TOPIC_MSG_MAPPING = {
    //topics subscribed to on turtlebot Bringup
    "/cmd_vel": "geometry_msgs/Twist",
    "/reset": "std_msgs/Empty",

    //topics robots publish to on turtlebot Bringup
    //"/battery_state": "sensor_msgs/BatteryState",
    //"/imu": "sensor_msgs/Imu",
    //"/joint_states": "sensor_msgs/JointState",
    "/odom": "nav_msgs/Odometry",
    //"/sensor_state": "turtlebot3_msgs/SensorState",
    //"/version_info": "turtlebot3_msgs/VersionInfo",

    //turtlebot's ids
    "/scan": "sensor_msgs/LaserScan",

    //things specific to the simulator like score, reset
    "/myscore": "std_msgs/Int64",
    "/opponentscore": "std_msgs/Int64",
    "/scorechange": "std_msgs/Int64"
  }

  //provide information on app of the topics for
  //ROS to sub to
  app.get('/', function (req, res) {
    res.send(that.TOPIC_MSG_MAPPING);
  });

  app.post('/reset', function(req,res) {
    that.restart();
    res.send({
      [that.TOPIC_MSG_MAPPING["/reset"]]: {}
    });
  });


  app.get('/follower/odom', function(req,res) {
    res.send({
      [that.TOPIC_MSG_MAPPING["/odom"]]: that.getRobotOdom()
    });
  });

  
  app.get('/leader/odom', function(req,res) {
    res.send({
      [that.TOPIC_MSG_MAPPING["/odom"]]: that.getLeaderRobotOdom()
    });
  });

  //add to q
  app.post('/cmd_vel', function (req, res) {
    let result = that.updateRobotVelocity(JSON.parse(req.query[that.TOPIC_MSG_MAPPING["/cmd_vel"]]));
    res.send({
      [that.TOPIC_MSG_MAPPING["/cmd_vel"]]: result,
    });
  });

  //set listener here
  app.listen(3000, function () {
    //get all the JSON here and perform the corresponding response.
    console.log('sim server running on port');
  });

  this.run();
}

/**
 * Will toggle the mouse constraint for matterjs library
 * @param {Boolean} mouseOption 
 */
Simulation.prototype.mouseToggle = function(mouseOption) {
  let that = this;
  that.mouseOpt = mouseOption;

  if (that.mouseOpt) {
    // add mouse control
    var mouse = Mouse.create(that.render.canvas);
    World.add(that.engine.world,MouseConstraint.create(that.engine, {
      mouse: mouse,
      constraint: {
        stiffness: 0.9,
        render: {
          visible: true
        }
      }
    }) );

    // keep the mouse in sync with rendering
    that.render.mouse = mouse;
  } else {
    this.restartPositions();
  }

}

/**
 * resets the heater to off and the temperature to a random value
 */
Simulation.prototype.restart = function () {
  this.currentTime = 0;

  this.myScore = 0;
  this.opponentScore = 0;

  this.restartPositions();
  if (this.mouseOpt) {
    this.mouseToggle(this.mouseOpt);
  }
}

/**
 * restart positions of all bodies
 */
Simulation.prototype.restartPositions = function() {
  let that = this;
  this.engine.events = {};

  World.clear(this.engine.world);
  Engine.clear(this.engine);
  Render.stop(this.render);

  this.render.canvas = null;
  this.render.context = null;
  this.render.textures = {};

  this.initWorld();
  
  Body.setVelocity(that.leaderBot,
    {
      x:  (Math.abs(1.5) > that.MAX_ROBOT_SPEED ? Math.sign(1.5)*that.MAX_ROBOT_SPEED : 1.5),
      y:  (Math.abs(1.5) > that.MAX_ROBOT_SPEED ? Math.sign(1.5)*that.MAX_ROBOT_SPEED : 1.5)
    }
  )
}


/**
 * Returns the robot's odometry reading 
 * @param {integer} botId 
 */
Simulation.prototype.getRobotOdom = function() {
  var bb = this.followBot;
  return {
    "pose": {
      "position": {
        "x": bb.position.x,
        "y": bb.position.y,
        "z": 0,
      },
      "orientation": {
        "x": 0,
        "y": 0,
        "z": bb.angle,
        "w": 0,
      }
    },
    "twist": {
      "linear": {
        "x": bb.velocity.x,
        "y": bb.velocity.y,
        "z": 0,
      },
      "angular": {
        "x": 0,
        "y": 0,
        "z": bb.angularSpeed,
      }
    }
  };
}

/**
 * Returns the robot's odometry reading 
 * @param {integer} botId 
 */
Simulation.prototype.getLeaderRobotOdom = function() {
  var bb = this.leaderBot;
  return {
    "pose": {
      "position": {
        "x": bb.position.x,
        "y": bb.position.y,
        "z": 0,
      },
      "orientation": {
        "x": 0,
        "y": 0,
        "z": bb.angle,
        "w": 0,
      }
    },
    "twist": {
      "linear": {
        "x": bb.velocity.x,
        "y": bb.velocity.y,
        "z": 0,
      },
      "angular": {
        "x": 0,
        "y": 0,
        "z": bb.angularSpeed,
      }
    }
  };
}

/**
 * run every .25 seconds and updates the leader's velocity such that it moves in a random 
 * direction. If it nears a wall in the defined distance, will determine if it will move at a curve left or right
 */
Simulation.prototype.moveLeader = function() {
  let that = this;

  let xV = that.leaderBot.velocity.x;
  let yV = that.leaderBot.velocity.y;

  //random generate new velocity if 0
  if (xV != 1.5 && xV != -1.5){
    that.leaderBot.velocity.x = 1.5;
  }
  if (yV != 1.5 && yV != -1.5){
    that.leaderBot.velocity.y = 1.5;
  }
  xV = that.leaderBot.velocity.x;
  yV = that.leaderBot.velocity.y;


  if ((that.leaderBot.position.x < that.DISTANCE_TO_CHANGE_DIRECTION) || (that.leaderBot.position.x > that.canvas.width - that.DISTANCE_TO_CHANGE_DIRECTION) ) {
    //too close to the left side of the field
    xV = xV * -1;
  } 

  if ((that.leaderBot.position.y < that.DISTANCE_TO_CHANGE_DIRECTION) || (that.leaderBot.position.y > that.canvas.height - that.DISTANCE_TO_CHANGE_DIRECTION) ){
    yV = yV * -1;
  }

  Body.setVelocity(that.leaderBot,
    {
      x:  xV,
      y:  yV
    }
  )
}

/**
 * update the robot's velocity
 * @param {} twist 
 */
Simulation.prototype.updateRobotVelocity = function (twist) {
  let that = this;
  Body.setAngularVelocity(that.followBot,(Math.abs(twist.angular.z) > that.MAX_ROBOT_ANGVEL ? Math.sign(twist.angular.z)*that.MAX_ROBOT_ANGVEL : twist.angular.z));
  Body.setVelocity(that.followBot,{
    x:  (Math.abs(twist.linear.x) > that.MAX_ROBOT_SPEED ? Math.sign(twist.linear.x)*that.MAX_ROBOT_SPEED : twist.linear.x),
    y:  (Math.abs(twist.linear.y) > that.MAX_ROBOT_SPEED ? Math.sign(twist.linear.y)*that.MAX_ROBOT_SPEED : twist.linear.y)
  });
    return {};
}


/**
 * run an instance of the simulator
 */
Simulation.prototype.run = function () {
  var that = this;

  //pull the data and perform the corresponding action
  that.canvas.html = "";
  that.ctx = that.canvas.getContext("2d");

  // PHYSICS ENGINE INITIALIZATION
  // module aliase
  that.initWorld();

  //for this simulation, it will control the parameters
  // of one thing in the system. This file should
  //contain the resulting part
  that.updateSignal();
}

/**
 * repeated updates needed for the simulator
 */
Simulation.prototype.updateSignal = function () {
  //start changing the temperature
  var that = this;

  that.currentTime += .25;

  //redraw the thing
  //that.defineFrameFn({
  //  time: that.currentTime
  //});
  that.initCanvasWorld();
  that.moveLeader();

  //recall the thing
  setTimeout(function () {
    that.updateSignal()
  }, that.animationTimeFrame);
}

/**
 * draws any necessary updates to the canvas world 
 * such as score, time, etc. that are not part of matter.js
 */
Simulation.prototype.initCanvasWorld = function() {
  let that = this;
  //draw the field outline
  that.clearCanvas();
  that.ctx.lineWidth = 6;
  that.ctx.rect(10, 10, that.canvas.width - 20, that.canvas.height - 20);
  that.ctx.stroke();
  that.ctx.fillStyle = colors.gray;
  that.ctx.fill();
  //border of stadium
  that.ctx.strokeStyle = colors.gray;
  that.ctx.beginPath();
  that.ctx.rect(10, 10, that.canvas.width - 20, that.canvas.height - 20);
  that.ctx.stroke();
}



/**
 * Matter.js world initialization
 */
Simulation.prototype.initWorld = function () {
  let that = this;

  //create engine
  that.engine = Engine.create();
  that.engine.world.gravity.y = 0;


  that.render = Render.create({
    canvas: that.matterCanvas,
    engine: that.engine,
    options: {
      width: 750,
      height: 500,
      hasBounds: true,
      pixelRatio: 1,
      showCollisions: true,
      background: 'transparent',
      showVelocity: true,
      showBounds: true,
      showAxes: true,
      showAngleIndicator: true,
      showPositions: true,
      wireframes: false, //required for images
    }
  });

  //add border constraints
  World.add(that.engine.world, [
    // walls
    Bodies.rectangle(10, (that.canvas.height - 10) / 2, 5, (that.canvas.height - 20), {
      density: 99,
      label:"wall",
      isStatic: true
    }),
    Bodies.rectangle(5 + (that.canvas.width - 10) / 2, 10, (that.canvas.width - 10), 5, {
      density: 99,
      label:"wall",
      isStatic: true
    }),
    Bodies.rectangle((that.canvas.width - 10), (that.canvas.height - 10) / 2, 5, (that.canvas.height - 20), {
      density: 99,
      label:"wall",
      isStatic: true
    }),
    Bodies.rectangle(5 + (that.canvas.width - 10) / 2, (that.canvas.height - 10), (that.canvas.width - 10), 5, {
      density: 99,
      label:"wall",
      isStatic: true
    })
  ]);

  //draw the user's team robots
  var bot = Bodies.rectangle(
    that.X_POS,
    that.Y_POS,
    that.BOT_SIZE, that.BOT_SIZE, {
      density: 1,
      mass: 1,
      frictionAir: 0,
      restitution: .2,
      friction: 0,
      sleepThreshold: 1,
      label:"Leader",
      render: {
        sprite: {
          xScale: 0.2,
          yScale: 0.2,
          texture: './robot.png'
        }
      }
    }
  );

  that.followBot = bot;
  World.add(that.engine.world, bot);

  //draw the user's team robots
  var bot = Bodies.rectangle(
    that.X_POS + (this.X_POS),
    that.Y_POS,
    that.BOT_SIZE, that.BOT_SIZE, {
      density: 1,
      mass: 1,
      frictionAir: 0,
      restitution: .2,
      friction: 0,
      sleepThreshold: 1,
      label:"Follower",
      velocity: {
        x: 1.5,
        y: 1.5
      },
      render: {
        sprite: {
          xScale: 0.2,
          yScale: 0.2,
          texture: './robotOpposite.png'
        }
      }
    }
  );

  that.leaderBot = bot;
  World.add(that.engine.world, bot);
  
  Engine.run(that.engine); //run
  Render.run(that.render); //render
}



/**
 * clear anything on the canvas window
 */
Simulation.prototype.clearCanvas = function () {
  this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
}


/**
 * draw a point on the canvas
 */
Simulation.prototype.draw = function (strokeColor, fillColor, xP, yP) {
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
 * draw variable size rectangle
 */
Simulation.prototype.drawRectangle = function (strokeFillColor, xP, yP, w, h) {
  this.ctx.strokeStyle = strokeFillColor;
  this.ctx.fillStyle = strokeFillColor;

  this.ctx.fillRect(xP, yP, w, h);
}


/**
 * display some text on the window
 */
Simulation.prototype.writeText = function (txt, xP = 50, yP = 50) {
  this.ctx.fillStyle = "black";
  this.ctx.font = "14px monospace";
  this.ctx.fillText(txt, xP, yP);
}