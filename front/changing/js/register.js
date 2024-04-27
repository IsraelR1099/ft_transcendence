import { fetchAccountData } from './fetchUser.js';

document.addEventListener('DOMContentLoaded', function() {
	const registerForm = document.getElementById('registerForm');
	async function registerUser(email, username, password1, password2) {
		try {
			const response = await fetch('/api/user/register/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					email,
					username,
					password1,
					password2,
				}),
			});

			const data = await response.json();
			if (response.ok) {
                if (data.error) {
                    console.error("Register failed: ", data.error);
                    alert(data.error);
                    return;
                }
				console.log(data);
				localStorage.setItem('userData', JSON.stringify(data));
				await fetchAccountData(data.id);
			}
			else {
				console.error("Register failed: ", data.error);
			}
		} catch (error) {
			console.error('Error:', error);
		}
	}

	registerForm.addEventListener('submit', async function(event) {
		event.preventDefault();
		const email = document.getElementById('inputEmail').value;
		const username = document.getElementById('inputUsername').value;
		const password1 = document.getElementById('inputPassword1').value;
		const password2 = document.getElementById('inputPassword2').value;
        console.log('Registering user with email: ', email, ' username: ', username, ' password1: ', password1, ' password2: ');
		await registerUser(email, username, password1, password2);
	});
});
