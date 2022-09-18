function test() {
    $('#addtobagmodal').modal('show');
  }

  function openModal(){

    $('#myModal').modal();
}       

function ColorToHex(color) {
  var hexadecimal = color.toString(16);
  return hexadecimal.length == 1 ? "0" + hexadecimal : hexadecimal;
}

function ConvertRGBtoHex(red, green, blue) {
  return "#" + ColorToHex(red) + ColorToHex(green) + ColorToHex(blue);
}

  let colorsall=[];


  var styleimage=1;

  function pallette(ele){
      console.log('Hi');
      var x=ele.id;
      var p=x.slice(3);
      styleimage=p;
      var fileid="File"+styleimage;
      var file=document.getElementById(fileid).files[0];
      console.log(file);
      /**drawOnImage(image);**/
      const image =  document.createElement("img");
      const image1 =  document.createElement("img");
      image.src =URL.createObjectURL(file);
      image1.id="Image"+styleimage;
      console.log(image.src);

      image.addEventListener("load", () => {
        drawOnImage(image,styleimage);
      });

      var container = document.getElementById("ColorPick");
      // Clear previous contents of the container
      while (container.hasChildNodes()) {
          container.removeChild(container.lastChild);
      }

      jQuery.noConflict(); 
      jQuery('#myModal').modal('show'); 
  }


  function fileToDataUri(field) {
    return new Promise((resolve) => {
      const reader = new FileReader();
  
      reader.addEventListener("load", () => {
        resolve(reader.result);
      });
  
      reader.readAsDataURL(field);
    });
  }

  function getBase64 (file, callback) {

    const reader = new FileReader();

    reader.addEventListener('load', () => callback(reader.result));

    reader.readAsDataURL(file);
}



  function drawOnImage(image = null,p) {
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
     /* var rgbset=new Set();
      var colors=[];
      var imgData = context.getImageData(0, 0, imageWidth, imageHeight);

        // invert colors
        for (var i = 0; i < imgData.data.length; i += 4) {
          var rgb=ConvertRGBtoHex(imgData.data[i],imgData.data[i+1],imgData.data[i+2]);
          rgbset.add(rgb);
        }
        rgbset.forEach (function(value) {
          console.log(value);
        colors.add(ConvertRGBtoHex(value[0],value[1],value[2]));
        })
        console.log(rgbset.size);
        setColorPickers(colors,p);*/
    }
}






function setColorPickers(arr=[[255,255,255]],p=styleimage){
  var fileid="File"+styleimage;
  var file=document.getElementById(fileid).files[0];
  var data=new FormData();
  data.append("num",document.getElementById("numColors").value);
  data.append("file",file);
  data.append("stylenum",styleimage);
  console.log(data);
  jQuery.ajax({
    type: "POST",
    url: '/colors',
    data: data,
    contentType: false,
    processData: false,
    success: function(response){
      console.log(response,typeof(response));
      arr=response["colors"];
      console.log(arr);


      var number = arr.length;
      // Container <div> where dynamic content will be placed
      var container = document.getElementById("ColorPick");
      // Clear previous contents of the container
      while (container.hasChildNodes()) {
          container.removeChild(container.lastChild);
      }
      for (i=0;i<number;i++){
          // Append a node with a random text
          container.appendChild(document.createTextNode("Color " + (i+1)));
          // Create an <input> element, set its type and name attributes
          var color=ConvertRGBtoHex(arr[i][0],arr[i][1],arr[i][2]);
          var input = document.createElement("input");
          input.type = "color";
          input.name = "color" + p;
          input.value=color;
          input.disabled=true;
          container.appendChild(input);
    
          var input1 = document.createElement("input");
          input1.type = "color";
          input1.name = "ncolor" + p;
          input1.value=color;
          container.appendChild(input1);
          // Append a line break 
          
          container.appendChild(document.createElement("br"));
      }
      container.appendChild(myFunction1(p));

    },
    error: function(response){
     console.log(response.responseJSON["Status"]);
     alert(response.responseJSON["Status"]);
    }
  });

  


  console.log(arr);
 

}





function addFields(){
    // Number of inputs to create
    var number = document.getElementById("numStyles").value;
    // Container <div> where dynamic content will be placed
    var container = document.getElementById("addField");
    // Clear previous contents of the container
    while (container.hasChildNodes()) {
        container.removeChild(container.lastChild);
    }
    for (i=0;i<number;i++){
        // Append a node with a random text
        container.appendChild(document.createTextNode("File " + (i+1)));
        // Create an <input> element, set its type and name attributes
        var input = document.createElement("input");
        input.type = "file";
        input.name = "File";
        input.id="File" + (i+1);
        container.appendChild(input);
        // Append a line break 
       /* var input1 = document.createElement("input");
        input1.type = "text";
        input1.name = "Area";
        input1.value='';
        container.appendChild(input1);*/

        container.appendChild(myFunction(i+1));
        container.appendChild(document.createElement("br"));
    }
    
    document.getElementById("Submitall").style="display:block";
    
}


function myFunction(x) {
  var btn = document.createElement("BUTTON");
  var t = document.createTextNode("Color Change");
  btn.setAttribute("id","btn"+x);
  btn.setAttribute("class","btn btn-primary");
  btn.setAttribute("onclick","pallette(this)");
  btn.appendChild(t);
  return btn;   
}

function myFunction1(x) {
  var btn = document.createElement("BUTTON");
  var t = document.createTextNode("SUBMIT");
  btn.setAttribute("id","clr"+x);
  btn.setAttribute("class","btn btn-primary");
  btn.setAttribute("onclick","submit(this)");
  btn.appendChild(t);
  return btn;   
}

function submit(ele){
var id=ele.id;
var p=id.slice(3);
var a=document.getElementsByName("color"+p);
var b=document.getElementsByName("ncolor"+p);
var l1=[],l2=[];
a.forEach(function(x){
l1.push(x.value);
})
b.forEach(function(x){
  l2.push(x.value);
  })
  colorsall.push([p,l1,l2]);
  console.log(colorsall);

  var data={};
  data['color']=[[p,l1,l2]];
  

  jQuery.ajax({
    type: "POST",
    url: '/clrchange',
    data: JSON.stringify(data),
    contentType: 'json',
    processData: false,
    success: function(response){
      document.getElementById("result1").style.display = 'block';
      console.log(response);
      var x = response["number"].replace(/\\n/g, "");
      var p = x.substr(2, x.length - 3);
      console.log(p);
      document.getElementById("result1").src="data:image/png;base64,"+p;
    },
    error: function(response){
     console.log(response);
     alert(response);
    }
  });







}


 function submitStyle(){
  var x1=document.getElementsByName("File");
  var data1=new FormData();
  var data={};
  var x=[],y=[],im=[];
  var i=1;
  x1.forEach(function(x11){
  data1.append('file'+i,x11.files[0]);
  i+=1;
  })
 
   data1.append('color',colorsall);
data['color']=colorsall;
data['position']=y;
  console.log(data);
 jQuery.ajax({
    type: "POST",
    url: '/style',
    data: data1,
    contentType: false,
    processData: false,
    success: function(){
      alert('Style images posted');
    },
    error: function(response){
     console.log(response["Status"]);
     alert(response["Status"]);
    }
  });


  jQuery.ajax({
    type: "POST",
    url: '/style1',
    data: JSON.stringify(data),
    contentType: 'json',
    processData: false,
    success: function(){
      alert('Style color change information posted');
    },
    error: function(response){
     console.log(response["Status"]);
     alert(response["Status"]);
    }
  });

}