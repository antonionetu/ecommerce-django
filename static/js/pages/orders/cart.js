document.addEventListener('DOMContentLoaded', function () {
    const cartReferenceForm = document.querySelector("#cart_reference")
    const freightIdForm = document.querySelector("#freight_id")

    if (cartReference === "vazio"){
        const pathSegments = location.pathname.split('/');
        localStorage.setItem("Cart-Reference", pathSegments[pathSegments.length - 2]);
    }

    const modal = document.getElementById("confirmModal");
    const btnYes = document.getElementById("confirmYes");
    const btnNo = document.getElementById("confirmNo");
    
    let itemToRemoveRow = null;
    let itemToRemoveId = null;
    
    function updateCartTotal() {
        let total = 0;
        document.querySelectorAll(".item-subtotal").forEach(el => {
            total += parseFloat(el.textContent.replace(',', '.'));
        });
        document.getElementById("cart-total").textContent = total.toFixed(2).replace('.', ',');
    }
    
    document.querySelectorAll(".qty-btn").forEach(button => {
        button.addEventListener("click", async function () {
            const itemId = this.dataset.itemId;
            const quantityElement = document.getElementById(`qty-${itemId}`);
            const subtotalElement = document.getElementById(`subtotal-${itemId}`);
            const row = this.closest("tr");

            selectedVariant = itemId;
            let currentQty = parseInt(quantityElement.textContent);

            const priceText = row.querySelector("td:nth-child(3)").textContent.trim();
            const unitPrice = parseFloat(priceText.replace('R$', '').replace('.', '').replace(',', '.'));

            if (this.classList.contains("increase")) {
                currentQty++;
                quantityElement.textContent = currentQty;

                const newSubtotal = (unitPrice * currentQty);
                subtotalElement.textContent = newSubtotal.toFixed(2).replace('.', ',');

                await addProduct();
                updateCartTotal();
                location.reload();
            }

            if (this.classList.contains("decrease")) {
                if (currentQty === 1) {
                    modal.classList.remove("hidden");
                    itemToRemoveRow = row;
                    itemToRemoveId = itemId;
                    return;
                } else {
                    currentQty--;
                    quantityElement.textContent = currentQty;

                    const newSubtotal = (unitPrice * currentQty);
                    subtotalElement.textContent = newSubtotal.toFixed(2).replace('.', ',');

                    await removeProduct();
                    updateCartTotal();
                    location.reload();
                }
            }
        });
    });
    
    btnYes.addEventListener("click", async() => {
        if (itemToRemoveRow) {
            itemToRemoveRow.remove();
            await removeProduct();
            location.reload()
        }
        modal.classList.add("hidden");
    });
    
    btnNo.addEventListener("click", () => {
        modal.classList.add("hidden");
        itemToRemoveRow = null;
        itemToRemoveId = null;
    });


    const validFreights = freightOptions.filter(f => !f.error && f.price && f.delivery_time);

    const cheapest = getCheapestFreight(validFreights);
    const fastest = getFastestFreight(validFreights);

    const remainingFreights = validFreights.filter(f =>
        f !== cheapest && f !== fastest
    );

    remainingFreights.sort((a, b) => {
        if ((a.delivery_time ?? Infinity) !== (b.delivery_time ?? Infinity)) {
            return (a.delivery_time ?? Infinity) - (b.delivery_time ?? Infinity);
        }
        return parseFloat(a.price) - parseFloat(b.price);
    });

    const topFreights = fastest === cheapest
        ?[fastest, ...remainingFreights.slice(0, 2)]
        :[fastest, cheapest, remainingFreights[0]]

    const container = document.getElementById('freightOptions');

    topFreights.forEach((freight, index) => {
        const id = `freight-${freight.id}`;
        const label = `${freight.name} - R$ ${parseFloat(freight.price).toFixed(2)} - ${freight.delivery_time} dia${freight.delivery_time > 1 ? 's' : ''}`;

        const wrapper = document.createElement('div');
        wrapper.style.display = "flex"
        wrapper.style.gap = "4px"

        const input = document.createElement('input');
        input.type = 'radio';
        input.name = 'freight_id';
        input.value = freight.id;
        input.id = id;

        if (freightIdForm){
            freightIdForm.value = freight.id
        }

        if (index === 0) input.checked = true;

        const labelEl = document.createElement('label');
        labelEl.setAttribute('for', id);
        labelEl.textContent = label;

        wrapper.appendChild(input);
        wrapper.appendChild(labelEl);
        container.appendChild(wrapper);
    });

    const cartTotalEl = document.getElementById("cart-total");
    const baseTotal = parseFloat(cartTotalEl.dataset.base.replace(',', '.'));
    let currentFreightValue = 0;

    function updateTotalWithFreight(newFreightValue) {
        const newTotal = baseTotal + newFreightValue;
        cartTotalEl.textContent = newTotal.toFixed(2).replace('.', ',');
        currentFreightValue = newFreightValue;

        cartTotalEl.classList.add("highlighted-total");
        setTimeout(() => {
            cartTotalEl.classList.remove("highlighted-total");
        }, 300);
    }

    function setFreightById(id) {
        const freight = freightOptions.find(f => f.id == id);
        if (freight) {
            const priceStr = freight.price.replace(',', '.');
            const priceNum = parseFloat(priceStr);
            updateTotalWithFreight(priceNum);
        } else {
            updateTotalWithFreight(0);
        }
    }

    document.getElementById('freightOptions').addEventListener('change', e => {
        if (e.target.name === 'freight_id') {
            setFreightById(e.target.value);
        }
    });

    window.addEventListener('DOMContentLoaded', () => {
        const checkedInput = document.querySelector('input[name="freight_id"]:checked');
        checkedInput
            ? setFreightById(checkedInput.value)
            : updateTotalWithFreight(0);
    });

    if (cartReferenceForm){
        cartReferenceForm.value = cartReference;
    }
});
