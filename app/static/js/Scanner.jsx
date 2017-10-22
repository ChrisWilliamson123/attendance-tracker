import Quagga from 'quagga';
import React, { Component } from 'react';

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

export default Scanner;