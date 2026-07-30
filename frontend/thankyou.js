document.addEventListener("DOMContentLoaded", () => {
    // Read query parameters from URL redirect
    const params = new URLSearchParams(window.location.search);

    const amount = params.get("amount") || "0";
    const donorName = params.get("donor_name") || "Valued Donor";
    const donationId = params.get("donation_id") ? `DON-${params.get("donation_id")}` : "N/A";
    const transactionId = params.get("transaction_id") || params.get("trx") || "N/A";
    const paymentMethod = params.get("payment_method") || "bKash";
    const rawDate = params.get("date");

    // Format date string safely
    let formattedDate = new Date().toLocaleDateString('en-GB', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });

    if (rawDate) {
        const parsed = new Date(rawDate);
        if (!isNaN(parsed)) {
            formattedDate = parsed.toLocaleDateString('en-GB', {
                day: 'numeric',
                month: 'long',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    }

    // Populate elements on the DOM
    document.getElementById("val-amount").textContent = `৳${amount}`;
    document.getElementById("val-donor").textContent = donorName;
    document.getElementById("val-donation-id").textContent = donationId;
    document.getElementById("val-trx-id").textContent = transactionId;
    document.getElementById("val-date").textContent = formattedDate;
    document.getElementById("val-method").textContent = paymentMethod;
});