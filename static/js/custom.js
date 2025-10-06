// Custom JavaScript for CHSTH Admission Portal

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm before submitting final application
    const submitButton = document.querySelector('button[type="submit"]');
    if (submitButton && window.location.pathname.includes('section-e')) {
        submitButton.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to submit your application? You cannot edit it after submission.')) {
                e.preventDefault();
            }
        });
    }

    // Form validation feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            }
        });
    });
});
