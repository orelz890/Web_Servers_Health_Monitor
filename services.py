from models import Webserver, RequestHistory
import requests


class WebserverService:
    @staticmethod
    def check_webserver_health(webserver_id):
        webserver = Webserver.query.get(webserver_id)
        if not webserver:
            return "Webserver not found", 404
        try:
            response = requests.get(webserver.http_url, timeout=59)
            latency = response.elapsed.total_seconds()
            
            success = response.status_code in range(200, 300) and latency < 60
            
            RequestHistory(webserver_id=webserver.id, response_code=response.status_code, latency=latency).save()
            
            # This will update the status and the last_checked
            webserver.update_data({"status": success})
            
            return f"Webserver: {webserver.id} Health check complete", 200
        except requests.RequestException as e:
            return str(e), 500
