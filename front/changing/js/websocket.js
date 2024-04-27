document.addEventListener('DOMContentLoaded', function() {
	const startConnectionBtn = document.getElementById('startConnection');
	let websocket;

	startConnectionBtn.addEventListener('click', function() {
		if ('WebSocket' in window) {
			websocket = new WebSocket('wss://pong.xyz/api/ws/chat/');
			websocket.onopen = function() {
				console.log("WebSocket connection established.");
			};
			websocket.onmessage = function(event) {
				console.log("Message received: ", event.data);
			};
			websocket.onclose = function(event) {
				console.log("WebSocket connection closed: ", event);
			};
			websocket.onerror = function(event) {
				console.log("WebSocket error: ", event);
			};
		} else {
			console.log("WebSocket is not supported");
		}
	});
});

