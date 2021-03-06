function measureURLsAccessTime() {
	var urlToGetFrom = "/getURL";
	
	atomic(urlToGetFrom)
		.then(function(response) {
			var urlsArr = response.data;
			
			// Measure retrieved URL(s) in a loop
			loopUrlsForMeasurement(urlsArr.length-1, urlsArr).then(function() {
			});
		})
		.catch(function(error) {
			console.log("Error: ", error.statusText);
		});
}

function loopUrlsForMeasurement(count, urlsArr) {
	if (count < 0) {
		return Promise.resolve();
	}
	
	var accessTimeArr = [];
	// Measurement method: Loop 4 times
	return repeatAccessTimeMeasurement(4, urlsArr[count], accessTimeArr).then(function() {
		sendAccessTimeToServer(accessTimeArr);
		
		return loopUrlsForMeasurement(count-1, urlsArr);
	});
}

function repeatAccessTimeMeasurement(count, url, accessTimeArr) {
	if (count == 0) {
		return Promise.resolve();
	}
	
	return measureAccessTime(url).then(function(accessTime) {
		var accessTimeJson = storeAccessTime(url, accessTime);
		accessTimeArr.push(accessTimeJson);
		
		return repeatAccessTimeMeasurement(count-1, url, accessTimeArr);
	});
}

function measureAccessTime(url) {
	return new Promise(function(resolve, reject) {
		var startTime = null;
		var endTime = null;
		
		var xhr = new XMLHttpRequest();
		xhr.open("GET", url, true);

		xhr.onload = function() {
			endTime = performance.now();
			resolve(endTime-startTime);
		}
		
		xhr.onerror = function() {
			resolve(loadImage(url));
		}
		
		startTime = performance.now();
		xhr.send(null);
	});	
}

// Detect CORS blocking by loading an img tag
function loadImage(url) {
	return new Promise(function(resolve, reject) {
		var image = document.createElement('img');
		
		// Other kind of errors
		image.onerror = function() {
			endTime = -1;
			resolve(endTime);
		}
		
		// Image exists but CORS blocked
		image.onload = function() {
			endTime = 0;
			resolve(endTime);
		}
		
		image.src = url;
	});
}

function getCookie() {
	var cookie = document.cookie;
	return cookie;
}

function storeAccessTime(url, accessTime) {
	var cookie = getCookie();
	var accessTimeJson = { "cookie" : cookie, "url" : url, "time" : accessTime};
	
	return accessTimeJson;
}

function sendAccessTimeToServer(accessTimeArr) {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "/addTiming");
    xhr.setRequestHeader("Content-Type", "application/json");
    
    xhr.onerror = function() {
    	console.log("Error: " + xhr.statusText);
    }
    
    xhr.send(JSON.stringify(accessTimeArr));
}
