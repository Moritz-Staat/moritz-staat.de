let inactivityTime = function() {
    let time;
    let overlay = document.getElementById('overlay');

    // Reset the timer
    function resetTimer() {
        clearTimeout(time);
        document.body.classList.remove('overlay-active');
        time = setTimeout(showOverlay, 20000);  // 20 seconds
    }

    // Show the overlay
    function showOverlay() {
        document.body.classList.add('overlay-active');
    }

    // Monitor mouse movement and key presses
    window.onload = resetTimer;
    document.onmousemove = resetTimer;
    document.onkeydown = resetTimer;
}

inactivityTime();
