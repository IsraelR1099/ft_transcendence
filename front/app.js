document.addEventListener('DOMContentLoaded', function () {

	const loginForm = document.getElementById('loginForm');
	const registerForm = document.getElementById('registerForm');
	const userPage = document.getElementById('userPage');

	const oauthButton = document.getElementById('oauthButton');
	if (oauthButton) {
		oauthButton.addEventListener('click', function() {
			window.location.href = 'https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-e874bdccc7b9faba51dfa57e391ee107a6d1eb6f84e62ddd20679af8403c851b&redirect_uri=https%3A%2F%2Fpong.xyz%2Fprofile&response_type=code';
		});
	}

	//Define routes

	const routes = {
		"/": "index.html",
		"/profile": "user.html",
	};

	// Function to parse URL parameters
	const getUrlParameter = (name) => {
		name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
		const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
		const results = regex.exec(location.search);
		return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
	};

	authCode();
	// Check if the 'code' parameter is present in the URL
	async function authCode()
	{
		const authorizationCode = getUrlParameter('code');
		if (authorizationCode) {
			// Print the authorization code to the console
			console.log('Authorization code:', authorizationCode);
			try
			{
				const response = await fetch('/api/user/auth42/', {
					"method": "POST",
					"headers": {
						"Content-Type": "application/json",
					},
					"body": JSON.stringify({ "code": authorizationCode }),
				});
				const data = await response.json();

				if (response.ok) {
					console.log('Authenticated with 42 API');
					localStorage.setItem('userData', JSON.stringify(data));
					localStorage.setItem('token_access1', JSON.stringify(data.token_access));
					await fetchAccountData(data.id, data.token_access, data.token_refresh);
				}
				else {
					console.error('Failed to authenticate with 42 API', data.error);
					alert(data.error);
				}
			}
			catch (error)
			{
				console.error('Failed to authenticate with 42 API', error);
			}
			return ;
		}
		else {
			console.log('No authorization code found');
		}
	}

	const navigateToRoute = (route) => {
		const filePath = routes[route];
		if (filePath) {
			window.history.pushState({ path: route }, "", route);
			window.location.href = filePath
		}
	};

 	function redirectToUserPage(data) {
		let newData = JSON.parse(localStorage.getItem('userData'));
		const profile_image_base64 = data.profile_image_base64;
		newData.profile_image_base64 = profile_image_base64;
		const updatedData = JSON.stringify(newData);
		localStorage.setItem('userData', updatedData);
		navigateToRoute('/profile');
        	//window.location.href = 'user.html';
    	}

    async function fetchCSRFToken() {
        try {
            const response = await fetch('/api/user/get_csrf_token/');
            const data = await response.json();
            return (data.csrf_token);
        } catch (error) {
            console.error('Failed to fetch CSRF token', error);
        }
    }

    async function loginUser(username, password) {
        try {
            const csrfToken = await fetchCSRFToken();
            console.log('CSRF token:', csrfToken);
            if (!csrfToken) {
                console.error('CSRF token not found');
                return;
            }
            const response = await fetch('/api/user/login/', {
            method: 'POST',
            headers: {
               'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                },
            body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (data.error) {
                console.error("Login failed", data.error);
                alert (data.error['__all__'][0]);
            }
            else if (response.ok) {
                console.log(data);
                localStorage.setItem('userData', JSON.stringify(data));
                localStorage.setItem('token_access1', JSON.stringify(data.token_access));
                await fetchAccountData(data.id, data.token_access, data.token_refresh);
                    //redirectToUserPage(data);
            } else
            {
                console.error("Login failed", data.error);
            }
        } catch (error)
        {
        alert('Login failed');
        console.error("There was an error", error);
        }
    }

    async function registerUser(email, username, password1, password2) {
        try {
            const response = await fetch('/api/user/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify({ email, username, password1, password2 }),
            });

            const data = await response.json();

		if (response.ok)
		{
			console.log(data);
			localStorage.setItem('userData', JSON.stringify(data));
			await fetchAccountData(data.id, data.token_access, data.token_refresh);
                //redirectToUserPage(data);
		} else
		{
			console.error("Registration failed", data.error);
		}

        } catch (error) {
            console.error(error);
        }
    }

	async function fetchAccountData(userId, token_access, token_refresh) {
		try {
			console.log('User ID:', userId);
			console.log('token access: ', token_access);
			const response = await fetch(`/api/user/account/${userId}/`, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'Accept': 'application/json',
					'Authorization': `Bearer ${token_access}`,
				},
			});

			const data = await response.json();
			if (response.ok) {
				console.log('Account data fetched');
				console.log('profile image is:', data.profile_image_base64);
				redirectToUserPage(data);
			} else {
				console.error('Failed to fetch account data');
			}

		} catch (error) {
			console.error(error);
		}
	}

    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        await loginUser(username, password);
    });

    registerForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const email = document.getElementById('inputEmail').value;
        const username = document.getElementById('inputUsername').value;
        const password1 = document.getElementById('inputPassword1').value;
        const password2 = document.getElementById('inputPassword2').value;

        await registerUser(email, username, password1, password2);
    });

	const initialRoute = window.location.pathname;
	navigateToRoute(initialRoute);
});
