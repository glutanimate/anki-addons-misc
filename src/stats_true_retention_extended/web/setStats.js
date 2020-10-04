async function setStats(stats) {
	while (!document.querySelector('#graph-today-stats')) {
		await new Promise((resolve) => setTimeout(resolve, 100));
	}
	console.log('running this');
	document.getElementById('graph-today-stats').innerHTML = stats;
	document.getElementById('graph-today-stats').style = 'text-align: center';
}
