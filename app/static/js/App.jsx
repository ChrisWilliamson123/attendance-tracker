import Quagga from 'quagga';
import React, { Component } from 'react';

require('../css/App.css');
require('../css/fullstack.css');

Quagga.onProcessed(function(result) {
  const canvas = document.querySelector(".drawingBuffer"),
        canvasContext = canvas.getContext("2d");

  if (result) {
    console.log('here');
    if (result.boxes) {
      canvasContext.clearRect(0, 0, parseInt(canvas.getAttribute("width"), 10), parseInt(canvas.getAttribute("height"), 10));
      result.boxes.filter(function (box) {
        return box !== result.box;
      }).forEach(function (box) {
        Quagga.ImageDebug.drawPath(box, {x: 0, y: 1}, canvasContext, {color: "green", lineWidth: 2});
      });
    }

    if (result.box) {
      Quagga.ImageDebug.drawPath(result.box, {x: 0, y: 1}, canvasContext, {color: "#00F", lineWidth: 2});
    }

    if (result.codeResult && result.codeResult.code) {
      Quagga.ImageDebug.drawPath(result.line, {x: 'x', y: 'y'}, canvasContext, {color: 'red', lineWidth: 3});
    }
  }
});

class App extends Component {
  constructor() {
    super();

    this.state = {
      attendance: 0
    }

    Quagga.onDetected(result => {
      this.incrementAttendance();
      Quagga.stop();
    });
  }

  incrementAttendance = () =>
    this.setState({
      attendance: this.state.attendance + 1
    });

  render() {
    return (
      <div className="App">
        <h1>Attendance Tracker</h1>
        <p>Attendance: {this.state.attendance}</p>
        <Scanner
          incrementAttendance={this.incrementAttendance}
        />
      </div>
    );
  }
}

class Scanner extends React.Component {

  processImage = (changeEvent) => {
    this.props.incrementAttendance();
  }

  startScanning = () => {
    Quagga.init({
      inputStream : {
        name : "Live",
        type : "LiveStream"
      },
      decoder : {
        readers : ["code_128_reader"]
      }
    }, function(err) {
      if (err) {
          console.log(err);
          throw err;
      }
      console.log("Initialization finished. Ready to start");
      Quagga.start();
    });
  }

  render() {
    return (
      <div>
        <button onClick={this.startScanning}>Start scanning</button>
        <input
          type="file"
          accept="image/*"
          capture="camera"
          onChange={this.processImage}
          className="cameraInput"
        />
        <div id="interactive" className="viewport">
          <video autoPlay="true" preload="auto" src="" muted="true" playsInline="true"></video>
          <canvas className="drawingBuffer" width="640" height="480"></canvas>
        </div>
      </div>
    );
  }
}

export default App;
