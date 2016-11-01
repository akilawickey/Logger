var SerialPort = require('serialport');
var port = new SerialPort('/dev/ttyUSB0', { autoOpen: false });


var express = require('express');
var app = express();


app.get('/', function (req, res) {
	var a = "ado"
  res.send(a);
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});


port.open(function (err) {

  console.log('SerialPort Opened');
  if (err) {
    return console.log('Error opening port: ', err.message);
  }
  // write errors will be emitted on the port since there is no callback to write
  // port.write('main screen turn on');
});

port.on('data', function (data) {
  console.log('Data: ' + data);
});

// var ws = require("nodejs-websocket")
 
// // Scream server example: "hi" -> "HI!!!" 
// var server = ws.createServer(function (conn) {
// 	console.log('Server running at http://127.0.0.1:8001/');
//     console.log("New connection")
//     conn.on("text", function (str) {
//         console.log("Received "+str)
//         conn.sendText(str.toUpperCase()+"!!!")
//     })
//     conn.on("close", function (code, reason) {
//         console.log("Connection closed")
//     })
// }).listen(8001)

var http = require("http");

http.createServer(function(request, response) {
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("Connected");
  response.end();
}).listen(8888);
