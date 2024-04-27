document.addEventListener('DOMContentLoaded', function() {
	const sendFriendRequestButton = document.getElementById('sendFriendRequestButton');
	sendFriendRequestButton.addEventListener('click', function() {
		sendFriendRequest(userId, username);
	});
});

async function sendFriendRequest(userId, username)
{
	try
	{
		const userData = JSON.parse(localStorage.getItem('userData'));
		console.log('Sending friend request to user', userId);
		const requestBody = {
			receiver_user_id: userId,
			username: username
		};
		const response = await fetch(`/api/user/friend_request/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${userData.token_access}`,
			},
			body: JSON.stringify(requestBody),
		});
		const data = await response.json();
		if (response.ok)
		{
			alert('Friend request sent');
		}
		else
		{
			alert(data.error);
			console.eror('Error sending friend request:', response);
		}
	}
	catch (error)
	{
		console.error('Error sending friend request:', error);
	}
}
