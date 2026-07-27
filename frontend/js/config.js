// const CONFIG = {
//     API_BASE_URL: "http://127.0.0.1:8000/api/v1",

//     ENDPOINTS: {
//         DONATE: "/donations",
//         QUERY_PAYMENT: "/bkash/query",
//         SEARCH_TRANSACTION: "/bkash/search"
//     }
// };

const isLocal = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";

const CONFIG = {
    // If local, use full localhost URL; otherwise use relative path ""
    API_BASE_URL: isLocal ? "http://127.0.0.1:8000/api/v1" : "/api/v1",

    ENDPOINTS: {
        DONATE: "/donations",
        QUERY_PAYMENT: "/bkash/query",
        SEARCH_TRANSACTION: "/bkash/search"
    }
};