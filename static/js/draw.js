const fileInput = document.querySelector("#upload");
let imgfile='';
// enabling drawing on the blank canvas
drawOnImage();

fileInput.addEventListener("change", async (e) => {
  const [file] = fileInput.files;

  // displaying the uploaded image
  const image = document.createElement("img");
  image.src = await fileToDataUri(file);

  // enbaling the brush after after the image
  // has been uploaded
  image.addEventListener("load", () => {
    drawOnImage(image);
    imgfile=image.src;
  });

  return false;
});

function fileToDataUri(field) {
  return new Promise((resolve) => {
    const reader = new FileReader();

    reader.addEventListener("load", () => {
      resolve(reader.result);
    });

    reader.readAsDataURL(field);
  });
}

const sizeElement = document.querySelector("#sizeRange");
let size = sizeElement.value;
sizeElement.oninput = (e) => {
  size = e.target.value;
};

const colorElement = document.getElementsByName("colorRadio");
let color;
colorElement.forEach((c) => {
  if (c.checked) color = c.value;
});

colorElement.forEach((c) => {
  c.onclick = () => {
    color = c.value;
  };
});


const colorElement1 = document.getElementById("head");
let color1;
colorElement1.onchange=()=>{color1=colorElement1.value};

function getCursorPosition(e) {
  const canvasElement = document.getElementById("canvas");
  var x;
  var y;
  if (e.pageX || e.pageY) {
    x = e.pageX;
    y = e.pageY;
  } else {
    x =
      e.clientX +
      document.body.scrollLeft +
      document.documentElement.scrollLeft;
    y =
      e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
  }
  x -= canvasElement.offsetLeft;
  y -= canvasElement.offsetTop;
  return [x, y];
}

function drawOnImage(image = null) {
  const canvasElement = document.getElementById("canvas");
  const context = canvasElement.getContext("2d");

  // if an image is present,
  // the image passed as a parameter is drawn in the canvas
  if (image) {
    const imageWidth = image.width;
    const imageHeight = image.height;
    console.log(imageWidth, imageHeight);
    // rescaling the canvas element
    canvasElement.width = imageWidth;
    canvasElement.height = imageHeight;

    context.drawImage(image, 0, 0, imageWidth, imageHeight);
  }

  const clearElement = document.getElementById("clear");
  clearElement.onclick = () => {
    currentpoints = [];
    points = [];
    context.closePath();
    const imageWidth = image.width;
    const imageHeight = image.height;
    context.clearRect(0, 0, canvasElement.width, canvasElement.height);
    canvasElement.width = imageWidth;
    canvasElement.height = imageHeight;

    context.drawImage(image, 0, 0, imageWidth, imageHeight);
  };
  var colors={'black':'white','white':'black','green':'red','red':'green','blue':'orange'};
  const nextElement = document.getElementById("next");
  nextElement.onclick = () => {
    points.push(currentpoints);
    num += 1;
    context.font = size*5 +"pt Calibri ";
    context.fillStyle = color1;
    console.log(colors[color],size);
    context.fillText(num, currentpoints[0][0], currentpoints[0][1]);
    currentpoints = [];
  };

  const endElement = document.getElementById("end");
  endElement.onclick = () => {
    
    var data={};
    data['points']=points;
    data['image']=imgfile;
    console.log(data);
    $.ajax({
      type: "POST",
      url: '/content',
      data: JSON.stringify(data),
      dataType: 'json',
      contentType: 'application/json;charset=UTF-8',
      processData: false,
      success: function(){
        alert('hI');
      },
      error: function(response){
       console.log(response.responseJSON["Status"]);
       alert(response.responseJSON["Status"]);
      }
    });
    currentpoints = [];
    points = [];
    num = 0;
    context.closePath();
  };

  let points = [];
  let currentpoints = [],num = 0;

  canvasElement.onclick = (e) => {
    console.log("Hi");
    console.log(e.clientX, e.clientY);
    var p = getCursorPosition(e);
    currentpoints.push(p);
    console.log(p);
    if (currentpoints.length > 1) {
      var prevX = currentpoints[currentpoints.length - 2][0];
      var prevY = currentpoints[currentpoints.length - 2][1];
      context.moveTo(prevX, prevY);
      context.lineTo(p[0], p[1]);
      context.stroke();
    } else {
      context.beginPath();
      context.lineWidth = size;
      context.strokeStyle = color;
      context.lineJoin = "round";
      context.lineCap = "round";
      var p = getCursorPosition(e);
      context.rect(p[0], p[1], 1, 1);
      context.stroke();
    }
  };

 /* canvasElement.ondblclick = (e) => {
    console.log("double");
    if (currentpoints.length > 1) {
      var prevX = currentpoints[0][0];
      var prevY = currentpoints[0][1];
      var p = getCursorPosition(e);
      context.moveTo(p[0], p[1]);
      context.lineTo(prevX, prevY);
      context.stroke();
    }
  };*/

  /*canvasElement.onmousedown = (e) => {
    isDrawing = true;
    context.beginPath();
    context.lineWidth = size;
    context.strokeStyle = color;
    context.lineJoin = "round";
    context.lineCap = "round";
    context.moveTo(e.clientX, e.clientY);
  };

  canvasElement.onmousemove = (e) => {
    if (isDrawing) {
      context.lineTo(e.clientX, e.clientY);
      context.stroke();
    }
  };

  canvasElement.onmouseup = function () {
    isDrawing = false;
    context.closePath();
  };*/
}
