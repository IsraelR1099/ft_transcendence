const route = async (event) => {
	event = event || window.event;
	event.preventDefault();
	const href = event.target.href;
	window.history.pushState({}, "", href);
	handleLocation();
};

const routes = {
	"/": "../index.html",
	"/login": "../pages/login.html",
	"/profile": "../pages/user_profile.html",
	"404": "../pages/404.html"
};

const handleLocation = async () => {
	const location = window.location.pathname;
	if (location.length == 0)
	{
		location = "/";
	}
	const route = routes[location] || routes["404"];
	const html = await fetch(route).then((data) => data.text());
};

window.onpopstate = handleLocation;
window.route = route;

handleLocation();

export { route };
