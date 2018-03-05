import React, { Component } from "react";

import { Form, Menu, Dialog, Separator ,Box, render, Window, App, Grid, Button, TextInput } from "proton-native";

class Example extends Component {
	render() {
		return (
			<App>
				<Window title="Example" size={{w: 500, h: 500}}>
					
					<Grid padded={true}>
						<Form padded={true} row={0} column={0}>
							<TextInput label="Username" />
							<TextInput label="Password" secure={true} />
						</Form>
						<Separator/>
						<Button row={0} column={3}>
							SUBMIT
						</Button>
					</Grid>
					
				</Window>
			</App>
		);
	}
}

render(<Example />);