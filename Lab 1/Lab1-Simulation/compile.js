var NwBuilder = require('C:/Users/dena1/AppData/Roaming/npm/node_modules/nw-builder');

var nw = new NwBuilder({
    files: ['C:/Users/dena1/Dropbox/researches/ece813/project simulations/project1sim/*'
], // use the glob format
    platforms: ['win64'],
    flavor: 'normal',
    appName: 'lab1sim',
    version: '0.14.7',
    production: true
});

// Log stuff you want
nw.on('log',  console.log);

nw.build().then(function () {
   console.log('all done!');
});