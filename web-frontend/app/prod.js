'use strict';

var express = require('express');
var app = express();
var server = require('http').createServer(app);

server.listen(3000)

var io = require('socket.io').listen(server);

app.engine('html', require('ejs').renderFile);
app.set('views', __dirname + '/../public');

app.use(app.router);
app.use('/public', express.static(__dirname + "/../public"));
app.use('/scripts', express.static(__dirname + "/../public/scripts"));
app.use('/views', express.static(__dirname + "/../public/views"));

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


app.get('/', function(req, res){
    res.render('index.html');    
});

app.use(function(req, res) {
    res.status(404).render('404.html');
});

// use livereload middleware
app.use(require('grunt-contrib-livereload/lib/utils').livereloadSnippet);

exports = module.exports = server;

exports.use = function() {
	app.use.apply(app, arguments);
};

