function normalizePhone(phone){

    phone = phone.replace(/\s+/g,"");

    if(phone.startsWith("+880"))
        phone = "0" + phone.substring(4);

    else if(phone.startsWith("880"))
        phone = "0" + phone.substring(3);

    return phone;
}

function isValidBDPhone(phone){

    phone = normalizePhone(phone);

    return /^01[3-9]\d{8}$/.test(phone);
}

function isValidEmail(email){

    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}