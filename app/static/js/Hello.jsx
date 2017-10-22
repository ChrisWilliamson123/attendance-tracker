import React from 'react';
import { Button } from 'react-bootstrap';
import $ from 'jquery';

class Hello extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            greeting: 'Hello ' + this.props.name
        };

        this.getPythonHello = this.getPythonHello.bind(this);
    }

    getPythonHello() {
        $.get(window.location.href + 'hello', data => {
            console.log(data);
            this.personaliseGreeting(data);
        });
    }

    personaliseGreeting(greeting) {
        this.setState({
            greeting: greeting + ' ' + this.props.name + '!'
        });
    }

    render() {
        return (
            <div>
                <h1>{this.state.greeting}</h1>
                <hr/>
                <Button bsSize='large' bsStyle='danger' onClick={this.getPythonHello}>
                    Say Hello!
                </Button>
            </div>
        )
    }
}

export default Hello;