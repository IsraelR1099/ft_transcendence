import { fetchAccountData } from './fetchUser.js';

document.addEventListener('DOMContentLoaded', function() {
	const	getUrlParameter = (name) => {
		name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
		const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
		const results = regex.exec(location.search);
		return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
	};
	authCode();
	async function authCode() {
		const	code = getUrlParameter('code');
		if (code) {
			try {
				const response = await fetch('/api/user/auth42/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ "code": code }),
				});
				const data = await response.json();
				if (response.ok)
				{
					if (data.error) {
						alert(data.error);
						window.location.href = '/';
						return;
					}
					console.log("Login successful: ", data);
					localStorage.setItem('userData', JSON.stringify(data));
					await fetchAccountData(data.id);
				} else {
					alert(data.error);
				}
			} catch (error) {
				console.error('Error:', error);
			}
		} else {
			alert('Error: No code found');
		}
	}
});
