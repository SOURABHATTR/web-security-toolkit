
const baseUrl = "http://127.0.0.1:5000";

// Global variable to store all results
const scanResults = {
    email: null,
    darkweb: null,
    ssl: null,
    vulnerability: null,
    threat: null,
    subdomain: null,
    ports: null
};

// Utility: show loading spinner
function showLoading(elementId) {
    const resultElement = document.getElementById(elementId);
    resultElement.innerHTML = `<p style="color: blue;">Loading...</p>`;
}

// Utility: show proper result
function displayResult(elementId, data) {
    const resultElement = document.getElementById(elementId);
    resultElement.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

// Utility: show errors
function handleError(error, elementId) {
    console.error("Error:", error);
    document.getElementById(elementId).innerHTML = `<p style="color: red;">Error: ${error.message || "An error occurred"}</p>`;
}

// Generic function for backend API call
async function fetchData(endpoint, requestData, resultElement, resultKey = null) {
    showLoading(resultElement);

    try {
        const response = await fetch(`${baseUrl}/${endpoint}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestData),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText);
        }

        const data = await response.json();
        displayResult(resultElement, data);

        if (resultKey) {
            scanResults[resultKey] = data; // 🧠 Store results if key provided
        }
    } catch (error) {
        handleError(error, resultElement);
    }
}

// Perform web vulnerability scan
function performScan() {
    const url = document.getElementById("scanUrl").value.trim();
    if (!url.startsWith("http")) {
        alert("Enter a valid URL with http or https!");
        return;
    }
    fetchData("scan", { url }, "scanResult", "vulnerability");
}

// Threat intelligence check
function checkThreat() {
    const ip = document.getElementById("ipInput").value.trim();
    if (!ip) {
        alert("Enter a valid IP address!");
        return;
    }
    fetchData("threat-check", { ip }, "threatResult", "threat");
}

// Email security check
function checkEmail() {
    const email = document.getElementById("emailInput").value.trim();
    if (!email.includes("@")) {
        alert("Enter a valid email address!");
        return;
    }
    fetchData("email-check", { email }, "emailResult", "email");
}

// SSL certificate check
function checkSSL() {
    const domain = document.getElementById("sslDomain").value.trim();
    if (!domain) {
        alert("Please enter a valid domain name!");
        return;
    }
    fetchData("ssl-check", { domain }, "sslResult", "ssl");
}

// Subdomain enumeration
function enumerateSubdomains() {
    const domain = document.getElementById("subdomainInput").value.trim();
    if (!domain) {
        alert("Please enter a valid domain for subdomain enumeration!");
        return;
    }
    fetchData("subdomain-enum", { domain }, "subdomainResult", "subdomain");
}

// Open port scan
function scanPorts() {
    const ip = document.getElementById("portIp").value.trim();
    if (!ip) {
        alert("Please enter a valid IP address for port scanning!");
        return;
    }
    fetchData("port-scan", { ip }, "portResult", "ports");
}

// Dark Web Monitoring
async function monitorDarkWeb() {
    const queryInput = document.getElementById('darkwebQuery');
    const resultElement = document.getElementById('darkwebResult');

    if (!queryInput || !resultElement) {
        console.error('Input field or result element not found.');
        return;
    }

    const query = queryInput.value.trim();
    if (!query) {
        resultElement.innerHTML = '<p style="color: red;">Please enter a search query</p>';
        return;
    }

    try {
        resultElement.innerHTML = `<p style="color: blue;">Searching dark web for "${query}"...</p>`;

        const response = await fetch(`${baseUrl}/darkweb-monitor`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to search dark web');
        }

        const data = await response.json();
        displayDarkwebResults(data, resultElement);

        scanResults.darkweb = data; // 🧠 Save darkweb scan result

    } catch (error) {
        resultElement.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        console.error('Dark web search error:', error);
    }
}

// Display darkweb results nicely
function displayDarkwebResults(data, element) {
    let html = `<h3>Dark Web Results for: ${data.query}</h3>`;
    html += `<p><strong>Status:</strong> ${data.status}</p>`;

    if (data.results && data.results.length > 0) {
        html += '<div class="results-container">';
        data.results.forEach(result => {
            html += `
                <div class="result-item">
                    <p><strong>Site:</strong> ${result.site}</p>
                    <p><strong>Description:</strong> ${result.description}</p>
                    ${result.date ? `<p><strong>Date:</strong> ${result.date}</p>` : ''}
                </div>
            `;
        });
        html += '</div>';
    } else {
        html += '<p>No results found on the dark web.</p>';
    }

    element.innerHTML = html;
}

// Generate PDF report
function generateReport() {
    showLoading("reportResult"); // Show loading

    const reportData = {
        email: scanResults.email || "Not Scanned",
        darkweb: scanResults.darkweb || "Not Scanned",
        ssl: scanResults.ssl || "Not Scanned",
        vulnerability: scanResults.vulnerability || "Not Scanned",
        threat: scanResults.threat || "Not Scanned",
        subdomain: scanResults.subdomain || "Not Scanned",
        ports: scanResults.ports || "Not Scanned"
    };
    
    
    fetch(`${baseUrl}/generate-report`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(reportData),
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(err => { throw new Error(err); });
        }
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        a.download = "security_report.pdf";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.getElementById("reportResult").innerHTML = `<p style="color: green;">Report Downloaded Successfully!</p>`;
    })
    .catch(error => handleError(error, "reportResult"));
}

// Wait until DOM fully loaded
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("scanBtn")?.addEventListener("click", performScan);
    document.getElementById("threatBtn")?.addEventListener("click", checkThreat);
    document.getElementById("emailBtn")?.addEventListener("click", checkEmail);
    document.getElementById("sslBtn")?.addEventListener("click", checkSSL);
    document.getElementById("subdomainBtn")?.addEventListener("click", enumerateSubdomains);
    document.getElementById("portBtn")?.addEventListener("click", scanPorts);
    document.getElementById("darkwebBtn")?.addEventListener("click", monitorDarkWeb);
    document.getElementById("reportBtn")?.addEventListener("click", generateReport);
});
