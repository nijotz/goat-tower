var buffer = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc non ex a est malesuada rhoncus. Morbi dignissim nisi erat, eget cursus dolor tempor sit amet. Nullam ultricies sapien malesuada, porttitor justo a, fermentum lectus. Aliquam vel egestas ante. Curabitur velit quam, facilisis eget ipsum eget, volutpat ultricies orci. Morbi tempus, est id vulputate egestas, velit dolor lobortis metus, non vulputate arcu ipsum vitae lectus. Sed enim quam, posuere et neque quis, faucibus pharetra neque. Donec tincidunt arcu eu felis auctor congue sed at orci.";
var output;

function init() {
  output = document.getElementById('output');
  write_text();
  blink_cursor();
}
window.addEventListener('load', init, false );

function write_text() {
  if (buffer.length === 0) {
    // TODO: re-enable input
    return;
  }

  // pop
  var next_char = buffer[0];
  buffer = buffer.substring(1);

  // add to output
  if (output.innerHTML[output.innerHTML.length - 1] === '_') {
    output.innerHTML = output.innerHTML.slice(0, -1);
  }
  output.innerHTML += next_char;
  setTimeout(write_text, 10);
}

function blink_cursor(on) {
  if (on) {
    output.innerHTML += '_';
  } else if (output.innerHTML[output.innerHTML.length - 1] === '_') {
    output.innerHTML = output.innerHTML.slice(0, -1);
  }
  setTimeout(function() { blink_cursor(!on); }, 500);
}
