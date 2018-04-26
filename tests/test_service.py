import pytest
from mock import Mock, patch
from datetime import datetime

from src.base.entity import ReportRecord
from src.service.exception import ServiceError
from src.service.exporter import ConsoleExporter
from src.service.service import ReportService, OrderService
from src.store.dao import DaoManager
from src.store.db import DataSource
from src.utils.file import TemplateUtil, FileUtil


@pytest.mark.service
class TestOrderService(object):

    @pytest.fixture
    def mock_dao_manager(self):
        return Mock(spec=DaoManager(DataSource()))

    @pytest.fixture
    def mock_console_exporter(self):
        return Mock(spec=ConsoleExporter())

    @pytest.fixture
    def order_service(self, mock_dao_manager):
        return OrderService(mock_dao_manager)

    @pytest.fixture
    def report_service(self, mock_dao_manager):
        return ReportService(mock_dao_manager)

    @patch("src.service.service.datetime")
    @patch.object(FileUtil, 'write')
    @patch.object(TemplateUtil, 'process')
    def test_order_service_make_bill(self, template_util, file_util, datetime_mock, order_service, valid_order):
        bill_data_format = "%Y-%m-%d %H:%M:%S"
        bill_template_path = "./../resource/template/bill.txt"
        bill_outcome_path_template = "./../outcome/{}.txt"

        template = "template string"
        template_util.return_value = template

        time_now = datetime(2018, 4, 24, 22, 16, 26, 39793)
        formatted_date = time_now.strftime(bill_data_format)
        datetime_mock.now = Mock(return_value=time_now)

        order_service.make_bill(valid_order)

        items_to_string = "\n".join([item.__str__() for item in valid_order.items])
        template_data = {"date": formatted_date, "user": valid_order.user.fullname, "item": items_to_string}

        template_util.assert_called_once_with(bill_template_path, template_data)
        file_util.assert_called_once_with(bill_outcome_path_template.format(formatted_date), template)

    def test_order_service_make_bill_invalid_order(self, order_service, invalid_order):
        with pytest.raises(ServiceError, message="Expect ServiceError if order passed to service is without items"):
            order_service.make_bill(invalid_order)

    def test_order_service_save_valid_order(self, mock_dao_manager, order_service, valid_order):
        order_id = 1
        mock_dao_manager.order_dao.persist.return_value = order_id

        order_service.save(valid_order)

        mock_dao_manager.order_dao.persist.assert_called_with(valid_order)
        for item in valid_order.items:
            mock_dao_manager.item_dao.persist.assert_any_call(item, order_id)

        mock_dao_manager.commit.assert_called_once()
        mock_dao_manager.close_connection.assert_called_once()

    def test_order_service_save_invalid_order(self, order_service, invalid_order):
        with pytest.raises(ServiceError, message="Expect ServiceError if order passed to service is without items"):
            order_service.save(invalid_order)

    def test_report_service_report_to_console(self, mock_dao_manager, report_service, mock_console_exporter):
        test_report_records = [ReportRecord("Test_0, Test1", 20, 20.1010),
                               ReportRecord("Test_2, Test_3", 10, 10.0101)]
        exp_export_data = [
            (report_record.fullname, str(report_record.sales_number), str(report_record.sales_value))
            for report_record in test_report_records]
        exp_total_sales = str(sum([report_record.sales_number for report_record in test_report_records]))
        exp_total_values = str(sum([report_record.sales_value for report_record in test_report_records]))

        mock_dao_manager.report_dao.get_sales_records.return_value = test_report_records
        report_service.report(mock_console_exporter)
        mock_console_exporter.export.assert_called_once_with(exp_export_data, exp_total_sales, exp_total_values)

    def test_report_service_attribute_error(self, mock_dao_manager, report_service):
        with pytest.raises(AttributeError, message="Expect AttributeError if the arg of report method is an object "
                                                   "without export interface."):
            mock_dao_manager.report_dao.get_sales_records.return_value = [ReportRecord("Test_0, Test1", 20, 20.1010)]
            mock_without_export_method = Mock(spec=ObjectWoExportMethod())
            report_service.report(mock_without_export_method)


class ObjectWoExportMethod(object):
    pass
