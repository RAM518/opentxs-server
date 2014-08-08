/* 

  Slider.js sliding menu-holder for reciept and message decoder / decrypter
  based on code from  here: http://jsfiddle.net/np56t/1/

  An invisible element is used for dragging.
  This element is resized to take up the whole screen when dragging.

*/


var mouseDown = false;

function dragStart(e) {

    document.getElementById('decoder_panemover').style.width = '100%';
    document.getElementById('decoder_panemover').style.left = '0px';

    mouseDown = true;
    x = e.clientX
   
    dragOffsetLeft = document.getElementById('left_decoder').offsetWidth - x;
    dragOffsetRight = document.getElementById('right_decoder').offsetWidth + x;
};

function dragRelease() {

    if (!mouseDown) {
        return
    }           
    document.getElementById('decoder_panemover').style.width = '5px';
    document.getElementById('decoder_panemover').style.left = document.getElementById('decoder_pane').offsetLeft + 3 + 'px';
    mouseDown = false;
};

function drag(e) { 

    if (!mouseDown) {
        return
    }   
    x = e.clientX
    tmpLeft = dragOffsetLeft + x
    tmpRight = dragOffsetRight - x
    if (tmpLeft < 30 || tmpRight < 30) {
        return
    }
    document.getElementById('left_decoder').style.width = tmpLeft + 'px';
    document.getElementById('right_decoder').style.width = tmpRight + 'px';       
    // this prevents the left-side panel from sliding down if if gets shorter
    resetHeight();
};            
/*
function resetHeight() {
    // this prevents the left-side panel from sliding down if if gets shorter
    console.log('resetting height:');
    var infoPanel = document.getElementById("left_decoder");
    var textPanel = document.getElementById("right_decoder");
    var rightTable = document.getElementById("rightTable")
    thisHeight1 = Math.max(infoPanel.offsetHeight, textPanel.offsetHeight);
    thisHeight = Math.max(thisHeight1,rightTable.offsetHeight);
    document.getElementById('decoder_panemover').style.height = thisHeight + 'px';
    document.getElementById('right_decoder').style.height = thisHeight  + 'px';
    document.getElementById('decoder_pane').style.height = thisHeight  + 'px';
    document.getElementById('left_decoder').scrollLeft = '0px';    
}
*/
function set_leftPanel() {
   var infoPanel = document.getElementById("menuContents");
   var dir_menu = "cgi/dir_menu.py";
   $.ajax({url: dir_menu,
      success: function(data){
         infoPanel.innerHTML = data;
         var treeRoot = document.getElementById('treeRoot');
         TreeMenu.toggle(treeRoot);
         resetHeight();                       
         //console.log("data: " + data);
      }
   });
}

function set_rightPanel(fileTarget,fileType){
   var textPanel = document.getElementById("decodedContents");
   textPanel.innerHTML = "<center><font color=#A4F1A6>Decoding" +
     fileTarget + "</font><br /><font color=#E2E3E8>Please Wait...</font>" + 
     "</center>"; 
   $.ajax({
      url: "cgi/fileParser.py",
      type    : 'POST',
      data    : {'target':fileTarget,'type':fileType},
      dataType: 'text',
      success: function(response){
         textPanel.innerHTML = response;         
         resetHeight();                       
         console.log(response);
      }
   });    
    
}