var temp = document.createElement("iframe");
// temp.style.display = "none";
temp.id = "tempIframe";
document.body.appendChild(temp);

var hn_links = document.querySelectorAll("td.title>a");
var lights = [];
for (var i = 0; i < hn_links.length - 1; i++) {
    var url = encodeURIComponent(hn_links[i].href);
    temp.src = "http://www.reddit.com/submit?url=" + url;
    var content = document.getElementById("tempIframe").contentWindow.document.body.innerHTML;
    console.log(content);
    if (content.indexOf("been submitted") != -1) {
        lights[i] = "submitted";
    } else if (content.indexOf("submitting a link") != -1) {
        lights[i] = "new";
    }
}
console.log(lights);
