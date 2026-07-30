document.addEventListener("DOMContentLoaded", () => {
    // Read query parameters from URL redirect
    const params = new URLSearchParams(window.location.search);

    // 1. Amount
    const rawAmount = params.get("amount") || "0";
    const amountEl = document.getElementById("amount");
    if (amountEl) {
        amountEl.textContent = `৳${rawAmount}`;
    }

    // 2. Donor Name
    const donorName = params.get("donor_name") || params.get("name") || "Valued Donor";
    const donorEl = document.getElementById("donorName");
    if (donorEl) {
        donorEl.textContent = donorName;
    }

    // 3. Donation ID
    const rawDonationId = params.get("donation_id") || params.get("donationID");
    let displayDonationId = "N/A";
    if (rawDonationId) {
        displayDonationId = rawDonationId.startsWith("DON-") ? rawDonationId : `DON-${rawDonationId}`;
    }
    const donationEl = document.getElementById("donationId");
    if (donationEl) {
        donationEl.textContent = displayDonationId;
    }

    // 4. Transaction ID
    const transactionId = params.get("transaction_id") || params.get("trxID") || params.get("trx") || "N/A";
    const trxEl = document.getElementById("transactionId");
    if (trxEl) {
        trxEl.textContent = transactionId;
    }

    // 5. Payment Method
    const paymentMethod = params.get("payment_method") || "bKash";
    const methodEl = document.getElementById("val-method");
    if (methodEl) {
        methodEl.textContent = paymentMethod;
    }

    // 6. Date & Time
    const rawDate = params.get("date");
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

    const dateEl = document.getElementById("val-date");
    if (dateEl) {
        dateEl.textContent = formattedDate;
    }
});