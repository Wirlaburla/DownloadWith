/* globals chrome, compare_versions, get_version_warn, ERROR_COLOUR, WARNING_COLOUR */
var exe;

function open_external(item) {
	function error_listener(error) {
		console.error(error, chrome.runtime.lastError);
	}

	browser.downloads.cancel(item.id).then(
		function () {
			let command = exe.replace('%s', item.url);
			
			let port = chrome.runtime.connectNative('download_with');
			port.onDisconnect.addListener(error_listener);
			port.onMessage.addListener((m) => {
				console.log(m);
				port.onDisconnect.removeListener(error_listener);
				port.disconnect();
			});
			console.log('executing: '+command);
			port.postMessage(command.split(' '));
		},
		function (err) {
			console.log(`download_with: Could not cancel ${item.filename} (${item.id}): Error: ${err}`);
		}
    );
}

chrome.storage.local.get({execute: null}, function({execute}) {
	exe = execute;
});

browser.downloads.onCreated.addListener(open_external);