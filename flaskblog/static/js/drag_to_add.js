
function getPrev(evt, seats) {
  prev = document.getElementsByClassName("draggable-container--is-dragging")[0].id;
  var index = seats.indexOf(prev);
  if (index > -1) {
    seats.splice(index, 1);
  }
  return prev;
}

function addNewSeats(evt, prev, seats) {
  if (document.querySelector('.draggable-container--over') == null) {
    console.log("not defined");
  }
  else{
    cur = document.getElementsByClassName("draggable-container--over")[0].id;
    a = evt.dropzone;
    console.log(a);
    if (prev == cur){
      console.log("stayed");
    }
    else{
      seats.push(cur);
      console.log("moved");
      modifyForm();
    }
  }
}//end of addNewSeats

const containers = document.querySelectorAll('.block');
const droppable = new Draggable.Droppable(containers, {
  draggable: '.draggable',
  droppable: '.droppable'
});



var added_seats = [];
var previous_spot = 0;
var current_spot;


function modifyForm() {
  document.getElementById("floor_seats").value = added_seats.join();
  // document.getElementById("floor_seats").setAttribute('value', 'defaultValue');
  // console.log(document.getElementById("floor_seats").id);
}


droppable.on('drag:start', (evt) => previous_spot = getPrev(evt, added_seats));
droppable.on('drag:stop', (evt) => addNewSeats(evt, previous_spot, added_seats));
