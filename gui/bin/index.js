"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _react = require("react");

var _react2 = _interopRequireDefault(_react);

var _protonNative = require("proton-native");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; } // import from react

// import the proton-native components

var PasswordManager = function (_Component) {
	_inherits(PasswordManager, _Component);

	function PasswordManager() {
		_classCallCheck(this, PasswordManager);

		return _possibleConstructorReturn(this, (PasswordManager.__proto__ || Object.getPrototypeOf(PasswordManager)).apply(this, arguments));
	}

	_createClass(PasswordManager, [{
		key: "render",
		value: function render() {
			// all Components must have a render method
			return _react2.default.createElement(
				_protonNative.App,
				null,
				" // you must always include App around everything",
				_react2.default.createElement(
					_protonNative.Window,
					{ title: "Proton Native", size: { w: 500, h: 500 } },
					"// all your other components go here",
					_react2.default.createElement(
						Box,
						null,
						_react2.default.createElement(
							Button,
							null,
							"Hello"
						),
						_react2.default.createElement(TextInput, null)
					)
				)
			);
		}
	}]);

	return PasswordManager;
}(_react.Component);

(0, _protonNative.render)(_react2.default.createElement(PasswordManager, null)); // and finally render your main component