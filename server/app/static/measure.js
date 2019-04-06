// Measure access time of an arbitrary URL and send it back to server
function getAndSendUrlLoadTime() {
	// Step 1: Get URL
	var url = getUrl();

	// Step 2 : Get access time
	var accessTime = getUrlAccessTime(url);
	console.log('Url access time: ' + accessTime + 'ms');

	// Step 3: Store access time
	var accessTimeJson = storeAccessTime(url, accessTime);

	// Step 4: Send access time
	//sendAccessTimeToServer(accessTimeJson);
}

// Step 1 : Retrieve URL from server
function getUrl() {
	// TODO: Change to retrieve from server
	// Unsuccessful domain
	//var url = 'http://www.nus.edu.sg/templates/t3_nus2015/images/assets/logos/logo.png';
	// Successful domain
	var url = 'https://static.boredpanda.com/blog/wp-content/uploads/2017/08/before-after-cats-growing-up-141-5996b1a02695f__700.jpg';
	return url;
}

// Step 2 : Get access time of an arbitrary URL
function getUrlAccessTime(url) {
	// Step 2a: Measure current time before and after loading an URL
	// Step 2b: Load URL
	// Step 2c: Compute access time of URL
	var startTime = performance.now();
	loadUrl(url);
	var endTime = performance.now();
	
	var accessTime = endTime - startTime;
	return accessTime;
}

// Step 2b : Load an arbitrary URL
function loadUrl(url) {
	var request = new XMLHttpRequest();
	request.open("GET", url, false);
	request.send(null);
}

// Step 3 : Store access time in JSON format
function storeAccessTime(url, accessTime) {
	var accessTimeJson = { "url" : url, "access_time" : accessTime };
	console.log(accessTimeJson);
}

// Step 4 : Send access time JSON to server
function sendAccessTimeToServer(accessTimeJson) {
	// TODO
}
