// Auto-dismiss alert messages after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function () { alert.remove(); }, 500);
        }, 4000);
    });

    // Confirm before removing cart item
    document.querySelectorAll('.remove-btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm('Remove this item from cart?')) {
                e.preventDefault();
            }
        });
    });
});
