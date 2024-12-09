const socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('update', function (data) {
    const {speed, gear, rpm} = data;

    document.getElementById('speed').innerText = speed;
    document.getElementById('gear').innerText = gear;

    const progressBar = document.querySelector('.progress-bar');
    const needle = document.querySelector('.needle');

    const clampedPercentage = Math.min(Math.max(rpm, 0), 100);

    progressBar.style.width = clampedPercentage + '%';
    const containerWidth = document.querySelector('.progress-container').offsetWidth;
    const needlePosition = (clampedPercentage / 100) * containerWidth;
    needle.style.left = `${needlePosition}px`;
});
