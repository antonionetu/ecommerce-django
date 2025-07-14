async function getFreightPrice(CEP) {
    const url = new URL(window.location.href);
    url.searchParams.append('CEP', CEP);

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
    });

    const data = await response.json();
    return data;
}

function getCheapestFreight(freights) {
    const validFreights = freights.filter(f => !f.error);
    validFreights.sort((a, b) => {
        const priceDiff = parseFloat(a.price) - parseFloat(b.price);
        if (priceDiff !== 0) return priceDiff;
        return (a.delivery_time ?? Infinity) - (b.delivery_time ?? Infinity);
    });
    return validFreights.length > 0 ? validFreights[0] : null;
}
  
function getFastestFreight(freights) {
    const validFreights = freights.filter(f => !f.error);
    validFreights.sort((a, b) => {
        const timeDiff = (a.delivery_time ?? Infinity) - (b.delivery_time ?? Infinity);
        if (timeDiff !== 0) return timeDiff;
        return parseFloat(a.price) - parseFloat(b.price);
    });
    return validFreights.length > 0 ? validFreights[0] : null;
}
  