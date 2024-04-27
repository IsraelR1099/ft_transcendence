import { fetchAccountData } from './fetchUser.js';

document.addEventListener('DOMContentLoaded', function() {
	const loginForm = document.getElementById('loginForm');
	async function loginUser(username, password) {
		try {
			const response = await fetch('/api/user/login/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ username, password }),
			});

			const data = await response.json();
			if (data.error) {
				console.error("Login failed: ", data.error);
				alert (data.error['__all__'][0]);
			}
			else if (response.ok) {
				console.log("Login successful");
				localStorage.setItem('userData', JSON.stringify(data));
				await fetchAccountData(data.id);
			}
			else {
				console.error("Login failed: ", data);
				alert ("Login failed");
			}
		} catch (error) {
			console.error("Login failed: ", error);
			alert ("Login failed");
		}
	}

	loginForm.addEventListener('submit', async function(event) {
		event.preventDefault();
		const username = document.getElementById('username').value;
		const password = document.getElementById('password').value;
		await loginUser(username, password);
	});
});
