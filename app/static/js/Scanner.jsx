import axios from 'axios';
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
      scanning: false,
      error: ''
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
    console.log(barcode);
    const code = parseInt(barcode.codeResult.code);
    const direction = 'IN';
    this.setState({scanning: false});
    axios.get('/api/check_ticket', {
      params: {
        ticket_id: code,
        direction: direction
      }
    })
    .then(response => {
      console.log(response);
      if (response.data.action === 1) {
        this.props.incrementAttendance();
      }
      else this.handleRejectedBarcode(response.data.message);
    })
    .catch(error => console.log(error))
  }

  handleRejectedBarcode = (errorMessage) => {
    this.setState({error: errorMessage});
  }

  startScanning = () => {
    if (!this.state.scanning) this.setState({scanning: true, error: ''});
  }

  getScanButtonText = () => this.state.error.length ? 'Scan Again' : 'Start Scanning';

  render() {
    return (
      <div>
        { this.state.scanning ?
          <Row>
            <Col xs={12}>
              <div id="interactive" className="viewport">
                <video autoPlay="true" preload="auto" src="" muted="true" playsInline="true"></video>
                <canvas className="drawingBuffer" width="0" height="0" ref={canvas => {this.canvas = canvas}}></canvas>
              </div>
            </Col>
          </Row>
          :
          <Row>
            <Col xs={12}>
              <div className="text-center">
                <Button bsSize="large" onClick={this.startScanning}>{this.getScanButtonText()}</Button>
                {this.state.error.length ? <p>Error: {this.state.error}</p> : null}
              </div>
            </Col>
          </Row>
        }
      </div>
    );
  }
}

export default Scanner;