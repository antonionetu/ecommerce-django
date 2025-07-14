document.addEventListener('DOMContentLoaded', () => {
    let time = 60 * 3;
    const counter = document.getElementById("counter");

    function updateTimer() {
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        counter.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        if (time > 0) time--;
    }

    function checkPaymentStatus() {
        fetch(`pagamento?payment_method=pix&pix_payment_id=${paymentID}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'PAID') {
                    showPopup();
                    return;
                }
                alert("Seu código de pagamento expirou.")
                location.reload()
            })
    }

    setInterval(updateTimer, 1000)    
    checkPaymentStatus()
});
