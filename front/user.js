//<td>${userData.token_access}</td>
//<td>${userData.token_refresh}</td>
document.addEventListener('DOMContentLoaded', function () {
	const logoutButton = document.getElementById('logoutButton');
	const userTable = document.getElementById('userTable');

	function handleLoginData() {
		const userData = JSON.parse(localStorage.getItem('userData'));

		if (userData) {
			const row = `
			<tr>
                <td>${userData.code}</td>
				<td>${userData.id}</td>
				<td>${userData.email}</td>
				<td>${userData.username}</td>
				<td>${userData.password}</td>
				<td>${userData.status}</td>
				<br>
				<td><img src="data:image/png;base64,${userData.profile_image_base64}" alt="profile image"></td>
			</tr>
			`;
			userTable.innerHTML = row;
		}
	}

	async function logoutUser() {
		try {
			const userData = JSON.parse(localStorage.getItem('userData'));
			if (!userData) {
				console.error('No user data found.');
				return;
			}

			const response = await fetch('/api/user/logout/', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json',
					'Accept': 'application/json',
					'Authorization': `Bearer ${userData.token_access}`,
				},
				body: JSON.stringify({
					refresh_token: userData.token_refresh
				})
			});

			if (response.ok) {
				localStorage.removeItem('userData');
        			window.location.href = 'index.html';
			}
			else {
				console.error('Failed to log out.');
			}
		} catch (error) {
			console.errror('Error during logout.', error);
		}
	}


	function redirectToEditProfile() {
		window.location.href = 'edit.html';
	}

 	logoutButton.addEventListener('click', async function (event) {
		event.preventDefault();
		await logoutUser();
	});

	editButton.addEventListener('click', function (event) {
		event.preventDefault();
		redirectToEditProfile();
	});

	handleLoginData();
});

// Assume you have a function to retrieve the user's email
// Replace getUserEmail() with the actual function to get the user's email
