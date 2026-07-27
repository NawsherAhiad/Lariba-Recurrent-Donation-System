function showLoading(button,text="Please wait..."){

    button.disabled = true;

    button.dataset.original = button.innerHTML;

    button.innerHTML =
        `<span class="spinner"></span> ${text}`;
}

function hideLoading(button){

    button.disabled = false;

    button.innerHTML = button.dataset.original;
}

function showError(message){

    alert(message);
}