//import { fetchAccountData } from './fetchUser.js';

document.addEventListener('DOMContentLoaded', function() {
	const oauthButton = document.getElementById('oauthButton');
	if (oauthButton) {
		oauthButton.addEventListener('click', function() {
			window.location.href = 'https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-cc2f8e34fdaade350fbe905be7bfedf8c7537dcd7f78c28c5905db15b0d8b534&redirect_uri=https%3A%2F%2Fpong.xyz%2Fpages%2Fredirect.html&response_type=code';
		});
	}
});
