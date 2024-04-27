document.addEventListener('DOMContentLoaded', async function()
{
	const searchForm = document.getElementById('searchForm');
	const searchInput = document.getElementById('searchInput');

	searchForm.addEventListener('submit', async function(event)
	{
		event.preventDefault();

		const searchQuery = searchInput.value.trim();

		try
		{
			const userData = JSON.parse(localStorage.getItem('userData'));

			if (!userData || !userData.token_access)
			{
				console.error('No user data found');
				return;
			}

			const response = await fetch(`/api/user/search/?q=${searchQuery}`,
			{
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'Accept': 'application/json',
					'Authorization': `Bearer ${userData.token_access}`,
				},
			});

			const data = await response.json();

			if (response.ok)
			{
				console.log('Search results:', data);
				window.location.href = `search_result.html?results=${encodeURIComponent(JSON.stringify(data.accounts))}`;
			}
			else
			{
				console.error('Search failed:', data);
			}
		}
		catch (error)
		{
			console.error('Search failed:', error);
		}
	});
});
