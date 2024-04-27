document.addEventListener('DOMContentLoaded', function() {
	const	deleteButton = document.getElementById('delete42users');

	if (deleteButton) {
		deleteButton.addEventListener('click', async function() {
			try {
				const response = await fetch('/api/user/delete_users_42/', {
					method: "POST",
					headers: {
						'Content-Type': 'application/json',
					},
				});
				const data = await response.json();
				if (response.ok) {
					alert(data.message);
				} else {
					console.error('Failed to delete: ', data.error);
					alert(data.error);
				}
			} catch (error) {
				console.error('Failed to delete: ', error);
				alert('Failed to delete');
			}
		});
	}
});
