import Quagga from 'quagga';
import React, { Component } from 'react';
import ButtonToolbar from 'react-bootstrap/lib/ButtonToolbar';
import Button from 'react-bootstrap/lib/Button';
import Grid from 'react-bootstrap/lib/Grid';
import Row from 'react-bootstrap/lib/Row';
import Col from 'react-bootstrap/lib/Col';
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
        <Grid>
            <Row>
                <Col xs={12}>
                    <div className="text-center">
                        <Button bsSize="large" onClick={this.startScanning}>Start Scanning</Button>
                    </div>
                </Col>
            </Row>
            <Row>
                <Col xs={12}>
                    <div id="interactive" className="viewport">
                        <video autoPlay="true" preload="auto" src="" muted="true" playsInline="true"></video>
                        <canvas className="drawingBuffer" width="0" height="0"></canvas>
                    </div>
                </Col>
            </Row>
        </Grid>
      );
}
}

export default Scanner;