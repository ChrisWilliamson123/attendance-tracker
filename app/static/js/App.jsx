import Quagga from 'quagga';
import React, { Component } from 'react';
import Header from './Header';
import Scanner from './Scanner';

require('../css/App.css');

class App extends Component {
  constructor() {
    super();
    
    this.state = {
      attendance: 0
    }
  }

  incrementAttendance = () =>
    this.setState({
      attendance: this.state.attendance + 1
    });

  render() {
    return (
      <div className="App">
        <Header />
        <div className="container">
          <h3>Current attendance: {this.state.attendance}</h3>
          <Scanner
            incrementAttendance={this.incrementAttendance}
          />
        </div>
      </div>
    );
  }
}

export default App;
