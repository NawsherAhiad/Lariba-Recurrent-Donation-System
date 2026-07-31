document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("donationForm");
    const submitBtn = document.getElementById("submitBtn");

    const nameInput = document.getElementById("name");
    const emailInput = document.getElementById("email");
    const phoneInput = document.getElementById("phone");
    const amountInput = document.getElementById("amount");
    const resetBtn = document.getElementById("resetBtn");


    // Restore previous values if user comes back
    restoreDonation();


    // Submit donation
    form.addEventListener("submit", submitDonation);



    // Reset button
    resetBtn.addEventListener("click", () => {

        // Reset all form fields
        form.reset();


        // Remove saved donation data
        sessionStorage.removeItem("donationSummary");


        // Reset amount button styles
        document.querySelectorAll(".amount-btn").forEach(btn => {

            btn.classList.remove(
                "bg-emerald-600",
                "text-white",
                "border-emerald-600"
            );

            btn.classList.add(
                "bg-slate-50",
                "text-slate-600",
                "border-slate-200"
            );

        });

    });




    function restoreDonation() {

        const raw = sessionStorage.getItem("donationSummary");

        if (!raw) return;


        const donation = JSON.parse(raw);


        nameInput.value = donation.name || "";

        emailInput.value = donation.email || "";

        phoneInput.value = donation.phone || "";

        amountInput.value = donation.amount || "";

    }




    async function submitDonation(e) {

        e.preventDefault();


        const donation = {

            name: nameInput.value.trim(),

            email: emailInput.value.trim(),

            phone: normalizePhone(phoneInput.value.trim()),

            amount: Number(amountInput.value),

            payment_method: "bkash"

        };



        if (donation.name.length < 3) {

            showError("Please enter your full name.");

            return;

        }



        if (!isValidEmail(donation.email)) {

            showError("Please enter a valid email address.");

            return;

        }



        if (!isValidBDPhone(donation.phone)) {

            showError("Please enter a valid Bangladeshi mobile number.");

            return;

        }



        if (isNaN(donation.amount) || donation.amount < 10) {

            showError("Minimum donation amount is 10 BDT.");

            return;

        }




        sessionStorage.setItem(
            "donationSummary",
            JSON.stringify(donation)
        );



        window.location.href = "summary.html";

    }





    function setAmount(amount, isCustom, button) {


        const buttons = document.querySelectorAll(".amount-btn");


        // Remove active style from all buttons
        buttons.forEach(btn => {

            btn.classList.remove(
                "bg-emerald-600",
                "text-white",
                "border-emerald-600"
            );


            btn.classList.add(
                "bg-slate-50",
                "text-slate-600",
                "border-slate-200"
            );

        });




        // Highlight selected button
        button.classList.remove(
            "bg-slate-50",
            "text-slate-600",
            "border-slate-200"
        );


        button.classList.add(
            "bg-emerald-600",
            "text-white",
            "border-emerald-600"
        );




        if (isCustom) {

            amountInput.value = "";

            amountInput.focus();


        } else {

            amountInput.value = Number(amount);

        }

    }




    // Expose function for inline onclick
    window.setAmount = setAmount;


});