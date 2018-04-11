from project.src.entity.base import Order


class OrderService(object):

    def make_bill(self, order: Order):
        pass

    def save(self, order: Order):
        pass


class ReportService(object):

    def __init__(self, exporter):
        self._exporter = exporter

    def report(self):
        self._exporter.export()
