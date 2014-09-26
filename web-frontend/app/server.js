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

io.sockets.on('connection', function (socket) {
	socket.emit('news', { hello: 'world' });
	socket.on('my other event', function (data) {
		console.log(data);
	});
});

app.get('/hello', function(req, res){
    // res.send('hello!');
    res.send('bonjour!');
});
// use livereload middleware
app.use(require('grunt-contrib-livereload/lib/utils').livereloadSnippet);

exports = module.exports = server;

exports.use = function() {
	app.use.apply(app, arguments);
};
