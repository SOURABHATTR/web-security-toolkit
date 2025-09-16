from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import logging
import asyncio

# Import modules
from generate_report import generate_report
from darkweb_monitor import monitordarkweb

try:
    import scanner
    import threat_intelligence
    import email_checker
    import ssl_checker
    import subdomain_enum
    import port_scanner
except ImportError as e:
    logging.error(f"Module import error: {e}")

# Initialize Flask app
app = Flask(__name__)

# Proper CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Logging
logging.basicConfig(level=logging.INFO)



@app.route('/scan', methods=['POST'])
def scan_website():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"error": "URL is required"}), 400

        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        result = asyncio.run(scanner.full_security_scan(url))
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Scan error: {e}", exc_info=True)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/threat-check', methods=['POST'])
def threat_check():
    try:
        data = request.get_json()
        ip = data.get('ip')
        if not ip:
            return jsonify({"error": "IP address is required"}), 400
        result = threat_intelligence.check_ip(ip)
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Threat check error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/email-check', methods=['POST'])
def email_check():
    try:
        data = request.get_json()
        email = data.get('email')
        if not email:
            return jsonify({"error": "Email is required"}), 400
        result = email_checker.check_email(email)
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Email check error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/ssl-check', methods=['POST'])
def ssl_check():
    try:
        data = request.get_json()
        domain = data.get('domain')
        if not domain:
            return jsonify({"error": "Domain is required"}), 400
        result = ssl_checker.check_ssl(domain)
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"SSL check error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/subdomain-enum', methods=['POST'])
def subdomain_enum_route():
    try:
        data = request.get_json()
        domain = data.get('domain')
        if not domain:
            return jsonify({"error": "Domain is required"}), 400
        result = subdomain_enum.get_subdomains(domain)
        return jsonify({"subdomains": result}), 200
    except Exception as e:
        logging.error(f"Subdomain enumeration error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/port-scan', methods=['POST'])
def port_scan_route():
    try:
        data = request.get_json()
        ip = data.get('ip')
        if not ip:
            return jsonify({"error": "IP address is required"}), 400
        result = port_scanner.scan_ports(ip)
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Port scan error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/darkweb-monitor', methods=['POST'])
def darkweb_monitor_route():
    try:
        data = request.get_json()
        keyword = data.get('query')
        if not keyword:
            return jsonify({"error": "Query is required"}), 400
        result = monitordarkweb(keyword)
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Dark web monitoring error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/generate-report', methods=['POST'])
def generate_report_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        filename = "security_report.pdf"
        result = generate_report(data, filename)

        if "error" in result:
            return jsonify(result), 400

        return send_file(filename, as_attachment=True)
    except Exception as e:
        logging.error(f"Report generation error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Web Security Toolkit API is running!"}), 200

# ---------------------------------------

if __name__ == '__main__':
    app.run(debug=False)
