const cartReference = localStorage.getItem("Cart-Reference") || "vazio";

document.addEventListener('DOMContentLoaded', function () {
    const cartLink = document.getElementById("cartLinkPage");
    cartLink.href = `/pedidos/carrinho/${cartReference}/`;
});
