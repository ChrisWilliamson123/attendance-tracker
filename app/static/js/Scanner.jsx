import Quagga from 'quagga';
import React, { Component } from 'react';
import ButtonToolbar from 'react-bootstrap/lib/ButtonToolbar';
import Button from 'react-bootstrap/lib/Button';
import Grid from 'react-bootstrap/lib/Grid';
import Row from 'react-bootstrap/lib/Row';
import Col from 'react-bootstrap/lib/Col';
import { quaggaConfig } from './utils';

class Scanner extends React.Component {
  constructor() {
    super();

    Quagga.onDetected(result => this.handleDetectedBarcode(result));

    Quagga.onProcessed(result => {
      const canvas = this.canvas,
      canvasContext = canvas.getContext("2d");

      if (result) {
        if (result.boxes) {
          canvasContext.clearRect(0, 0, parseInt(canvas.getAttribute("width"), 10), parseInt(canvas.getAttribute("height"), 10));
          result.boxes.filter(box => {
            return box !== result.box;
          }).forEach(box => 
            Quagga.ImageDebug.drawPath(box, {x: 0, y: 1}, canvasContext, {color: "green", lineWidth: 2})
          );
        }

        if (result.box) {
          Quagga.ImageDebug.drawPath(result.box, {x: 0, y: 1}, canvasContext, {color: "#00F", lineWidth: 2});
        }

        if (result.codeResult && result.codeResult.code) {
          Quagga.ImageDebug.drawPath(result.line, {x: 'x', y: 'y'}, canvasContext, {color: 'red', lineWidth: 3});
        }
      }
    });

    this.state = {
      scanning: false
    }
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.state.scanning) {
      Quagga.init(quaggaConfig, err => {
        if (err) throw err;
        Quagga.start();
      });
    }
    else if (prevState.scanning === true) {
      Quagga.stop();
    }
  }

  handleDetectedBarcode = barcode => {
    this.setState({scanning: false});
    this.props.incrementAttendance();
  }

  startScanning = () => {
    if (!this.state.scanning) this.setState({scanning: true});
  }

  render() {
    return (
      <Grid>
        <Row>
          <Col xs={12}>
            <div className="text-center">
              <Button bsSize="large" onClick={this.startScanning}>Start Scanning</Button>
            </div>
          </Col>
        </Row>
        { this.state.scanning ?
          <Row>
            <Col xs={12}>
              <div id="interactive" className="viewport">
                <video autoPlay="true" preload="auto" src="" muted="true" playsInline="true"></video>
                <canvas className="drawingBuffer" width="0" height="0" ref={canvas => {this.canvas = canvas}}></canvas>
              </div>
            </Col>
          </Row>
          : null 
        }
      </Grid>
    );
  }
}

export default Scanner;