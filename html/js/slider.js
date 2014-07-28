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

function resetHeight() {
    // this prevents the left-side panel from sliding down if if gets shorter
    document.getElementById('decoder_panemover').style.height = infoPanel.offsetHeight + 'px';
    document.getElementById('right_decoder').style.height = infoPanel.offsetHeight  + 'px';
    document.getElementById('decoder_pane').style.height = infoPanel.offsetHeight  + 'px';
    document.getElementById('left_decoder').scrollLeft = '0px';    
}
