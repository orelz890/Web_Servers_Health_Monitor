from models import Webserver, RequestHistory
import requests

class SchedulerService:
    SUCCESS_STATUS_CODE_RANGE = range(200, 300)
    TIMEOUT_SECONDS = 59

    @staticmethod
    def check_webserver_health(webserver_id):
        webserver = Webserver.query.get(webserver_id)
        if not webserver:
            return "Webserver not found", 404

        success, response_code, latency = SchedulerService.perform_health_check(webserver.http_url)
        
        if response_code is None:  # Network error or timeout
            return str(success), 500

        SchedulerService.update_webserver_status(webserver, success)
        SchedulerService.log_request_history(webserver.id, response_code, latency)

        return f"Webserver: {webserver.id} Health check complete", 200


    @staticmethod
    def perform_health_check(url):
        try:
            response = requests.get(url, timeout=SchedulerService.TIMEOUT_SECONDS)
            latency = response.elapsed.total_seconds()
            success = response.status_code in SchedulerService.SUCCESS_STATUS_CODE_RANGE and latency < 60
            return success, response.status_code, latency
        except requests.RequestException as e:
            return e, None, None  # None signifies no response code or latency due to exception

    @staticmethod
    def update_webserver_status(webserver, success):
        new_status = webserver.status
        if success:
            if 0 <= new_status <= 4:
                new_status += 1
            elif new_status < 0:
                new_status = 1
        else:
            if -2 <= new_status <= 0:
                new_status -= 1
            elif new_status > 0:
                new_status = -1

        webserver.update_data({"status": new_status})

    @staticmethod
    def log_request_history(webserver_id, response_code, latency):
        RequestHistory(webserver_id=webserver_id, response_code=response_code, latency=latency).save()
        
    