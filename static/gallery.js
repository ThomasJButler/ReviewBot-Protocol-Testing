// Loads the saved renders from the server and lists them on the page.

function setStatus(colour) {
  document.getElementById("status-dot").style.background = colour;
}

function buildEntry(item) {
  var entry = document.createElement("div");
  entry.className = "render";
  entry.innerHTML = "<h2>" + item.title + "</h2>";

  var image = document.createElement("img");
  image.src = "/renders/" + item.file;
  entry.appendChild(image);

  return entry;
}

function loadRenders() {
  setStatus("#d62828");

  fetch("/api/renders")
    .then(function (response) {
      return response.json();
    })
    .then(function (renders) {
      var list = document.getElementById("render-list");
      list.innerHTML = "";
      renders.forEach(function (item) {
        list.appendChild(buildEntry(item));
      });
      setStatus("#2a9d8f");
    })
    .catch(function (error) {
      console.error("could not load the render list", error);
      setStatus("#d62828");
    });
}

loadRenders();
