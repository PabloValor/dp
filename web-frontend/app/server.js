'use strict';

var express = require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io').listen(server);
var consolidate = require('consolidate');

app.engine('dust', consolidate.dust);
app.set('view engine', 'dust');
app.set('views', './app/templates');

app.use(app.router);
app.use('/public', express.static(__dirname + "/../public"));

var redis = require('socket.io/node_modules/redis');
var sub = redis.createClient();

sub.subscribe('notifications');

io.sockets.on('connection', function (socket) {
    console.log('conectando');
    sub.on('message', function(channel, response) {
        var message = JSON.parse(response);
        console.log(message.listener_id);
        console.log(message['notification']);
        console.log('000');
        socket.emit(message.listener_id, message.notification);
        console.log('enviado');
    });
});


app.get('/hello', function(req, res){
    res.send('bonjour!');
});

// use livereload middleware
app.use(require('grunt-contrib-livereload/lib/utils').livereloadSnippet);

exports = module.exports = server;

exports.use = function() {
	app.use.apply(app, arguments);
};
