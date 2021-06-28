console.log("content.js runs");

chrome.runtime.onMessage.addListener(message, function outputSummary(message){
  if (message ==="generate"){
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
    console.log(tabs[0].url);
    var link = tabs[0].url;
    function callback() {
    if (oReq.readyState === XMLHttpRequest.DONE) {
        if (oReq.status === 200) {
            result = oReq.responseText;
            chrome.runtime.sendMessage({"message": "result", "data": result});
        }
    }
}

var oReq = new XMLHttpRequest();
oReq.open("GET", link, true);
oReq.onreadystatechange = callback;
oReq.send();
});
}

var oReq = new XMLHttpRequest();
oReq.open("GET", link, true);
oReq.onreadystatechange = callback;
oReq.send();
})
