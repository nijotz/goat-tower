var output_buffer = 'Goat Tower Pre-Alpha 0.00 Early Access Preview Build 1\n';
var output;
var input_buffer = '';
var input = '';

function init() {
  output = document.getElementById('output');
  write_text();
  blink_cursor();
  prompt_user();
}
window.addEventListener('load', init, false );

function write_text() {
  setTimeout(write_text, 10);

  var next_char;

  // pop from output or input buffers
  if (output_buffer.length > 0) {
    next_char = output_buffer[0];
    output_buffer = output_buffer.substring(1);
  } else if (input_buffer.length > 0) {
    next_char = input_buffer[0];
    input_buffer = input_buffer.substring(1);
  } else {
    return;
  }

  // Don't append after cursor if it's there
  if (output.value[output.value.length - 1] === '_') {
    output.value = output.value.slice(0, -1);
  }

  // add to output
  output.value += next_char;
  output.scrollTop = output.scrollHeight;
}

function blink_cursor(on) {
  if (on) {
    output.value += '_';
  } else if (output.value[output.value.length - 1] === '_') {
    output.value = output.value.slice(0, -1);
  }
  setTimeout(function() { blink_cursor(!on); }, 500);
}

function prompt_user() {
  output_buffer += '\n';
  output_buffer += '> ';
  output_buffer += input_buffer;
  input_buffer = '';
}

function read_text(event) {
  if (window.event) {
    key = event.charCode;
  } else if (e.which) {
    key = e.which;
  }

  if (event.keyCode == 13) {
    output_buffer += '\n\n';
    handle_command();
    return;
  }

  var char = String.fromCharCode(key);
  input_buffer += char;
  input += char;
}
document.onkeypress = read_text;

function handle_backspace(event) {

  if (event.keyCode !== 8) { return; }

  event.preventDefault();

  if (!input.length > 0) { return; }

  input = input.slice(0, -1);
  input_buffer = input_buffer.slice(0, -1);

  if (output.value[output.value.length - 1] === '_') {
    output.value = output.value.slice(0, -1);
  }
  output.value = output.value.slice(0, -1);
}
document.onkeydown = handle_backspace;

function handle_command() {
  run_command(input);
  input = '';
}

function command_json(cmd) {
  return JSON.stringify( {'command': cmd, 'user': 'WebUser00001'} );
}

function run_command() {
  var json = command_json(input);

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/api');
  xhr.setRequestHeader('Content-type', 'application/json');

  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      var output = JSON.parse(xhr.responseText);
      output.result.forEach(function(line) {
        output_buffer += line;
      });
      prompt_user();
    }
  }

  xhr.send(json);
}
