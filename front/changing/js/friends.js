document.addEventListener('DOMContentLoaded', async function() {
	const	friendList = document.getElementById('friendList');

	try {
		const	userData = JSON.parse(localStorage.getItem('userData'));
		const	response = await fetch(`/api/user/friend_list/${userData.id}/`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			}
		});

		const	data = await response.json();

		if (response.ok) {
			if (data.error) {
				alert("Failed to get friend list", data.error);
				return;
			} else {
				console.log(data);
				friendList.innerHTML = '';
				data.friends.forEach(friend => {
					const	friendElement = document.createElement('div');
					friendElement.classList.add('friend');

					const	friendName = document.createElement('p');
					friendName.textContent = friend.friend;
					friendElement.appendChild(friendName);

					friendList.appendChild(friendElement);
				});
			}
		} else {
			alert("Failed to get friend list", data.error);
			return;
		}
	} catch (error) {
		alert("Failed to get friend list", error);
	}
});
