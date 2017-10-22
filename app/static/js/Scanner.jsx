import Quagga from 'quagga';
import React, { Component } from 'react';
import { quaggaConfig } from './utils';

class Scanner extends React.Component {

  processImage = () =>
    this.props.incrementAttendance();

  startScanning = () =>
    Quagga.init(quaggaConfig, err => {
      if (err) throw err;
      Quagga.start();
    });

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