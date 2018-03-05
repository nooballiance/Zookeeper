import React, { Component } from "react"; // import from react

import { render, Window, App, Box, Button, TextInput } from "proton-native"; // import the proton-native components

class PasswordManager extends Component {
	render() { // all Components must have a render method
		return (
			<App> // you must always include App around everything
			<Window title="Proton Native" size={{w: 500, h: 500}}>
			// all your other components go here
				<Box>
					
					<TextInput />
					<Button>Enter</Button>
					<Button>Exit</Button>
				</Box>
			</Window>
			</App>
		);
	}
}

render(<PasswordManager />); // and finally render your main component
