document.addEventListener('DOMContentLoaded', async function() {
	const	searchForm = document.getElementById('searchForm');
	const	searchInput = document.getElementById('searchInput');

	searchForm.addEventListener('submit', async function(event) {
		event.preventDefault();
		const	searchQuery = searchInput.value.trim();

		try {
			const	userData = JSON.parse(localStorage.getItem('userData'));
			if (!userData) {
				throw new Error('User data not found');
			}
			const	response = await fetch(`/api/user/search/?q=${searchQuery}`, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'Accept': 'application/json',
				},
			});
			const	data = await response.json();
			if (response.ok) {
				if (data.error) {
					throw new Error(data.error);
				}
				window.location.href = `../pages/searchUsers.html?results=${encodeURIComponent(JSON.stringify(data.accounts))}`;
			} else {
				console.error("Error:", data.error);
				throw new Error(data.error);
			}
		} catch (error) {
			console.error("Error:", error);
		}
	});
});
