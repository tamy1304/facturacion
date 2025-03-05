document.getElementById('factura-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const cliente = document.getElementById('cliente').value;
    const producto = document.getElementById('producto').value;
    const precio = document.getElementById('precio').value;
    
    console.log({ cliente, producto, precio });  // Agrega un console.log para ver los datos enviados

    fetch('http://127.0.0.1:5000/crear_factura', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cliente, producto, precio })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.mensaje);
        obtenerFacturas();
    });
});


function obtenerFacturas() {
    fetch('http://127.0.0.1:5000/notificacion')
    .then(response => response.json())
    .then(data => {
        console.log("Notificaciones:", data);
    });

    fetch('http://127.0.0.1:5000/facturas')
    .then(response => response.json())
    .then(facturas => {
        console.log(facturas);  // Agrega un console.log para ver la respuesta
        const lista = document.getElementById('facturas-lista');
        lista.innerHTML = '';
        facturas.forEach(factura => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${factura.id}</td>
                <td>${factura.cliente}</td>
                <td>${factura.producto}</td>
                <td>${factura.precio}</td>
                <td>${factura.estado}</td>
                <td>
                    ${factura.estado === 'pendiente' ? `<button class='btn btn-success' onclick='pagarFactura(${factura.id})'>Pagar</button>` : ''}
                </td>
            `;
            lista.appendChild(row);
        });
    });
}

function pagarFactura(id) {
    fetch(`http://127.0.0.1:5000/pagar_factura/${id}`, { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        alert(data.mensaje);
        obtenerFacturas();
    });
}

document.addEventListener('DOMContentLoaded', obtenerFacturas);
