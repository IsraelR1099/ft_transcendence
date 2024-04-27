document.addEventListener('DOMContentLoaded', function() {
	const	userData = JSON.parse(localStorage.getItem('userData'));
	const	pk = userData.id;

	fetchMatchHistory(pk)
		.then(data => {
			console.log("data is: ", data);
			const matchHistoryArray = Array.isArray(data) ? data : [data];
			displayMatchHistory(matchHistoryArray);
		})
		.catch(error => {
			console.error(error);
		});
});

function fetchMatchHistory(pk) {
	return fetch(`/api/user/match_history/${pk}/`)
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
}

function displayMatchHistory(matchHistory) {
	const gameHistory = document.getElementById('gameHistoryTable');
	gameHistory.innerHTML = '';

	matchHistory.forEach(match => {
		const row = document.createElement('tr');
		row.innerHTML = `
			<td>${match.winner}</td>
			<td>${match.loser}</td>
			<td>${match.game_type}</td>
			<td>${match.room_code}</td>
			<td>${match.date}</td>
			<td>${match.result}</td>
		`;
		gameHistory.appendChild(row);
	});
}
