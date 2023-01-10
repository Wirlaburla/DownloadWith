/* globals chrome, compare_versions, compare_object_versions, get_version_warn, get_string, get_strings */
let testResult = document.getElementById('test_results');
let exeInput = document.getElementById('exeinput');

document.getElementById('test_button').onclick = function() {
	function error_listener() {
		testResult.style.color = 'red';
		testResult.innerText = "Error";
	}

	let port = chrome.runtime.connectNative('download_with');
	port.onDisconnect.addListener(error_listener);
	port.onMessage.addListener(function(message) {
		if (message) {
			console.log(message);
			testResult.style.color = 'darkgreen';
			testResult.innerText = "Success!";
		} else {
			error_listener();
		}
		port.onDisconnect.removeListener(error_listener);
		port.disconnect();
	});
	port.postMessage('ping');
};



exeInput.onchange = function(event) {
	chrome.storage.local.set({execute: exeInput.value});
}

chrome.storage.local.get({execute: null}, function({execute}) {
	exeInput.value = execute;
});