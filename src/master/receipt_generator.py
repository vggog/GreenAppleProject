import base64

import jinja2
import pdfkit

from src.master.model import RepairOrderModel
from src.core.config import load_config


class ReceiptGenerator:
    project_setup = load_config().project_setup
    template_loader = jinja2.FileSystemLoader(project_setup.static_files_dir)
    template_env = jinja2.Environment(loader=template_loader)

    @staticmethod
    def get_image_file() -> str:
        with open(
                f"{ReceiptGenerator.project_setup.static_files_dir}/"
                f"{ReceiptGenerator.project_setup.receipt_logo_name}"
                , 'rb'
        ) as image_file:
            return base64.b64encode(image_file.read()).decode()

    def generate_receipt(self, repair_order: RepairOrderModel):
        date = repair_order.created_at
        date_str = f"{date.day}.{date.month}.{date.year}"
        
        context = {
            "id": repair_order.id,
            "date": date_str,
            "full_name": repair_order.customer_full_name,
            "phone_model": repair_order.phone_model,
            "imei": repair_order.imei,
            "defect": repair_order.defect,
            "note": repair_order.note if repair_order.note else "",
            "image_string": self.get_image_file(),
        }

        template = self.template_env.get_template(
            self.project_setup.receipt_html_template
        )
        return template.render(context)

    def get_receipt(self, repair_order: RepairOrderModel) -> bytes | bool:
        html_receipt = self.generate_receipt(repair_order)

        return pdfkit.from_string(html_receipt)
