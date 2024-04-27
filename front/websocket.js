document.addEventListener('DOMContentLoaded', function()
{
	const websocketButton = document.getElementById('websocketButton');

	if (websocketButton)
	{
		websocketButton.addEventListener('click', function()
			{
				window.location.href = 'websocket.html';
			}
		);
	}
});
