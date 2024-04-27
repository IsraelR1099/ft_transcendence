async function friendRequests(userId)
{
    try
    {
        const userData = JSON.parse(localStorage.getItem('userData'));
        const response = await fetch(`/api/user/friend_request/${userId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userData.token_access}`,
            }
        });

        if (response.ok)
        {
            const data = await response.json();
            return data.friend_requests;
        }
        else
        {
            alert('Failed to get friend requests');
            return null;
        }
    }
    catch (error)
    {
        console.error('Error:', error);
        return null;
    }
}

async function handleFriendRequests()
{
    const userData = JSON.parse(localStorage.getItem('userData'));
    const userId = userData.id;
    console.log('userid en handle friends:', userId);
    const friendRequestsData = await friendRequests(userId);

    if (friendRequestsData && friendRequestsData.length > 0)
    {
        window.location.href = 'friend_requests.html?requests=' + encodeURIComponent(JSON.stringify(friendRequestsData));
    }
    else
    {
        alert('No friend requests');
    }
}

const friendRequestButton = document.getElementById('friendRequestButton');
if (friendRequestButton)
{
    friendRequestButton.addEventListener('click', handleFriendRequests);
}
