document.addEventListener("DOMContentLoaded", () => {

    const params = new URLSearchParams(window.location.search);


    // ============================
    // 1. Payment Status
    // ============================
    const status = params.get("status") || "success";

    const statusEl = document.getElementById("val-status");
    const titleEl = document.querySelector(".title");
    const messageEl = document.querySelector(".subtitle");

    if (status === "success") {

        if (statusEl) {
            statusEl.textContent = "Successful";
            statusEl.className = "detail-value status-success";
        }

    } else {

        if (statusEl) {
            statusEl.textContent = "Failed";
            statusEl.className = "detail-value status-failed";
        }

        if (titleEl) {
            titleEl.textContent = "Payment Unsuccessful";
        }

        if (messageEl) {
            messageEl.textContent =
                "Your payment could not be completed. Please try again.";
        }
    }



    // ============================
    // 2. Donation Amount
    // ============================
    const amount =
        params.get("amount") ||
        "0";

    const amountEl = document.getElementById("val-amount");

    if (amountEl) {
        amountEl.textContent = `৳${amount}`;
    }



    // ============================
    // 3. Donor Name
    // ============================
    const donorName =
        params.get("donor_name") ||
        params.get("name") ||
        "Anonymous";

    const donorEl = document.getElementById("val-donor");

    if (donorEl) {
        donorEl.textContent = donorName;
    }



    // ============================
    // 4. Donation ID
    // ============================
    const rawDonationId =
        params.get("donation_id") ||
        params.get("donationID");

    let donationId = "--";

    if (rawDonationId) {

        donationId = rawDonationId.startsWith("DON-")
            ? rawDonationId
            : `DON-${rawDonationId}`;

    }


    const donationEl = document.getElementById("val-donation-id");

    if (donationEl) {
        donationEl.textContent = donationId;
    }



    // ============================
    // 5. Transaction ID
    // ============================
    const transactionId =
        params.get("transaction_id") ||
        params.get("trxID") ||
        params.get("trx") ||
        "--";


    const trxEl = document.getElementById("val-trx-id");

    if (trxEl) {
        trxEl.textContent = transactionId;
    }



    // ============================
    // 6. Payment Method
    // ============================
    const paymentMethod =
        params.get("payment_method") ||
        params.get("method") ||
        "bKash";


    const methodEl = document.getElementById("val-method");

    if (methodEl) {
        methodEl.textContent = paymentMethod;
    }



    // ============================
    // 7. Date & Time
    // ============================
    const rawDate = params.get("date");

    let date = new Date();


    if (rawDate) {

        const parsedDate = new Date(rawDate);

        if (!isNaN(parsedDate)) {
            date = parsedDate;
        }

    }


    const formattedDate = date.toLocaleDateString("en-GB", {
        day: "numeric",
        month: "long",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });


    const dateEl = document.getElementById("val-date");

    if (dateEl) {
        dateEl.textContent = formattedDate;
    }

});