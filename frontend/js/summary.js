document.addEventListener("DOMContentLoaded", () => {

    const donation = JSON.parse(
        sessionStorage.getItem("donationSummary")
    );

    if (!donation) {
        window.location.href = "donation.html";
        return;
    }
    const editBtn = document.getElementById("editBtn");

    editBtn.addEventListener("click", () => {
        window.location.href = "donation.html";
    });
    //----------------------------------------------------
    // Populate Voucher
    //----------------------------------------------------

    document.getElementById("summaryName").innerText =
        donation.name;

    document.getElementById("summaryEmail").innerText =
        donation.email;

    document.getElementById("summaryPhone").innerText =
        donation.phone;

    document.getElementById("summaryAmount").innerText =
        Number(donation.amount).toFixed(2) + " BDT";

    document.getElementById("summaryPaymentMethod").innerText =
        "bKash";

    document.getElementById("summaryAmountWords").innerText =
        numberToWords(Number(donation.amount));

    document.getElementById("donationRef").innerText =
        "Pending";

    //----------------------------------------------------
    // Confirm Button
    //----------------------------------------------------

    const donateBtn =
        document.getElementById("confirmDonation");

    donateBtn.addEventListener("click", async () => {

        try {

            showLoading(
                donateBtn,
                "Connecting to bKash..."
            );

            const response = await createDonation(donation);

            console.log(response);

            if (!response.success) {

                throw new Error(response.message);

            }

            const payment = response.data;

            document.getElementById("donationRef").innerText =
                payment.payment_id;

            window.location.href = payment.bkash_url;

        }

        catch (error) {

            hideLoading(donateBtn);

            showError(error.message);

        }

    });

});



function numberToWords(num) {

    if (isNaN(num)) {
        return "Invalid Amount";
    }

    const ones = [
        "", "One", "Two", "Three", "Four", "Five",
        "Six", "Seven", "Eight", "Nine", "Ten",
        "Eleven", "Twelve", "Thirteen", "Fourteen",
        "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"
    ];

    const tens = [
        "", "", "Twenty", "Thirty", "Forty",
        "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"
    ];

    function convert(n) {

        n = Math.floor(n);

        if (n === 0) return "";

        if (n < 20) {
            return ones[n];
        }

        if (n < 100) {
            return tens[Math.floor(n / 10)] +
                (n % 10 ? " " + ones[n % 10] : "");
        }

        if (n < 1000) {
            return ones[Math.floor(n / 100)] +
                " Hundred" +
                (n % 100 ? " " + convert(n % 100) : "");
        }

        if (n < 100000) {
            return convert(Math.floor(n / 1000)) +
                " Thousand" +
                (n % 1000 ? " " + convert(n % 1000) : "");
        }

        if (n < 10000000) {
            return convert(Math.floor(n / 100000)) +
                " Lakh" +
                (n % 100000 ? " " + convert(n % 100000) : "");
        }

        return convert(Math.floor(n / 10000000)) +
            " Crore" +
            (n % 10000000 ? " " + convert(n % 10000000) : "");
    }

    const taka = Math.floor(num);
    const paisa = Math.round((num - taka) * 100);

    let result = "";

    if (taka > 0) {
        result += convert(taka) + " Taka";
    }

    if (paisa > 0) {
        if (result) result += " and ";
        result += convert(paisa) + " Paisa";
    }

    return result + " Only";
}