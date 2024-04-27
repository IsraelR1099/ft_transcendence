import { fetchAccountData } from './fetchUser.js';

document.addEventListener('DOMContentLoaded', function() {
	const editForm = document.getElementById('editForm');
	const editButton = document.getElementById('editButton');

	editForm.addEventListener('submit', async function(event) {
		event.preventDefault();
		const userData = JSON.parse(localStorage.getItem('userData'));
		const email = document.getElementById('email').value;
		const username = document.getElementById('username').value;
		if (!email && !username) {
			return alert('Please enter email or username');
		}
		const profileImageInput = document.getElementById('profileImage');
		const profile_image = profileImageInput.files[0];
//		if (!profile_image) {
//			return alert('Please select an image');
//		}
		try {
			if (!userData) {
				return alert('Please log in');
			}
			const formData = new FormData();
			formData.append('email', email);
			formData.append('username', username);
			formData.append('profile_image', profile_image);
			console.log("email: ", email);
			console.log("username: ", username);
			const response = await fetch(`/api/user/account/${userData.id}/edit/`, {
				method: 'POST',
				headers: {
				},
				body: formData,
			});
			const data = await response.json();
			if (response.ok) {
				if (data.error) {
					console.error('Failed to edit profile', data.errors);
					return alert('Failed to edit profile');
				}
				console.log('Profile edited', data);
				await fetchAccountData(userData.id);
				window.location.href = '../pages/user_profile.html';
			}
		} catch (error) {
			console.error('Faild to edit profile', error);
			alert('Faild to edit profile');
		}
	});
});
