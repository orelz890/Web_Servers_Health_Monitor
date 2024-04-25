from abc import ABC, abstractmethod
from models.models import Webserver, RequestHistory
import requests
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from datetime import datetime, timedelta
from models.models import db
from typing import Tuple


class ProtocolHandler(ABC):

    
    """
    Abstract base class for handling different network protocols
    for health checks. This class defines a common interface for all protocol handlers.
    """
    @abstractmethod
    def check_webserver_health(self, url, webserver_id):
        """
        Perform a health check for a given webserver. Must be implemented by each protocol handler.

        :param webserver: the URL of a Webserver instance.
        :return: A tuple (success, response_code, latency) representing the outcome of the health check.
        """
        pass


    @staticmethod
    def delete_old_request_histories():
        week_ago = datetime.utcnow() - timedelta(days=7)
        try:
            old_entries_count = RequestHistory.query.filter(RequestHistory.timestamp < week_ago).delete()
            db.session.commit()
            logging.info(f"Deleted {old_entries_count} old request histories successfully.")
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"Failed to delete old request histories: {str(e)}")