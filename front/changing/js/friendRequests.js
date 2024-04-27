document.addEventListener('DOMContentLoaded', async function() {
	const	friendRequestsList = document.getElementById('friendRequestsList');

	try {
		const	userData = JSON.parse(localStorage.getItem('userData'));
		const response = await fetch(`/api/user/friend_request/${userData.id}/`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			}
		});
		const data = await response.json();

		if (response.ok) {
			console.log(data);
			data.friend_requests.forEach((request) => {
				const	requestElement = document.createElement('div');
				requestElement.classList.add('friend-request');

				const	senderElement = document.createElement('p');
				senderElement.textContent = `From: ${request.sender}`;
				requestElement.appendChild(senderElement);

				const senderImage = document.createElement('img');
				senderImage.src = `data:image/png;base64,${request.sender_profile_image}`;
				senderImage.alt = `Profile image of ${request.sender}`;
				requestElement.appendChild(senderImage);

				const acceptButton = document.createElement('button');
				acceptButton.textContent = 'Accept';
				acceptButton.addEventListener('click', async function() {
					await handleAcceptRequest(request.sender, request.pk);
					requestElement.remove();
				});
				requestElement.appendChild(acceptButton);

				const declineButton = document.createElement('button');
				declineButton.textContent = 'Decline';
				declineButton.addEventListener('click', async function() {
					await handleDeclineRequest(request.sender, request.pk);
					requestElement.remove();
				});
				requestElement.appendChild(declineButton);

				friendRequestsList.appendChild(requestElement);
			});
		} else {
			alert('Failed to get friend requests');
		}
	} catch (error) {
		console.error(error);
	}
});

async function handleAcceptRequest(sender, requestId) {
	try {
		console.log('Accepting request from', sender);
		console.log('Request ID:', requestId);
		const userData = JSON.parse(localStorage.getItem('userData'));
		const	response = await fetch(`/api/user/accept_friend_request/${requestId}/`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			}
		});
		if (response.ok) {
			alert(`You are now friends with ${sender}`);
		} else {
			alert('Failed to accept friend request');
		}
	} catch (error) {
		console.error(error);
	}
}

async function handleDeclineRequest(sender, requestId) {
	try {
		const userData = JSON.parse(localStorage.getItem('userData'));
		const	response = await fetch(`/api/user/decline_friend_request/${requestId}/`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			}
		});
		if (response.ok) {
			alert(`You declined the friend request from ${sender}`);
		} else {
			alert('Failed to decline friend request');
		}
	} catch (error) {
		console.error(error);
	}
}
