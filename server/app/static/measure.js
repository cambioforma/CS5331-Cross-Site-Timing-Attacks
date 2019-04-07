// Measure access time of an arbitrary URL and send it back to server
function getAndSendUrlLoadTime() {
	// Step 1: Get URL
	var url = getUrl();

	// Step 2 : Get access time
	// Access time:
	// 1) >0: Unblocked domain
	// 2) 0 : CORS blocked domain
	// 3) -1: Unaccessible domain (network errors etc.)
	var urlPromise = getUrlAccessTime(url);
	
	// Waits for getUrlAccessTime(url) to finish execution before resuming
	urlPromise.then(function(accessTime) {
		// Run all the functions
		console.log("Finished running loadUrl");
		console.log(accessTime);
		
		// Step 3: Store access time
		var accessTimeJson = storeAccessTime(url, accessTime);

		// Step 4: Send access time
		//sendAccessTimeToServer(accessTimeJson);	
	});
}

// Step 1 : Retrieve URL from server
function getUrl() {
	// TODO: Change to retrieve from server
	
	// CORS blocked domain -> return 0
	//var url = 'http://www.nus.edu.sg/templates/t3_nus2015/images/assets/logos/logo.png';
	//var url = 'https://ivle.nus.edu.sg/v1/content/assets/images/ivle-logo.png';
	
	// Unexisting URL -> return -1
	//var url = 'https://ivle.nus.edu.sg/v1/content/assets/images/icelogo.png';
	
	// Successful domain -> return accessTime
	var url = 'https://static.boredpanda.com/blog/wp-content/uploads/2017/08/before-after-cats-growing-up-141-5996b1a02695f__700.jpg';
	return url;
}

// Step 2 : Get access time of an arbitrary URL
// Step 2a: Measure current time before loading URL
// Step 2b: Load an arbitrary URL
// Step 2c: Measure current time after loading URL
// Step 2d: Compute access time of URL (successful loading)
function getUrlAccessTime(url) {
	console.log("Entered loadUrl");
	return new Promise(function(resolve, reject) {
		var startTime = null;
		var endTime = null;
		
		// Setup XmlHttpRequest
		var xhr = new XMLHttpRequest();
		xhr.open("GET", url, true);

		xhr.onload = function() {
			console.log("Entered xhr.onload");
			endTime = performance.now();
			resolve(endTime-startTime);
		}
		
		xhr.onerror = function() {
			console.log("Entered xhr.onerror");
			resolve(loadImage(url));
		}
		
		startTime = performance.now();
		// Load URL
		xhr.send(null)
	});	
}

// Detect CORS blocking by loading as an img tag
function loadImage(url) {
	console.log("Entered loadImage");
	return new Promise(function(resolve, reject) {
		var image = document.createElement('img');
		
		// Other kind of errors
		image.onerror = function() {
			console.log(url, "other kind of errors");
			endTime = -1;
			resolve(endTime);
		}
		
		// Image exists but CORS blocked
		image.onload = function() {
			console.log(url, "image exists but cors blocked");
			endTime = 0;
			resolve(endTime);
		}
		
		image.src = url;
	});
}

// Step 3 : Store access time in JSON format
function storeAccessTime(url, accessTime) {
	var cookie = "abc";
	var sequence = 0;
	var accessTimeJson = { "cookie" : cookie, "url" : url, "time" : accessTime, "sequence" : sequence };
	console.log(accessTimeJson);
}

// Step 4 : Send access time JSON to server
function sendAccessTimeToServer(accessTimeJson) {
	// TODO
}
