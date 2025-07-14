function showPopup() {
    document.getElementById("payment-popup").classList.remove("hidden");
}

function closePopup() {
    localStorage.setItem('Cart-Reference', "vazio")
    location.href = '/'
}
