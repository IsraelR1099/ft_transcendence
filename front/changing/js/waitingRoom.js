document.addEventListener('DOMContentLoaded', function() {
	const	queryParams = new URLSearchParams(window.location.search);
	const	room_code = queryParams.get('room_code');
	if (!room_code) {
		alert("No room_code provided");
		return ;
	}
	async function	waiting() {
		try {
			const response = await fetch('/api/tictac/play/' + room_code + '/', {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				});
			const	data = await response.json();
			if (response.ok) {
				if (data.error) {
					console.error("Failed to fetch play room: ", data.error);
					alert(data.error);
					return ;
				}
				console.log("data is: ", data);
			} else {
				console.error("Failed to fetch information: ", data.error);
				alert(data.error);
			}
			}
		} catch (error) {
			console.log("Failed : ", error);
			alert("Failed");
		}
	}
});
