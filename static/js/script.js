// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-dismiss alerts after 5 seconds
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Initialize charts on report pages
    if (typeof Chart !== 'undefined') {
        var ctx = document.getElementById('salesChart');
        if (ctx) {
            var salesChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: JSON.parse(ctx.getAttribute('data-labels')),
                    datasets: [{
                        label: 'Daily Sales',
                        data: JSON.parse(ctx.getAttribute('data-values')),
                        backgroundColor: 'rgba(13, 110, 253, 0.1)',
                        borderColor: 'rgba(13, 110, 253, 1)',
                        borderWidth: 2,
                        tension: 0.1,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        var pieCtx = document.getElementById('productChart');
        if (pieCtx) {
            var productChart = new Chart(pieCtx, {
                type: 'pie',
                data: {
                    labels: JSON.parse(pieCtx.getAttribute('data-labels')),
                    datasets: [{
                        data: JSON.parse(pieCtx.getAttribute('data-values')),
                        backgroundColor: [
                            'rgba(13, 110, 253, 0.8)',
                            'rgba(25, 135, 84, 0.8)',
                            'rgba(255, 193, 7, 0.8)',
                            'rgba(220, 53, 69, 0.8)',
                            'rgba(111, 66, 193, 0.8)',
                            'rgba(32, 201, 151, 0.8)',
                            'rgba(253, 126, 20, 0.8)',
                            'rgba(13, 202, 240, 0.8)',
                            'rgba(108, 117, 125, 0.8)',
                            'rgba(214, 51, 132, 0.8)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                        }
                    }
                }
            });
        }
    }
    
    // Barcode scanner simulation for demo purposes
    if (document.getElementById('barcode-scanner')) {
        document.getElementById('barcode-scanner').addEventListener('click', function() {
            // In a real app, this would interface with a barcode scanner
            // For demo, we'll simulate scanning a random barcode
            var randomBarcode = Math.floor(Math.random() * 1000000000000).toString().padStart(12, '0');
            document.getElementById('id_barcode').value = randomBarcode;
            
            // Show a notification
            var alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-success alert-dismissible fade show';
            alertDiv.innerHTML = `
                <strong>Barcode scanned!</strong> ${randomBarcode}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            `;
            document.querySelector('.container').prepend(alertDiv);
            
            // Auto-dismiss after 3 seconds
            setTimeout(function() {
                var bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }, 3000);
        });
    }
});