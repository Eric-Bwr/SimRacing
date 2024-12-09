const socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('update', function (data) {
    const {speed, gear, rpm} = data;

    document.getElementById('speed').innerText = speed;
    document.getElementById('gear').innerText = gear;
    document.getElementById('rpm').innerText = rpm;
});