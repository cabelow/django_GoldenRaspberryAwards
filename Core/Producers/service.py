import logging
from Core.Producers.repository import ProducerRepository

logger = logging.getLogger(__name__)


class ProducerService:
    @staticmethod
    def get_all_producers():
        try:
            return ProducerRepository.get_all_producers()
        except Exception as e:
            logger.error(
                f"Failed to fetch all producers: {str(e)}"
            )
            raise

    @staticmethod
    def get_producer_by_id(producer_id):
        try:
            producer = ProducerRepository.get_producer_by_id(producer_id)
            if not producer:
                logger.warning(
                    f"Producer with ID {producer_id} not found."
                )
            return producer
        except Exception as e:
            logger.error(
                f"Error fetching producer by ID {producer_id}: {str(e)}"
            )
            raise

    @staticmethod
    def create_producer(name):
        try:
            if ProducerRepository.exists_by_name(name):
                message = (
                    f"Producer with name '{name}' already exists."
                )
                logger.warning(message)
                raise ValueError(message)
            producer = ProducerRepository.create_producer(name)
            logger.info(
                f"Producer '{name}' created successfully with ID "
                f"{producer.id}."
            )
            return producer
        except Exception as e:
            logger.error(
                f"Error creating producer '{name}': {str(e)}"
            )
            raise

    @staticmethod
    def update_producer(producer_id, name):
        try:
            producer = ProducerRepository.update_producer(producer_id, name)
            if producer:
                logger.info(
                    f"Producer ID {producer_id} updated successfully."
                )
            else:
                logger.warning(
                    f"Producer ID {producer_id} not found."
                )
            return producer
        except Exception as e:
            logger.error(
                f"Error updating producer ID {producer_id}: {str(e)}"
            )
            raise

    @staticmethod
    def delete_producer(producer_id):
        try:
            success = ProducerRepository.delete_producer(producer_id)
            if success:
                logger.info(
                    f"Producer ID {producer_id} deleted successfully."
                )
            else:
                logger.warning(
                    f"Producer ID {producer_id} not found."
                )
            return success
        except Exception as e:
            logger.error(
                f"Error deleting producer ID {producer_id}: {str(e)}"
            )
            raise
