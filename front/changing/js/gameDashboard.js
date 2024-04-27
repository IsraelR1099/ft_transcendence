async function createRoom() {
	const roomName = document.getElementById('roomName').value;
	if (!roomName) {
		alert('Please enter a room name');
		return;
	}
	try {
		const response = await fetch('/api/tictac/create_join/', {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({ room_code: roomName, option: "create" })
		});
		const data = await response.json();
		if (response.ok) {
			console.log("Room created:", data);
			redirectToGamePage(data);
		}
		else {
			console.error("Failed to create room:", data.error);
			alert(data.error);
		}
	}
	catch (error) {
		console.error("Failed to create room:", error);
		alert("Failed to create room");
	}
}

async function joinRoom() {
	const roomCode = document.getElementById('roomCode').value;
	console.log('roomCode es ' + roomCode);
	if (!roomCode) {
		alert('Please enter a room code');
		return;
	}
	try {
		const response = await fetch('/api/tictac/create_join/', {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({ room_code: roomCode, option: "join" })
		});
		const data = await response.json();
		if (response.ok) {
			if (data.error) {
				console.error("Failed to join room:", data.error);
				alert(data.error);
				return;
			}
			console.log("Room joined:", data);
			redirectToGamePage(data);
		}
		else {
			console.error("Failed to join room:", data.error);
			alert(data.error);
		}
	}
	catch (error) {
		console.error("Failed to join room:", error);
		alert("Failed to join room");
	}
}

function redirectToGamePage(roomInfo) {
	const queryParams = new URLSearchParams(roomInfo).toString();
	//window.location.href = `./pages/waitingRoom.html?${queryParams}`;
	window.location.href = `../pages/game.html?${queryParams}`;
}
