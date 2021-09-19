// SIMULATION STARTUP
$(document).ready(function(){
    gui = require('nw.gui');
    express = require("express");

    win = gui.Window.get();
    app = express();

    //window dimensions
    win.width  = 650; 
    win.height = 500;
    
    mc = new MainController("#navBar", win);
    
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

    this.buttonRestart = $(elemNavId + ' #restart');
    this.buttonClose = $(elemNavId + ' #close');

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

}