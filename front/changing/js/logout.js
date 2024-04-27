document.addEventListener('DOMContentLoaded', function() {
	const logoutButton = document.getElementById('logoutButton');
	async function logoutUser() {
		try {
			const userData = JSON.parse(localStorage.getItem('userData'));
			if (!userData) {
				alert('You are not logged in');
				return;
			}

			const response = await fetch('/api/user/logout/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Accept': 'application/json',
				},
			});
			if (response.ok) {
				localStorage.removeItem('userData');
				window.location.href = '../index.html';
			} else {
				alert('Failed to logout');
			}
		} catch (error) {
			console.error(error);
			alert('Failed to logout');
		}
	}
	logoutButton.addEventListener('click', async function(event) {
		event.preventDefault();
		await logoutUser();
	});
});
