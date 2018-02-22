import React from 'react'
// same as var React = require('react');
import { render, } from 'react-dom'
// same as var render = require('react-dom').render;
import App from '../components/App'

render(
	// define the encompassing component,
	// DOM element we want to mount it to
	<App/>, 
	document.getElementById('app')
)