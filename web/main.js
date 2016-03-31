var output_buffer = 'Goat Tower Pre-Alpha 0.00 Early Access Preview Build 1';
var output;
var input_buffer = '';
var input = '';

function init() {
  output = document.getElementById('output');
  write_text();
  read_text();
  blink_cursor();
}
window.addEventListener('load', init, false );

function write_text() {
  if (output_buffer.length === 0) {
    prompt_user();
    return;
  }

  // pop
  var next_char = output_buffer[0];
  output_buffer = output_buffer.substring(1);

  // add to output
  if (output.value[output.value.length - 1] === '_') {
    output.value = output.value.slice(0, -1);
  }
  output.value += next_char;
  setTimeout(write_text, 10);
}

function read_text() {
  setTimeout(read_text, 10);
  if (input_buffer.length === 0) { return; }

  // add to output
  if (output.value[output.value.length - 1] === '_') {
    output.value = output.value.slice(0, -1);
  }
  output.value += input_buffer;
  input_buffer = '';
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
  output.value += '\n\n';
  output.value += '> ';
  output.value += input_buffer;
  input_buffer = '';
}

function handle_input(event) {
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
document.onkeypress = handle_input;

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
        write_text();
      });
    }
  }

  xhr.send(json);
}
