var qrCode;

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}
function showQR(){
    qr_data = document.getElementById("inputQRData").value;
    qrCode = new QRCodeStyling({
        width: 250,
        height: 250,
        type: "svg",
        data: qr_data,
        dotsOptions: {
            color: "#000000",
            type: "rounded"
        },
        margin: 5,
        backgroundOptions: {
            color: "#ffffff",
        },
        imageOptions: {
            crossOrigin: "anonymous",
            margin: 1,
            imageSize: 0.36
        }
    });
    qrCode.update({image: unlock_logo});
    canvas = document.getElementById("qr_code")
    removeAllChildNodes(canvas);
    qrCode.append(canvas);
}
function getTheSvg(url) {
   return fetch(url).then(res => res.text());
}
function createElementFromHTML(htmlString) {
  var div = document.createElement('div');
  div.innerHTML = htmlString.trim();

  // Change this to div.childNodes to support multiple top-level nodes.
  return div.firstChild;
}

function downloadSVG(svg){
    //get svg element.

    //get svg source.
    var serializer = new XMLSerializer();
    var source = serializer.serializeToString(svg);

    //add name spaces.
    if(!source.match(/^<svg[^>]+xmlns="http\:\/\/www\.w3\.org\/2000\/svg"/)){
        source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
    }
    if(!source.match(/^<svg[^>]+"http\:\/\/www\.w3\.org\/1999\/xlink"/)){
        source = source.replace(/^<svg/, '<svg xmlns:xlink="http://www.w3.org/1999/xlink"');
    }

    //add xml declaration
    source = '<?xml version="1.0" standalone="no"?>\r\n' + source;

    //convert svg source to URI data scheme.
    var url = "data:image/svg+xml;charset=utf-8,"+encodeURIComponent(source);

    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "qr.svg";
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
}

function download(){
    extension = document.getElementById("qr-extension").value;
    if (extension !== 'svg'){
        qrCode.download({ name: "qrcode", extension: extension })
        return;
    }
    svg = document.querySelector('#qr_code svg');
    var images = document.querySelectorAll('#qr_code img, image');
    if (images.length === 0){
        return;
    }
    var image = images.item(0);
    x = image.getAttribute('x')
    y = image.getAttribute('y')
    height = image.getAttribute('height')
    width = image.getAttribute('width')

    getTheSvg(unlock_logo).then(res => {
        svg_logo = createElementFromHTML(res);
        svg_logo.setAttribute('x', x);
        svg_logo.setAttribute('y', y);
        svg_logo.setAttribute('height', height);
        svg_logo.setAttribute('width', width);
        console.log(image)
        console.log(svg)
        svg.removeChild(image);
        svg.appendChild(svg_logo);
        downloadSVG(svg);
    });


}