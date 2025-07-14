async function addProduct(){
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
    };

    if (cartReference) {
        headers['Cart-Reference'] = cartReference;
    }

    const response = await fetch(cartManagementEndPoint, {
        method: 'PATCH',
        headers,
        body: JSON.stringify({
            csrfmiddlewaretoken: csrfToken,
            'product_variant_id': selectedVariant,
        })
    })

    const data = await response.json();

    if (cartReference === "vazio"){
        localStorage.setItem("Cart-Reference", data.add_items.cart_reference);
    }

    const targetPath = `/pedidos/carrinho/${data.add_items.cart_reference}/`;
    if (location.pathname !== targetPath) {
        location.href = targetPath;
    }
}

async function removeProduct(){
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
    };

    if (cartReference) {
        headers['Cart-Reference'] = cartReference;
    }

    await fetch(cartManagementEndPoint, {
        method: 'DELETE',
        headers,
        body: JSON.stringify({
            csrfmiddlewaretoken: csrfToken,
            'product_variant_id': selectedVariant,
        })
    })
}
