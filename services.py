from models import Webserver, RequestHistory
import requests

class WebserverService:
    SUCCESS_STATUS_CODE_RANGE = range(200, 300)
    TIMEOUT_SECONDS = 59

    @staticmethod
    def check_webserver_health(webserver_id):
        webserver = Webserver.query.get(webserver_id)
        if not webserver:
            return "Webserver not found", 404

        success, response_code, latency = WebserverService.perform_health_check(webserver.http_url)
        
        if response_code is None:  # Network error or timeout
            return str(success), 500

        WebserverService.update_webserver_status(webserver, success)
        WebserverService.log_request_history(webserver.id, response_code, latency)

        return f"Webserver: {webserver.id} Health check complete", 200

    @staticmethod
    def perform_health_check(url):
        try:
            response = requests.get(url, timeout=WebserverService.TIMEOUT_SECONDS)
            latency = response.elapsed.total_seconds()
            success = response.status_code in WebserverService.SUCCESS_STATUS_CODE_RANGE and latency < 60
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



# from models import Webserver, RequestHistory
# import requests


# class WebserverService:
#     @staticmethod
#     def check_webserver_health(webserver_id):
#         webserver = Webserver.query.get(webserver_id)
#         if not webserver:
#             return "Webserver not found", 404
#         try:
#             response = requests.get(webserver.http_url, timeout=59)
#             latency = response.elapsed.total_seconds()
            
#             success = response.status_code in range(200, 300) and latency < 60
            
#             new_status = webserver.status
#             print(f"========== status before: {new_status} ==============")
#             if new_status is not None:
#                 if success:
#                     if 0 <= new_status <= 4:
#                         new_status += 1
#                     elif new_status < 0:
#                         new_status = 1

#                 # Current check failed
#                 else:
#                     if -2 <= new_status <= 0:
#                         new_status -= 1
#                     elif new_status > 0:
#                         new_status = -1

#                 # This will update the status and the last_checked
#                 webserver.update_data({"status": new_status})
#             print(f"========== status after: {new_status} ==============")
#             RequestHistory(webserver_id=webserver.id, response_code=response.status_code, latency=latency).save()



#             return f"Webserver: {webserver.id} Health check complete", 200
#         except requests.RequestException as e:
#             return str(e), 500
