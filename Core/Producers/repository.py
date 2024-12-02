from Core.Producers.models import Producer


class ProducerRepository:
    @staticmethod
    def get_all_producers():
        return Producer.objects.all()

    @staticmethod
    def get_producer_by_id(producer_id):
        try:
            return Producer.objects.get(id=producer_id)
        except Producer.DoesNotExist:
            return None

    @staticmethod
    def get_or_create_producer(producer_names):
        producers = []
        for name in producer_names:
            producer, _ = Producer.objects.get_or_create(name=name.strip())
            producers.append(producer)
        return producers

    @staticmethod
    def get_or_create_producer_by_id(producer_id):
        try:
            return Producer.objects.get(id=producer_id)
        except Producer.DoesNotExist:
            return None

    @staticmethod
    def create_producer(name):
        return Producer.objects.create(name=name)

    @staticmethod
    def exists_by_name(name):
        return Producer.objects.filter(name=name).exists()

    @staticmethod
    def update_producer(producer_id, name):
        producer = ProducerRepository.get_producer_by_id(producer_id)
        if producer:
            producer.name = name
            producer.save()
            return producer
        return None

    @staticmethod
    def delete_producer(producer_id):
        producer = ProducerRepository.get_producer_by_id(producer_id)
        if producer:
            producer.delete()
            return True
        return False
