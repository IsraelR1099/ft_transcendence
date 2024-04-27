document.addEventListener('DOMContentLoaded', function() {
	const userData = JSON.parse(localStorage.getItem('userData'));
	const userProfileContainer = document.getElementById('userProfile');

	const userProfileHeading = document.createElement('h1');
	userProfileHeading.textContent = 'User Profile';
	userProfileContainer.appendChild(userProfileHeading);

	const userImage = document.createElement('img');
	userImage.src = `data:image/png;base64, ${userData.profile_image_base64}`;
	userProfileContainer.appendChild(userImage);

	const userList = document.createElement('ul');
	userProfileContainer.appendChild(userList);

	for (const [key, value] of Object.entries(userData)) {
		if (key !== 'profile_image_base64') {
			const listItem = document.createElement('li');
			listItem.textContent = `${key}: ${value}`;
			userList.appendChild(listItem);
		}
	}
});
