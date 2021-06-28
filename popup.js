
console.log("popup.js runs");


document.getElementById("replacely-form").addEventListener("click",myFunction);
function myFunction() {
  chrome.runtime.sendMessage({"message":"generate"});
}
chrome.runtime.onMessage.addListener(
 function(request, sender, sendResponse) {
   if( request.message === "result" ) {
       var sum = request.data;
       //$('#YSummarize-form div:last').after('<div class="myDiv">' + sum + '</div>' );
       document.getElementById("summarytext").innerHTML +=sum;
   }
  }
);