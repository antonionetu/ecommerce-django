document.addEventListener('DOMContentLoaded', function () {
    const container = document.querySelector('.image-container');
    const img = container.querySelector('.zoom-img');

    container.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        img.style.setProperty('--x', `${x}%`);
        img.style.setProperty('--y', `${y}%`);
    });

    const mainImage = document.querySelector(".zoom-img")

    document.querySelectorAll(".miniature").forEach(function (thumbnail) {
        thumbnail.addEventListener("click", function () {
            mainImage.src = this.src;
        });
    });


    document.querySelector("#selectVariant").addEventListener("change", function(event) {
        selectedVariant = event.target.value;
    });

    
    function applyCepMask(input) {
        let value = input.value;
        value = value.replace(/\D/g, "");
        value = value.substring(0, 8);

        if (value.length > 5) {
            value = value.substring(0, 5) + "-" + value.substring(5);
        }

        input.value = value;
    }

    function clearResult() {
        document.getElementById("freightResult").textContent = "";
    }

    function createFreightItem(freight) {
        const companyImg = freight.company?.picture
            ? `<img src="${freight.company.picture}" alt="${freight.company.name}" style="width:30px; vertical-align:middle; margin-right:8px;">`
            : "";
        const li = document.createElement("li");
        li.style.marginBottom = "10px";
        li.innerHTML = `${companyImg}<strong>${freight.name}</strong> - R$ ${parseFloat(freight.price).toFixed(2)} (${freight.delivery_time} dia${freight.delivery_time > 1 ? 's' : ''})`;
        return li;
    }    

    function displayFreightOptions(freights) {
        const result = document.getElementById("freightResult");
        result.innerHTML = "";
      
        const validFreights = freights.filter(f => f.price && !f.error);
      
        if (validFreights.length === 0) {
            result.textContent = "Nenhuma opção de frete disponível para este CEP.";
            return;
        }
      
        const cheapest = getCheapestFreight(validFreights);
        const fastest = getFastestFreight(validFreights);
      
        const ol = document.createElement("ol");
        ol.style.listStyle = "none";
        ol.style.padding = 0;
      
        if (cheapest && fastest && cheapest.id === fastest.id) {
            const li = createFreightItem(cheapest);
            li.style.fontWeight = "bold";
            li.innerHTML += " - Melhor Opção";
            ol.appendChild(li);
        } else {
            if (cheapest) {
                const liCheapest = createFreightItem(cheapest);
                liCheapest.style.fontWeight = "bold";
                liCheapest.innerHTML += " - Mais Barato";
                ol.appendChild(liCheapest);
            }
        
            if (fastest) {
                const liFastest = createFreightItem(fastest);
                liFastest.style.fontWeight = "bold";
                liFastest.innerHTML += " - Mais Rápido";
                ol.appendChild(liFastest);
            }
        }

        let excludedIds = [];

        if (cheapest) excludedIds.push(cheapest.id);
        if (fastest && fastest.id !== cheapest?.id) excludedIds.push(fastest.id);
        
        let otherOptions = validFreights.filter(f => !excludedIds.includes(f.id));
      
        otherOptions.sort((a, b) => {
            if ((a.delivery_time ?? Infinity) !== (b.delivery_time ?? Infinity)) {
                return (a.delivery_time ?? Infinity) - (b.delivery_time ?? Infinity);
            }
            return parseFloat(a.price) - parseFloat(b.price);
        });
      
        otherOptions = otherOptions.slice(0, 3);
      
        if (otherOptions.length > 0) {
            const liOthers = document.createElement("li");
            liOthers.style.marginTop = "20px";
            liOthers.innerHTML = "<strong>Outras opções:</strong>";
            ol.appendChild(liOthers);
        
            otherOptions.forEach(freight => {
                const li = createFreightItem(freight);
                ol.appendChild(li);
            });
        }
      
        result.appendChild(ol);
    }
      
    document.querySelector('#calculateFreightButton').addEventListener('click', async function() {
        const CEP = document.getElementById('CEP').value.replace("-", "").trim();
        const result = document.getElementById("freightResult");
    
        if (!/^\d{8}$/.test(CEP)) {
            result.textContent = "CEP inválido. Digite 8 números.";
            return;
        }
    
        result.textContent = "Calculando...";
    
        try {
            const freights = await getFreightPrice(CEP);
            displayFreightOptions(freights);
        } catch (error) {
            result.textContent = `Erro ao calcular frete, tente mais tarde.`;
            console.error(error);
        }
    });


    const select = document.getElementById('selectVariant');
    const prices = document.querySelectorAll('#variantPrices .price');

    select.value = "0";

    prices.forEach(price => price.style.display = 'none');

    select.addEventListener('change', function () {
        const selectedId = this.value;

        prices.forEach(price => {
            price.style.display = (price.dataset.variantId === selectedId) ? 'block' : 'none';
        });
    });

    document.querySelector("#addProduct").addEventListener("click", function (){
        if (!selectedVariant){
            alert("Selecione um tamanho disponível.")
            return;
        }

        addProduct()
    })
});
