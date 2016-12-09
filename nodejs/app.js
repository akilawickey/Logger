/*Http server*/
var express = require("express");
var app = express();
var http = require('http').Server(app);
var path = __dirname + '/';
var io = require('socket.io')(http);
var router = express.Router();
var csvWriter = require('csv-write-stream')
var writer = csvWriter({sendHeaders: false})
var fs = require('fs');


/*Socket IO*/
router.use("/",function(req,res){
  res.sendFile(path + "index.html");
});

app.use("/",router);
app.use(express.static(__dirname + '/public'));

/*Serial Port Intitiate*/
var SerialPort = require('serialport');

/*Validation Flag*/
var flag_V = 0;

var port = new SerialPort("/dev/ttyUSB0", {
  // baudrate: 9600,
  baudrate: 115200,
  bufferSize: 1 ,
  rtscts: true ,

  //parser: port.parsers.readline("\n")
});

/*Open data from COM6*/
// port.open(function (err) {
//   console.log('SerialPort Opened');
//   if (err) {
//     return console.log('Error opening port: ', err.message);
//   }
//   // Send data through COM6.
//   // port.write('main screen turn on');
// });

function myPrint(data) {
	// console.log("-----------------------------------" + data.length);
	var i;
	// for (i=0;i<data.length;i++){
 //    	console.log('Data: ' + data[i]);
 //  	}
 	console.log('Data: ' + data);
  writer.write(data);
}

   // writer.end()

function validateData(x){
	if(x != "#"){
		port.flush();
	}else if( x == "#"){
		flag_V=1;
		console.log("Validated");
	}
}


var str = "";
var count=0;
var no_pkt = 0;
port.on('data', function (data) {

// myPrint(data.toString('hex'));
// myPrint(data);

  if(flag_V == 0) validateData(data) ;
  else{
  	str += data;

  	// if(count == 100){
  	// 	myPrint(str);
  	// 	count = 0;
  	// 	io.emit('chat message', str);								//send msg to web interface.
  	// 	str=""
  	// 	flag_V = 0;
  	// 	no_pkt++;
  	// 	console.log("Packet Number :" + no_pkt);
  	// }

  	if(data == "!"){ 	
  		myPrint(str);
  		count = 0;
  		io.emit('chat message', str);								//send msg to web interface.
  		str=""
  		flag_V = 0;
  		no_pkt++;
  		console.log("Packet Number :" + no_pkt);
  	}
  	
  	count++;
  }

  // var waitTill = new Date(new Date().getTime() + 1 * 1000);
  // while(waitTill > new Date()){}
});

/*Create http server*/
app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  console.log('User connected');
  socket.on('chat message', function(msg){
    // console.log('message: ' + msg);
    // io.emit('chat message', msg);
  });

    socket.on('disconnect', function(data) {
        console.log('-----------------disconnected the socket!-------------');
    });

  // socket.on('disconnect', function(){
  //   console.log('user disconnected');
  // });
});

http.listen(4001, function(){
  console.log('listening on :4001');
  console.log('--------------------------------------------------------------');
  console.log('-------------------------TEAM VEGA----------------------------');
  console.log('--------------------------------------------------------------');
  writer.pipe(fs.createWriteStream('out.csv'))


});

