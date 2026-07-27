async function createDonation(data) {

    const response = await fetch(
        CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.DONATE,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
    );

    if (!response.ok) {

        let message = "Something went wrong.";

        try {
            const err = await response.json();
            message = err.detail || message;
        } catch (_) {}

        throw new Error(message);
    }

    return await response.json();
}