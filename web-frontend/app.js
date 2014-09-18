var express =require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io').listen(server);

app.configure(function() {
    app.set('port', process.env.PORT || 3333)
    app.use(express.bodyParser());
    app.use(express.methodOverride());

    app.use(app.router);
    app.use(express.static(__dirname + "/dist"));
});


io.on('connection', function (socket) {
  socket.emit('news', { hello: 'world' });
  socket.on('my other event', function (data) {
    console.log(data);
  });
});

server.listen(app.get('port'), function() {
    console.log("Express server listening on port " + app.get('port'));
});
