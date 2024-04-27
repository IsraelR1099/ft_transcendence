document.addEventListener('DOMContentLoaded', function() {
    const friendListButton = document.getElementById('friendListButton');
    friendListButton.addEventListener('click', function() {
        fetchFriendList();
    });
});

async function fetchFriendList() {
    try {
        const userData = JSON.parse(localStorage.getItem('userData'));
        const response = await fetch(`/api/user/friend_list/${userData.id}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userData.token_access}`,
            }
        });

        if (response.ok) {
            const friendListData = await response.json();
            // Implement code to display the friend list data
            console.log('Friend List Data:', friendListData);
            displayFriendList(friendListData);
        } else {
            console.error('Failed to fetch friend list:', response);
        }
    } catch (error) {
        console.error('Error fetching friend list:', error);
    }
}

function displayFriendList(friendListData)
{
    const friends = friendListData.friends;
    const friendListJson = encodeURIComponent(JSON.stringify(friends));
    const url = `friend_list.html?friends=${friendListJson}`;
    window.location.href = url;
}
