import Quagga from 'quagga';
import React, { Component } from 'react';
import Header from './Header';
import Scanner from './Scanner';
import Header from './Header';

require('../css/App.css');

Quagga.onProcessed(function(result) {
  const canvas = document.querySelector(".drawingBuffer"),
        canvasContext = canvas.getContext("2d");

  if (result) {
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
        <Header />
        <Scanner
          incrementAttendance={this.incrementAttendance}
          attendance={this.state.attendance}
        />
      </div>
    );
  }
}

export default App;
