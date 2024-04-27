async function fetchAccountData(userId) {
	try {
		console.log('User ID:', userId);
		const response = await fetch(`/api/user/account/${userId}/`, {
			method: 'GET',
			headers: {
			'Content-Type': 'application/json',
			'Accept': 'application/json'
			},
		});
		const data = await response.json();
		if (response.ok) {
			console.log("Account data fetched");
			redirectToUserPage(data);
		}
		else {
			console.error("Failed to feth account", data.error);
			alert("Failed to fetch user info.");
		}
	}
	catch (error) {
		console.error("error fetching user info:", error);
	}
}

function redirectToUserPage(data) {
	let	newData = JSON.parse(localStorage.getItem('userData'));
	const profile_image_base64 = data.profile_image_base64;
	newData.profile_image_base64 = profile_image_base64;
	const updateData = JSON.stringify(newData);
	localStorage.setItem('userData', updateData);
	window.location.href = '../pages/user_profile.html';
}

export { fetchAccountData };
