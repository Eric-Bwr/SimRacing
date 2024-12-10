const socket = io.connect('http://' + document.domain + ':' + location.port);

let flashingInterval;

socket.on('update', function (data) {
    const {speed, gear, rpm, flashing} = data;

    document.getElementById('speed').innerText = speed.toString().padStart(3, '0');
    document.getElementById('gear').innerText = gear;

    const progressBar = document.querySelector('.progress-bar');
    const needle = document.querySelector('.needle');

    const clampedPercentage = Math.min(Math.max(rpm, 0), 100);
    progressBar.style.width = clampedPercentage + '%';
    const containerWidth = document.querySelector('.progress-container').offsetWidth;
    const needlePosition = (clampedPercentage / 100) * containerWidth;
    needle.style.left = `${needlePosition}px`;

    if (flashing) {
        if (!flashingInterval) {
            flashingInterval = setInterval(() => {
                document.body.style.backgroundColor = document.body.style.backgroundColor === "red" ? "#2B2B2B" : "red";
            }, 120);
        }
    } else {
        clearInterval(flashingInterval);
        flashingInterval = null;
        document.body.style.backgroundColor = "#2B2B2B";
    }
});
