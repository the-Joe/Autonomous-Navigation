// SIMULATION STARTUP
$(document).ready(function(){
    gui = require('nw.gui');
    express = require("express");

    win = gui.Window.get();
    app = express();

    //window dimensions
    win.width  = 760; 
    win.height = 570;
    
    win.on("loaded",function() {
        mc = new MainController("#navBar", win);
    });

    
    // listen to main window's close event
    win.on('close', function() {
        // hide the window to give the user the feeling of closing immediately
        this.hide();

        // do on close event
        this.close(true);

    });
    
});

/**
 * The main controller for the simulation app
 * @param elemNavId The selector to use
 * @param nwWin The node webkit window
 */
function MainController(elemNavId) {
    var that = this;
    this.navElement = $(elemNavId);
    this.simulationInstance = new Simulation("simArea");

    this.mouseEnabled = false;
    this.buttonRestart = $(elemNavId + ' #restart');
    this.buttonClose = $(elemNavId + ' #close');
    this.buttomMouseToggle = $(elemNavId + " #mouse");

    this.initialize();
}

//Constructor
MainController.prototype.initialize = function() {
    var that = this;
    //initialize the buttons
    //restart the simulation
    that.buttonRestart.unbind().click(function(e) {
        that.simulationInstance.restart();
    });
    //close the window
    that.buttonClose.unbind().click(function(e) {
        gui.App.quit();
    });

    that.buttomMouseToggle.unbind().click(function(e) {
        that.mouseEnabled = !that.mouseEnabled;
        that.simulationInstance.mouseToggle(that.mouseEnabled);
        if (that.mouseEnabled) {
            that.buttomMouseToggle.text("Disable Mouse");
        } else {
            that.buttomMouseToggle.text("Enable Mouse");
        }
    })

}