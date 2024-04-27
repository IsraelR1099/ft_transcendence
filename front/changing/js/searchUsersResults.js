import {fetchAccountData} from './fetchUser.js';

document.addEventListener('DOMContentLoaded', function() {
	const	searchUsersResults = document.getElementById('searchResults');
	const	urlParams = new URLSearchParams(window.location.search);
	const	searchResultsJson = urlParams.get('results');
	const	searchResults = JSON.parse(searchResultsJson);
	if (searchResults) {
		searchResults.forEach(account => {
			const	accountElement = document.createElement('div');
			accountElement.classList.add('account');

			const usernameLink = document.createElement('a');
			usernameLink.textContent = account.username;
			usernameLink.href = "#";
			usernameLink.addEventListener('click', function() {
				fetchAccountData(account.id);
			});

			accountElement.appendChild(usernameLink);
			const	userIdParagraph = document.createElement('p');
			userIdParagraph.textContent = `User Id: ${account.id}`;
			accountElement.appendChild(userIdParagraph);

			const	friendStatusParagraph = document.createElement('p');
			friendStatusParagraph.textContent = account.is_friend ? 'Friend' : 'Not friend';
			friendStatusParagraph.classList.add(account.is_friend ? 'friend' : 'not-friend');
			accountElement.appendChild(friendStatusParagraph);

			console.log("account.is_friend: ", account.is_friend);
			console.log("accound: ", account);
			if (!account.is_friend) {
				console.log("account.id: ", account.id);
				const	sendFriendRequestButton = document.createElement('button');
				sendFriendRequestButton.textContent = 'Send friend request';
				sendFriendRequestButton.addEventListener('click', async function() {
				const	userData = JSON.parse(localStorage.getItem('userData'));
				const	requestBody = {
					receiver_user_id: account.id,
					username: account.username,
				};
				const	response = await fetch('/api/user/friend_request/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify(requestBody),
				});
				const data = await response.json();
				if (response.ok) {
					if (data.error) {
						alert(data.error);
					} else {
						alert('Friend request sent');
					}
				} else {
					alert(data.error);
				}
			});
				accountElement.appendChild(sendFriendRequestButton);
			}

			searchUsersResults.appendChild(accountElement);
		});
	} else {
		const	errorMessage = document.createElement('p');
		errorMessage.textContent = 'No results found';
		searchUsersResults.appendChild(errorMessage);
	}
});
