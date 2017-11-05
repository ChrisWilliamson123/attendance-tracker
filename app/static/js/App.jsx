import Quagga from 'quagga';
import React, { Component } from 'react';
import Header from './Header';
import Scanner from './Scanner';

require('../css/App.scss');

class App extends Component {
  constructor() {
    super();
    
    this.state = {
      attendance: 0,
      entries: []
    }
  }

  incrementAttendance = () =>
    this.setState((prevState, props) => ({
      attendance: this.state.attendance + 1,
      entries: prevState.entries.concat([new Date()])
    }));

  getReadableDate = date =>
    `${date.getDate()}/${date.getMonth()+1}/${date.getFullYear()} at ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;

  getLastInTime = () => {
    const entries = this.state.entries;
    if (entries.length > 0) {
      return this.getReadableDate(entries[entries.length-1]);
    }
    return 'N/A'
  }

  render() {
    return (
      <div className="App">
        <Header />
        <div className="container">
          <div className="stats">
            <h3>Current attendance: {this.state.attendance}</h3>
            <h4>Last in: {this.getLastInTime()}</h4>
          </div>
          <Scanner
            incrementAttendance={this.incrementAttendance}
          />
        </div>
      </div>
    );
  }
}

export default App;
