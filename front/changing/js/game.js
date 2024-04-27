document.addEventListener('DOMContentLoaded', function() {
	const queryParams = new URLSearchParams(window.location.search);

	const	creator = queryParams.get('creator');
	const	opponent = queryParams.get('opponent');
	const	room_code = queryParams.get('room_code');
	let	player = JSON.parse(localStorage.getItem('userData'));
	player = player.username;
	document.getElementById('player1Name').textContent = creator || 'Unknown';
	document.getElementById('player2Name').textContent = opponent || 'Unknown';
	let	websocket;
	let	gameState = [ "", "", "", "", "", "", "", "", "" ];
	let	elementArray = document.querySelectorAll('.cell');

	websocket = new WebSocket('wss://pong.xyz/api/ws/game/' + room_code + '/');
	elementArray.forEach(function (element) {
		element.addEventListener('click', function(event) {
			const cellId = event.target.id;
			const value = (player == creator) ? 'X' : 'O';
			console.log('player from local storage: ' + player);
			console.log('value before setText: ' + value);
			setText(cellId, value);
			elementArray.forEach(function(cell) {
				cell.removeEventListener('click', handleClick);
			});
		});
	});

	function	checkGameEnd() {
		var count = 0;
		gameState.map((game) => {
			if (game != '') {
				count++;
			}
		})
		if (count >= 9) {
			var	data = {
				'type': 'over',
			}
			websocket.send(JSON.stringify({data}));
			Swal.fire("Game Over", "It's a draw", "warning");
		}
	}

	function	checkWon(value, player) {
		var	won = false;
		if (gameState[0] === value && gameState[1] == value && gameState[2] == value) {
			won = true;
		} else if (gameState[3] === value && gameState[4] == value && gameState[5] == value) {
			won = true;
		} else if (gameState[6] === value && gameState[7] == value && gameState[8] == value) {
			won = true;
		} else if (gameState[0] === value && gameState[3] == value && gameState[6] == value) {
			won = true;
		} else if (gameState[1] === value && gameState[4] == value && gameState[7] == value) {
			won = true;
		} else if (gameState[2] === value && gameState[5] == value && gameState[8] == value) {
			won = true;
		} else if (gameState[0] === value && gameState[4] == value && gameState[8] == value) {
			won = true;
		} else if (gameState[2] === value && gameState[4] == value && gameState[6] == value) {
			won = true;
		}
		if (won) {
			var	data = {
				'type': 'end',
				'player': player,
			}
			websocket.send(JSON.stringify({
				data
			}));
			Swal.fire("Good job!", "Player " + player + " won", "success");
		}

		checkGameEnd();
	}
	function	setText(index, value) {
		console.log('Setting value: ' + value + ' at index: ' + index);
		var	data = {
			'index': index,
			'player': player,
			'type': 'running'
		}
		if (gameState[parseInt(index)] == '') {
			gameState[parseInt(index)] = value;
			elementArray[parseInt(index)].innerHTML = value;
			websocket.send(JSON.stringify({
				data
			}));
			checkWon(value, player);
		} else {
			alert('You cannot fill this cell');
		}
		setTimeout(function() {
			elementArray.forEach(function(cell) {
				cell.addEventListener('click', handleClick);
			});
		}, 100000);
	}

	function	setAnotherUserText(index, value) {
		console.log('Setting value: ' + value + ' at index: ' + index);
		console.log('creator: ' + creator + ' opponent: ' + opponent);
		let	value2;
		if (value == creator) {
			value2 = 'X';
		}
		if (value == player) {
			value2 = 'O';
		}
		gameState[parseInt(index)] = value2;
		elementArray[parseInt(index)].innerHTML = value2;
	}

	websocket.onopen = function(event) {
		console.log('Connected to the websocket server');
	}
	websocket.onmessage = function(event) {
		var	data = JSON.parse(event.data);

		if (data.payload.type == 'end' && data.payload.player !== player) {
			Swal.fire("Game Over", "Player " + data.payload.player + " won", "error").then((result) => {
			if (result.isConfirmed) {
				const	winner = data.payload.player;
				let	loser;
				if (winner != player ) {
					loser = player;
				} else {
					loser = opponent;
				}
				const	game = 'Tic Tac Toe';
				const	match = {
					'winner': winner,
					'loser': loser,
					'game_type': game,
					'room_code': room_code,
				};

				fetch('/api/user/save_match/', {
					method: "POST",
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify(match),
				})
				.then((response) => response.json())
				.then((data) => {
					console.log('Match result saved: ', data);
				})
				.catch((error) => {
					console.error('Error saving match result:', error);
				});
			}
		});
		} else if (data.payload.type == 'over') {
			Swal.fire("Game Over", "It's a draw", "warning").then((result) => {
			if (result.isConfirmed) {
				const	winner = 'Draw';
				const	loser = 'Draw';
				const	game = 'Tic Tac Toe';
				const	match = {
					'winner': winner,
					'loser': loser,
					'game': game,
					'room_code': room_code,
				};

				fetch('/api/user/save_match/', {
					method: "POST",
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify(match),
				})
				.then((response) => response.json())
				.then((data) => {
					console.log('Match result saved: ', data);
				})
				.catch((error) => {
					console.error('Error saving match result:', error);
				});
			}
			return;
			});
		} else if (data.payload.type == 'running' && data.payload.player !== player) {
			setAnotherUserText(data.payload.index, data.payload.player);
		}
	}
	websocket.onclose = function(event) {
		console.log('Disconnected from the websocket server');
	}

	function	handleClick(event) {
		const cellId = event.target.id;
		const value = (player == creator) ? 'X' : 'O';
		console.log('value before setText: ' + value);
		setText(cellId, value);
		elementArray.forEach(function(cell) {
			cell.removeEventListener('click', handleClick);
		});
	}

	elementArray.forEach(function (element) {
		element.addEventListener('click', handleClick);
	});

});
